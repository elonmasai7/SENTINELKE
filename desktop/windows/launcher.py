from __future__ import annotations

import argparse
import os
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path
from tkinter import BOTH, END, LEFT, RIGHT, Button, Frame, Label, Text, Tk

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / '.runtime'
RUNTIME.mkdir(exist_ok=True)


def load_env(path: Path) -> dict[str, str]:
    env = os.environ.copy()
    if path.exists():
        for raw_line in path.read_text(encoding='utf-8').splitlines():
            line = raw_line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            env[key.strip()] = value.strip()
    return env


def check_python() -> None:
    if sys.version_info < (3, 11):
        raise RuntimeError('SentinelKE desktop launcher requires Python 3.11 or newer.')


def spawn(name: str, command: list[str], cwd: Path, env: dict[str, str]) -> subprocess.Popen:
    stdout = (RUNTIME / f'{name}.out.log').open('a', encoding='utf-8')
    stderr = (RUNTIME / f'{name}.err.log').open('a', encoding='utf-8')
    process = subprocess.Popen(command, cwd=str(cwd), env=env, stdout=stdout, stderr=stderr)
    (RUNTIME / f'{name}.pid').write_text(str(process.pid), encoding='utf-8')
    return process


class DesktopShell:
    def __init__(self, env: dict[str, str], headless: bool = False) -> None:
        self.env = env
        self.headless = headless
        self.processes: dict[str, subprocess.Popen] = {}
        self.dashboard_url = env.get('WEB_DASHBOARD_URL', 'http://127.0.0.1:8010')
        self.llama_url = env.get('LLAMA_CPP_URL', 'http://127.0.0.1:8080')

    def start_services(self) -> None:
        backend_env = self.env.copy()
        backend_env.setdefault('DJANGO_SETTINGS_MODULE', 'sentinelke.settings_local')
        self.processes['django'] = spawn(
            'django',
            [sys.executable, 'backend/manage.py', 'runserver', '127.0.0.1:8010', '--settings=sentinelke.settings_local'],
            ROOT,
            backend_env,
        )
        self.processes['ml'] = spawn(
            'ml',
            [sys.executable, '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '9000'],
            ROOT / 'ml_services',
            self.env.copy(),
        )
        if self.env.get('LLAMA_CPP_COMMAND'):
            self.processes['llama'] = spawn(
                'llama',
                self.env['LLAMA_CPP_COMMAND'].split(),
                ROOT,
                self.env.copy(),
            )
        if not self.headless:
            threading.Thread(target=self._open_dashboard_when_ready, daemon=True).start()

    def _open_dashboard_when_ready(self) -> None:
        from urllib import request

        deadline = time.time() + 45
        while time.time() < deadline:
            try:
                with request.urlopen(self.dashboard_url, timeout=5) as response:
                    if response.status < 500:
                        webbrowser.open(self.dashboard_url)
                        return
            except Exception:
                time.sleep(1)

    def stop_services(self) -> None:
        for process in self.processes.values():
            if process.poll() is None:
                process.terminate()
        self.processes.clear()

    def status_lines(self) -> list[str]:
        lines = [f'Python: {sys.executable}', f'Dashboard: {self.dashboard_url}', f'llama.cpp: {self.llama_url}']
        for name, process in self.processes.items():
            state = 'running' if process.poll() is None else f'exited ({process.returncode})'
            lines.append(f'{name}: {state}')
        return lines

    def run_ui(self) -> None:
        root = Tk()
        root.title('SentinelKE Desktop Control Panel')
        root.geometry('720x420')

        header = Label(root, text='SentinelKE Desktop Control Panel', font=('Segoe UI', 16, 'bold'))
        header.pack(pady=12)

        text = Text(root, wrap='word')
        text.pack(fill=BOTH, expand=True, padx=12, pady=12)

        buttons = Frame(root)
        buttons.pack(fill='x', padx=12, pady=(0, 12))

        def refresh() -> None:
            text.delete('1.0', END)
            text.insert('1.0', '\n'.join(self.status_lines()))
            root.after(2000, refresh)

        Button(buttons, text='Open Dashboard', command=lambda: webbrowser.open(self.dashboard_url)).pack(side=LEFT)
        Button(buttons, text='Open Logs', command=lambda: webbrowser.open(str(RUNTIME))).pack(side=LEFT, padx=8)
        Button(buttons, text='Stop Services', command=self.stop_services).pack(side=RIGHT)
        refresh()

        def on_close() -> None:
            self.stop_services()
            root.destroy()

        root.protocol('WM_DELETE_WINDOW', on_close)
        root.mainloop()


def main() -> int:
    parser = argparse.ArgumentParser(description='SentinelKE Windows desktop launcher')
    parser.add_argument('--service', action='store_true', help='Run in headless service mode')
    parser.add_argument('--env-file', default=str(ROOT / '.env.desktop'))
    args = parser.parse_args()

    check_python()
    env = load_env(Path(args.env_file))
    shell = DesktopShell(env=env, headless=args.service)
    shell.start_services()
    if args.service:
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            shell.stop_services()
        return 0
    shell.run_ui()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
