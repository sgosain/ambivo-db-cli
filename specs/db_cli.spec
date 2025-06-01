# enhanced_db_cli.spec - Fixed pandas import issue
# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

a = Analysis(
    ['../db_cli.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[
        # Core database dependencies
        'mysql.connector',
        'mysql.connector.conversion',
        'mysql.connector.cursor',
        'mysql.connector.errors',
        'mysql.connector.constants',
        'mysql.connector.authentication',

        # PostgreSQL dependencies
        'psycopg2',
        'psycopg2.extras',
        'psycopg2.extensions',

        # DuckDB
        'duckdb',

        # SQLite (built-in)
        'sqlite3',

        # SQLAlchemy - ESSENTIAL modules
        'sqlalchemy',
        'sqlalchemy.engine',
        'sqlalchemy.engine.default',
        'sqlalchemy.sql',
        'sqlalchemy.sql.sqltypes',
        'sqlalchemy.dialects',
        'sqlalchemy.dialects.mysql',
        'sqlalchemy.dialects.mysql.mysqlconnector',
        'sqlalchemy.dialects.postgresql',
        'sqlalchemy.dialects.postgresql.psycopg2',
        'sqlalchemy.dialects.sqlite',
        'sqlalchemy.pool',
        'sqlalchemy.types',

        # Pandas - CRITICAL: Include ALL necessary pandas modules
        'pandas',
        'pandas.core',
        'pandas.core.arrays',
        'pandas.core.arrays.categorical',
        'pandas.core.arrays.datetimes',
        'pandas.core.arrays.numeric',
        'pandas.core.arrays.period',
        'pandas.core.arrays.timedeltas',
        'pandas.core.computation',
        'pandas.core.dtypes',
        'pandas.core.dtypes.common',
        'pandas.core.dtypes.dtypes',
        'pandas.core.dtypes.generic',
        'pandas.core.dtypes.inference',
        'pandas.core.dtypes.missing',
        'pandas.core.frame',
        'pandas.core.generic',
        'pandas.core.groupby',
        'pandas.core.indexes',
        'pandas.core.indexes.api',
        'pandas.core.indexes.base',
        'pandas.core.indexes.category',
        'pandas.core.indexes.datetimes',
        'pandas.core.indexes.extension',
        'pandas.core.indexes.frozen',
        'pandas.core.indexes.multi',
        'pandas.core.indexes.numeric',
        'pandas.core.indexes.period',
        'pandas.core.indexes.range',
        'pandas.core.indexes.timedeltas',
        'pandas.core.internals',
        'pandas.core.ops',
        'pandas.core.reshape',
        'pandas.core.series',
        'pandas.core.tools',
        'pandas.io',
        'pandas.io.sql',
        'pandas.io.common',
        'pandas.io.parsers',
        'pandas.io.parsers.readers',
        'pandas._libs',
        'pandas._libs.lib',
        'pandas._libs.tslib',
        'pandas._libs.hashtable',
        'pandas._libs.algos',
        'pandas._libs.interval',
        'pandas._libs.join',
        'pandas._libs.missing',
        'pandas._libs.reduction',
        'pandas._libs.reshape',
        'pandas._libs.sparse',
        'pandas._libs.writers',
        'pandas.util',
        'pandas.util._decorators',

        # NumPy - Required by pandas
        'numpy',
        'numpy.core',
        'numpy.core._multiarray_umath',
        'numpy.core.multiarray',
        'numpy.core.numeric',
        'numpy.core.umath',
        'numpy.lib',
        'numpy.lib.format',
        'numpy.linalg',
        'numpy.random',
        'numpy.random._pickle',
        'numpy.random.mtrand',

        # Other essential modules
        'tabulate',
        'datetime',
        'json',
        'csv',
        'getpass',
        'argparse',
        'textwrap',
        'subprocess',
        'warnings',
        'os',
        'sys',
        'abc',
        'typing',
        'pathlib',

        # Optional but useful
        'readline',
        'rlcompleter',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[
        '../hooks/rthook_suppress_warnings.py'
    ],
    excludes=[
        # Exclude problematic modules
        'distutils',
        'setuptools',
        'pkg_resources',

        # Heavy modules not needed
        'matplotlib',
        'tkinter',
        'PyQt5',
        'PyQt6',
        'jupyter',
        'IPython',
        'scipy',
        'sklearn',
        'tensorflow',
        'torch',

        # Unused pandas modules
        'pandas.plotting',
        'pandas.io.clipboard',
        'pandas.io.excel',
        'pandas.io.feather',
        'pandas.io.parquet',
        'pandas.io.pickle',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Clean duplicates and remove problematic entries
a.pure = list(set(a.pure))
a.binaries = list(set(a.binaries))

# Remove distutils entries
a.pure = [x for x in a.pure if not x[0].startswith('distutils')]
a.binaries = [x for x in a.binaries if not x[0].startswith('distutils')]

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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)