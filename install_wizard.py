from __future__ import annotations

import getpass
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def ask(prompt: str, default: str = '') -> str:
    suffix = f' [{default}]' if default else ''
    value = input(f'{prompt}{suffix}: ').strip()
    return value or default


def write_env(path: Path, values: dict[str, str]) -> None:
    lines = [f'{key}={value}' for key, value in values.items()]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> int:
    print('SentinelKE installation wizard')
    print('This wizard prepares environment files and service settings without rebuilding the core application.\n')

    install_dir = ask('Install location', str(ROOT))
    domain = ask('Primary web domain', 'sentinelke.local')
    db_host = ask('PostgreSQL host', '127.0.0.1')
    db_name = ask('PostgreSQL database', 'sentinelke')
    db_user = ask('PostgreSQL user', 'sentinelke')
    db_password = getpass.getpass('PostgreSQL password [hidden]: ') or 'change-this'
    admin_user = ask('Initial admin username', 'admin')
    ai_provider = ask('Default AI provider', 'openrouter')
    api_base_url = ask('Mobile API base URL', f'https://{domain}')
    ai_service_url = ask('Mobile AI service URL', f'https://{domain}/ai')
    map_service_url = ask('Mobile map service URL', 'https://tile.openstreetmap.org')
    install_services = ask('Install Windows/Linux services now? (yes/no)', 'yes').lower() in {'yes', 'y'}

    prod_values = {
        'DJANGO_SETTINGS_MODULE': 'sentinelke.settings',
        'DJANGO_DEBUG': 'False',
        'DJANGO_ALLOWED_HOSTS': f'{domain},localhost,127.0.0.1',
        'DJANGO_SECURE_SSL_REDIRECT': 'True',
        'DJANGO_SECRET_KEY': 'replace-me',
        'POSTGRES_DB': db_name,
        'POSTGRES_USER': db_user,
        'POSTGRES_PASSWORD': db_password,
        'POSTGRES_HOST': db_host,
        'POSTGRES_PORT': '5432',
        'REDIS_HOST': '127.0.0.1',
        'REDIS_PORT': '6379',
        'REDIS_URL': 'redis://127.0.0.1:6379/2',
        'CELERY_BROKER_URL': 'redis://127.0.0.1:6379/0',
        'CELERY_RESULT_BACKEND': 'redis://127.0.0.1:6379/1',
        'NEO4J_URI': 'bolt://127.0.0.1:7687',
        'NEO4J_USER': 'neo4j',
        'NEO4J_PASSWORD': 'change-this',
        'WEB_DASHBOARD_URL': f'https://{domain}',
        'API_BASE_URL': api_base_url,
        'AI_SERVICE_URL': ai_service_url,
        'MAP_SERVICE_URL': map_service_url,
        'USSD_BASE_URL': 'http://127.0.0.1:8050',
        'USSD_TARGET_URL': f'https://{domain}/api/integrations/ussd/africastalking/',
        'AI_DEFAULT_PROVIDER': ai_provider,
        'INSTALL_DIR': install_dir,
        'ADMIN_USERNAME': admin_user,
    }
    mobile_values = {
        'API_BASE_URL': api_base_url,
        'AI_SERVICE_URL': ai_service_url,
        'MAP_SERVICE_URL': map_service_url,
        'WS_BASE_URL': api_base_url.replace('https://', 'wss://').replace('http://', 'ws://'),
    }

    write_env(ROOT / '.env.prod', prod_values)
    write_env(ROOT / '.env.mobile', mobile_values)
    shutil.copyfile(ROOT / '.env.prod', ROOT / 'deploy' / 'web' / '.env.production')

    print('\nPrepared:')
    print(f'  - {ROOT / ".env.prod"}')
    print(f'  - {ROOT / ".env.mobile"}')
    print(f'  - {ROOT / "deploy" / "web" / ".env.production"}')
    print(f'  - Admin bootstrap target user: {admin_user}')
    if install_services:
        print('  - Service installation can now be completed with desktop/windows/install_service.ps1 or deploy/linux/install.sh')
    else:
        print('  - Service installation skipped by user choice')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
