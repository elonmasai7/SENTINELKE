from __future__ import annotations

import argparse
import os
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent
RUNTIME_DIR = ROOT / '.runtime'
RUNTIME_DIR.mkdir(exist_ok=True)


@dataclass
class ManagedProcess:
    name: str
    command: list[str]
    cwd: Path
    env: dict[str, str]
    pid_file: Path
    stdout_file: Path
    stderr_file: Path
    process: subprocess.Popen | None = None

    def start(self) -> None:
        if self.is_running():
            return
        self.stdout_file.parent.mkdir(parents=True, exist_ok=True)
        stdout_handle = self.stdout_file.open('a', encoding='utf-8')
        stderr_handle = self.stderr_file.open('a', encoding='utf-8')
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        self.process = subprocess.Popen(
            self.command,
            cwd=str(self.cwd),
            env=self.env,
            stdout=stdout_handle,
            stderr=stderr_handle,
            creationflags=creationflags,
        )
        self.pid_file.write_text(str(self.process.pid), encoding='utf-8')

    def is_running(self) -> bool:
        if self.process and self.process.poll() is None:
            return True
        if self.pid_file.exists():
            try:
                pid = int(self.pid_file.read_text(encoding='utf-8').strip())
            except ValueError:
                return False
            if _pid_exists(pid):
                return True
        return False

    def stop(self) -> None:
        pid = None
        if self.process and self.process.poll() is None:
            pid = self.process.pid
        elif self.pid_file.exists():
            try:
                pid = int(self.pid_file.read_text(encoding='utf-8').strip())
            except ValueError:
                pid = None
        if pid:
            _terminate_pid(pid)
        if self.pid_file.exists():
            self.pid_file.unlink(missing_ok=True)


def _pid_exists(pid: int) -> bool:
    try:
        if os.name == 'nt':
            result = subprocess.run(
                ['tasklist', '/FI', f'PID eq {pid}'],
                capture_output=True,
                text=True,
                check=False,
            )
            return str(pid) in result.stdout
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def _terminate_pid(pid: int) -> None:
    try:
        if os.name == 'nt':
            subprocess.run(['taskkill', '/PID', str(pid), '/T', '/F'], check=False, capture_output=True)
        else:
            os.kill(pid, signal.SIGTERM)
    except Exception:
        pass


def load_env(env_file: Path) -> dict[str, str]:
    env = os.environ.copy()
    if env_file.exists():
        for raw_line in env_file.read_text(encoding='utf-8').splitlines():
            line = raw_line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            env[key.strip()] = value.strip()
    return env


def wait_for_http(url: str, timeout: int = 60) -> bool:
    from urllib import request

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with request.urlopen(url, timeout=5) as response:
                if response.status < 500:
                    return True
        except Exception:
            time.sleep(1)
    return False


def check_socket(host: str, port: int, timeout: float = 2.0) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
            return True
        except OSError:
            return False


def maybe_start_infra(env: dict[str, str], compose_file: Path) -> None:
    docker = shutil.which('docker')
    if not docker or not compose_file.exists():
        return
    command = [docker, 'compose', '-f', str(compose_file), 'up', '-d', 'postgres', 'redis', 'neo4j', 'llama-cpp']
    subprocess.run(command, cwd=str(ROOT), check=False)
    time.sleep(3)


