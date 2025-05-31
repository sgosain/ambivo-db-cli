# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Ambivo Multi-Database CLI (db_cli.py)

This spec file creates a standalone executable for the universal database CLI
that supports MySQL, PostgreSQL, SQLite, and DuckDB.

Author: Hemant Gosain 'Sunny'
Company: Ambivo
License: MIT
"""

import os
import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Add the parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

block_cipher = None

# Collect all submodules for database drivers
mysql_modules = collect_submodules('mysql.connector')
psycopg2_modules = collect_submodules('psycopg2')
sqlalchemy_modules = collect_submodules('sqlalchemy')

# Analysis for Multi-Database CLI
a = Analysis(
    ['../db_cli.py'],  # Relative path to source file from specs/ directory
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[
        # MySQL connector dependencies
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
        'mysql.connector.authentication',
        'mysql.connector.network',
        'mysql.connector.utils',
        'mysql.connector.catch23',

        # PostgreSQL dependencies
        'psycopg2',
        'psycopg2.extras',
        'psycopg2.extensions',
        'psycopg2.pool',
        'psycopg2._psycopg',
        'psycopg2._range',
        'psycopg2.tz',
        'psycopg2.errorcodes',
        'psycopg2.sql',

        # DuckDB dependencies
        'duckdb',

        # SQLite (built-in but ensure it's included)
        'sqlite3',

        # SQLAlchemy and its dialects
        'sqlalchemy',
        'sqlalchemy.engine',
        'sqlalchemy.engine.default',
        'sqlalchemy.engine.reflection',
        'sqlalchemy.sql',
        'sqlalchemy.sql.sqltypes',
        'sqlalchemy.sql.type_api',
        'sqlalchemy.dialects',
        'sqlalchemy.dialects.mysql',
        'sqlalchemy.dialects.mysql.mysqlconnector',
        'sqlalchemy.dialects.postgresql',
        'sqlalchemy.dialects.postgresql.psycopg2',
        'sqlalchemy.dialects.sqlite',
        'sqlalchemy.dialects.sqlite.pysqlite',
        'sqlalchemy.pool',
        'sqlalchemy.event',
        'sqlalchemy.util',

        # Pandas dependencies for CSV import
        'pandas',
        'pandas.io',
        'pandas.io.sql',
        'pandas.io.common',
        'pandas.io.parsers',
        'pandas.core',
        'pandas.core.dtypes',
        'pandas._libs',
        'pandas._libs.tslib',

        # Core dependencies
        'tabulate',
        'tabulate.tabulate',

        # Optional readline support
        'readline',
        'rlcompleter',

        # Standard library modules that might be missed
        'json',
        'csv',
        'datetime',
        'getpass',
        'subprocess',
        'textwrap',
        'argparse',
        'abc',
        'typing',
        'pathlib',
        'os',
        'sys',
        'platform',
        'socket',
        'ssl',
        'hashlib',
        'hmac',
        'base64',
        'urllib',
        'urllib.parse',
        'email',
        'email.utils',
        'decimal',
        'uuid',
        'struct',
        'collections',
        'collections.abc',
        'functools',
        'itertools',
        'operator',
        'copy',
        'pickle',
        'io',
        'warnings',
        'logging',
        're',
        'string',
        'time',
        'calendar',
        'math',
        'random',
        'threading',
        'queue',
        'multiprocessing',
        'concurrent',
        'concurrent.futures',

        # Additional SQLAlchemy modules
        'sqlalchemy.orm',
        'sqlalchemy.schema',
        'sqlalchemy.types',
        'sqlalchemy.inspection',
        'sqlalchemy.exc',

        # Additional pandas modules
        'pandas.plotting',
        'pandas.tseries',
        'pandas.api',
        'pandas.compat',

        # NumPy (pandas dependency)
        'numpy',
        'numpy.core',
        'numpy.lib',
        'numpy.random',

        # Additional database-related modules
        'dateutil',
        'dateutil.parser',
        'pytz',
        'zoneinfo',

    ] + mysql_modules + psycopg2_modules + sqlalchemy_modules,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude GUI and unnecessary modules to reduce size
        'matplotlib',
        'matplotlib.pyplot',
        'tkinter',
        'tkinter.ttk',
        'PyQt4',
        'PyQt5',
        'PyQt6',
        'PySide',
        'PySide2',
        'PySide6',
        'wx',
        'IPython',
        'jupyter',
        'notebook',
        'sphinx',
        'pytest',
        'setuptools',
        'distutils',
        'pip',
        'wheel',

        # Exclude development/testing modules
        'test',
        'tests',
        'testing',
        'unittest',
        'doctest',
        'pdb',
        'profile',
        'cProfile',
        'pstats',
        'timeit',
        'trace',

        # Exclude other heavy modules not needed
        'scipy',
        'sklearn',
        'tensorflow',
        'torch',
        'cv2',
        'PIL',
        'Pillow',
        'bokeh',
        'plotly',
        'seaborn',
        'statsmodels',

        # Exclude unused pandas modules
        'pandas.plotting._matplotlib',
        'pandas.io.clipboard',
        'pandas.io.excel',
        'pandas.io.feather',
        'pandas.io.gbq',
        'pandas.io.html',
        'pandas.io.json',
        'pandas.io.orc',
        'pandas.io.parquet',
        'pandas.io.pickle',
        'pandas.io.pytables',
        'pandas.io.sas',
        'pandas.io.spss',
        'pandas.io.stata',
        'pandas.plotting._core',
        'pandas.plotting._style',
        'pandas.plotting._tools',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate entries
a.pure = list(set(a.pure))
a.binaries = list(set(a.binaries))

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ambivo-db-cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                    # Enable UPX compression for smaller binaries
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,                # Keep console for CLI application
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,                   # Add path to .ico file if you have one: 'assets/ambivo-icon.ico'
    version='../version_info.txt' if os.path.exists('../version_info.txt') else None,
)