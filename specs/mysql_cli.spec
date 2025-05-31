# mysql_only.spec - MySQL CLI Only (Smaller Binary)
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../mysql_cli.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'mysql.connector',
        'mysql.connector.conversion',
        'mysql.connector.abstracts',
        'mysql.connector.constants',
        'mysql.connector.cursor',
        'mysql.connector.pooling',
        'mysql.connector.protocol',
        'mysql.connector.errors',
        'mysql.connector.locales',
        'mysql.connector.charsets',
        'tabulate',
        'pandas',
        'sqlalchemy',
        'sqlalchemy.dialects.mysql',
        'readline'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude other database drivers for smaller MySQL-only binary
        'psycopg2',
        'duckdb',
        'matplotlib',
        'tkinter',
        'PyQt5'
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