def managed_processes(env: dict[str, str]) -> list[ManagedProcess]:
    python_exe = sys.executable
    backend_env = env.copy()
    backend_env.setdefault('DJANGO_SETTINGS_MODULE', env.get('DJANGO_SETTINGS_MODULE', 'sentinelke.settings_local'))
    celery_env = env.copy()
    celery_env.setdefault('DJANGO_SETTINGS_MODULE', env.get('DJANGO_SETTINGS_MODULE', 'sentinelke.settings_local'))
    return [
        ManagedProcess(
            name='django',
            command=[python_exe, 'backend/manage.py', 'runserver', '127.0.0.1:8010', '--settings=sentinelke.settings_local'],
            cwd=ROOT,
            env=backend_env,
            pid_file=RUNTIME_DIR / 'django.pid',
            stdout_file=RUNTIME_DIR / 'django.out.log',
            stderr_file=RUNTIME_DIR / 'django.err.log',
        ),
        ManagedProcess(
            name='ml-service',
            command=[python_exe, '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '9000'],
            cwd=ROOT / 'ml_services',
            env=env.copy(),
            pid_file=RUNTIME_DIR / 'ml.pid',
            stdout_file=RUNTIME_DIR / 'ml.out.log',
            stderr_file=RUNTIME_DIR / 'ml.err.log',
        ),
        ManagedProcess(
            name='celery',
            command=[python_exe, '-m', 'celery', '-A', 'sentinelke', 'worker', '-l', 'info'],
            cwd=ROOT / 'backend',
            env=celery_env,
            pid_file=RUNTIME_DIR / 'celery.pid',
            stdout_file=RUNTIME_DIR / 'celery.out.log',
            stderr_file=RUNTIME_DIR / 'celery.err.log',
        ),
        ManagedProcess(
            name='ussd-service',
            command=[python_exe, 'services/ussd_service/app.py'],
            cwd=ROOT,
            env=env.copy(),
            pid_file=RUNTIME_DIR / 'ussd.pid',
            stdout_file=RUNTIME_DIR / 'ussd.out.log',
            stderr_file=RUNTIME_DIR / 'ussd.err.log',
        ),
    ]


def launch_mobile_emulator(command: str) -> None:
    if not command:
        return
    subprocess.Popen(command, cwd=str(ROOT), shell=True)


def run(args: argparse.Namespace) -> int:
    env = load_env(ROOT / args.env_file)
    maybe_start_infra(env, ROOT / 'docker-compose.yml')

    infra_checks = {
        'postgres': ('127.0.0.1', int(env.get('POSTGRES_PORT', '5432'))),
        'redis': (env.get('REDIS_HOST', '127.0.0.1'), int(env.get('REDIS_PORT', '6379'))),
        'neo4j': ('127.0.0.1', 7687),
    }
    for name, (host, port) in infra_checks.items():
        print(f'[{name}] reachable={check_socket(host, port)} on {host}:{port}')

    if env.get('ENABLE_MOBILE_EMULATOR', 'False').lower() == 'true' and not args.no_mobile_emulator:
        launch_mobile_emulator(env.get('MOBILE_EMULATOR_COMMAND', ''))

    processes = managed_processes(env)
    if env.get('LLAMA_CPP_COMMAND'):
        processes.append(
            ManagedProcess(
                name='llama-cpp',
                command=env['LLAMA_CPP_COMMAND'].split(),
                cwd=ROOT,
                env=env.copy(),
                pid_file=RUNTIME_DIR / 'llama.pid',
                stdout_file=RUNTIME_DIR / 'llama.out.log',
                stderr_file=RUNTIME_DIR / 'llama.err.log',
            )
        )

    for process in processes:
        process.start()
        print(f'Started {process.name}')

    if wait_for_http(env.get('WEB_DASHBOARD_URL', 'http://127.0.0.1:8010')) and env.get('OPEN_BROWSER_ON_START', 'True').lower() == 'true' and not args.no_browser:
        threading.Thread(target=webbrowser.open, args=(env.get('WEB_DASHBOARD_URL', 'http://127.0.0.1:8010'),), daemon=True).start()

    print('SentinelKE stack is running. Press Ctrl+C to stop managed host processes.')
    try:
        while True:
            time.sleep(2)
            for process in processes:
                if not process.is_running():
                    print(f'{process.name} is no longer running.')
    except KeyboardInterrupt:
        print('Stopping managed processes...')
        for process in reversed(processes):
            process.stop()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Run the full SentinelKE application stack.')
    parser.add_argument('--env-file', default='.env.dev')
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--no-mobile-emulator', action='store_true')
    return parser


if __name__ == '__main__':
    raise SystemExit(run(build_parser().parse_args()))
