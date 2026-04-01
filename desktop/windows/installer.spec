# PyInstaller spec for SentinelKE desktop launcher.

from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

spec_dir = Path(globals().get('SPECPATH', '.')).resolve()
project_root = spec_dir.parents[1]
block_cipher = None
hiddenimports = collect_submodules('uvicorn')

a = Analysis(
    [str(spec_dir / 'launcher.py')],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        (str(project_root / '.env.desktop'), '.'),
        (str(project_root / 'backend'), 'backend'),
        (str(project_root / 'ml_services'), 'ml_services'),
        (str(project_root / 'services' / 'ussd_service'), 'services/ussd_service'),
        (str(project_root / 'desktop' / 'windows' / 'assets'), 'assets'),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SentinelKE_Setup',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon='assets/sentinelke.ico' if Path('assets/sentinelke.ico').exists() else None,
    onefile=True,
)
