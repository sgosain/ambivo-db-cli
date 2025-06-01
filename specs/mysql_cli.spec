# mysql_simple.spec - Simplified MySQL CLI (Most Reliable)
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../mysql_cli.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        # Core MySQL
        'mysql.connector',
        'mysql.connector.conversion',
        'mysql.connector.cursor',
        'mysql.connector.errors',

        # Core CSV support
        'pandas',
        'pandas.io.sql',
        'sqlalchemy',
        'sqlalchemy.engine',
        'sqlalchemy.dialects.mysql.mysqlconnector',

        # Essential
        'tabulate',
        'readline',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Only exclude what we really don't need
        'matplotlib',
        'tkinter',
        'PyQt5',
        'PyQt6',
        'scipy',
        'sklearn',
        'tensorflow',
        'torch',
        'PIL',
        'cv2',
        'pytest',
        'IPython',
        'jupyter',
    ],
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
    name='ambivo-mysql-cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)