from __future__ import annotations

import argparse
import json
import os
import socket
import sqlite3
import sys
from pathlib import Path
from urllib import error, request

ROOT = Path(__file__).resolve().parent


def load_env(env_file: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not env_file.exists():
        return env
    for raw_line in env_file.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        env[key.strip()] = value.strip()
    return env


def socket_check(host: str, port: int, timeout: float = 3.0) -> tuple[bool, str]:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, 'reachable'
    except OSError as exc:
        return False, str(exc)


def http_check(url: str, timeout: float = 5.0) -> tuple[bool, str]:
    try:
        with request.urlopen(url, timeout=timeout) as response:
            return True, f'HTTP {response.status}'
    except error.HTTPError as exc:
        return False, f'HTTP {exc.code}'
    except Exception as exc:
        return False, str(exc)


def append_health_path(url: str) -> str:
    if url.endswith('/health'):
        return url
    return url.rstrip('/') + '/health'


def sqlite_check(path: Path) -> tuple[bool, str]:
    try:
        with sqlite3.connect(path) as connection:
            connection.execute('select 1')
        return True, f'opened {path.name}'
    except Exception as exc:
        return False, str(exc)


def postgres_check(env: dict[str, str]) -> tuple[bool, str]:
    host = env.get('POSTGRES_HOST', '127.0.0.1')
    port = int(env.get('POSTGRES_PORT', '5432'))
    try:
        import psycopg
    except Exception:
        return socket_check(host, port)
    try:
        conn = psycopg.connect(
            host=host,
            port=port,
            dbname=env.get('POSTGRES_DB', 'sentinelke'),
            user=env.get('POSTGRES_USER', 'sentinelke'),
            password=env.get('POSTGRES_PASSWORD', ''),
            connect_timeout=3,
        )
        conn.close()
        return True, 'authenticated'
    except Exception as exc:
        return False, str(exc)


def report(name: str, result: tuple[bool, str]) -> dict[str, str | bool]:
    ok, detail = result
    status = 'OK' if ok else 'FAIL'
    print(f'[{status}] {name}: {detail}')
    return {'name': name, 'ok': ok, 'detail': detail}


def main() -> int:
    parser = argparse.ArgumentParser(description='SentinelKE health checks')
    parser.add_argument('--env-file', default='.env.dev')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    env = os.environ.copy()
    env.update(load_env(ROOT / args.env_file))
    skip_external = env.get('SKIP_EXTERNAL_HEALTHCHECKS', 'False').lower() == 'true'

    checks = []
    if env.get('DJANGO_SETTINGS_MODULE', '').endswith('settings_local'):
        checks.append(report('local-sqlite', sqlite_check(ROOT / 'backend' / 'local.sqlite3')))
    else:
        checks.append(report('postgres', postgres_check(env)))

    redis_host = env.get('REDIS_HOST', '127.0.0.1')
    redis_port = int(env.get('REDIS_PORT', '6379'))
    checks.append(report('redis', socket_check(redis_host, redis_port)))
    checks.append(report('neo4j', socket_check('127.0.0.1', 7687)))
    checks.append(report('web-dashboard', http_check(env.get('WEB_DASHBOARD_URL', 'http://127.0.0.1:8010'))))
    checks.append(report('mobile-api', http_check(env.get('API_BASE_URL', 'http://127.0.0.1:8010'))))
    checks.append(report('ai-service', http_check(append_health_path(env.get('AI_SERVICE_URL', env.get('ML_SERVICE_URL', 'http://127.0.0.1:9000'))))))
    checks.append(report('llama-cpp', http_check(append_health_path(env.get('LLAMA_CPP_URL', 'http://127.0.0.1:8080')))))
    checks.append(report('ussd-service', http_check(append_health_path(env.get('USSD_BASE_URL', 'http://127.0.0.1:8050')))))
    if skip_external:
        checks.append(report('map-service', (True, 'skipped external check')))
    else:
        checks.append(report('map-service', http_check(env.get('MAP_SERVICE_URL', 'https://tile.openstreetmap.org'))))
    checks.append(report('background-worker-broker', socket_check(redis_host, redis_port)))

    if args.json:
        print(json.dumps(checks, indent=2))
    return 0 if all(item['ok'] for item in checks) else 1


if __name__ == '__main__':
    sys.exit(main())
