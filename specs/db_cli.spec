# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Build Specification for Ambivo DB CLI v2.1.0
Includes matplotlib and all required dependencies.
Platform: Universal (Windows/Linux/macOS)

Build with: pyinstaller db_cli.spec
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Application metadata
APP_NAME = "ambivo-db-cli"
VERSION = "2.1.0"

block_cipher = None

# Collect data files for packages that need them
try:
    matplotlib_datas = collect_data_files('matplotlib', include_py_files=True)
except:
    matplotlib_datas = []

try:
    pandas_datas = collect_data_files('pandas')
except:
    pandas_datas = []

try:
    sqlalchemy_datas = collect_data_files('sqlalchemy')
except:
    sqlalchemy_datas = []

# Filter out unnecessary matplotlib data to reduce size
filtered_matplotlib_datas = []
for src, dst in matplotlib_datas:
    # Exclude large unnecessary files
    if not any(exclude in src.lower() for exclude in [
        'tests', 'test_', 'sample_data', 'examples',
        'backends/web_backend', 'backends/qt', 'backends/tk'
    ]):
        filtered_matplotlib_datas.append((src, dst))

# Comprehensive hidden imports
hiddenimports = [
    # Database drivers
    'mysql.connector',
    'mysql.connector.cursor',
    'mysql.connector.pooling',
    'mysql.connector.connection',
    'mysql.connector.errors',
    'psycopg2',
    'psycopg2.extras',
    'psycopg2.extensions',
    'psycopg2.pool',
    'duckdb',
    'sqlite3',

    # Core data processing
    'pandas',
    'pandas.core',
    'pandas.io',
    'pandas.io.common',
    'pandas.io.sql',
    'pandas.io.parsers',
    'sqlalchemy',
    'sqlalchemy.dialects',
    'sqlalchemy.dialects.mysql',
    'sqlalchemy.dialects.postgresql',
    'sqlalchemy.dialects.sqlite',
    'sqlalchemy.engine',
    'sqlalchemy.pool',
    'numpy',
    'numpy.core',
    'numpy.core._multiarray_umath',

    # Visualization (matplotlib)
    'matplotlib',
    'matplotlib.pyplot',
    'matplotlib.figure',
    'matplotlib.axes',
    'matplotlib.dates',
    'matplotlib.backends',
    'matplotlib.backends.backend_agg',
    'matplotlib.backends._backend_agg',
    'matplotlib.ft2font',
    'matplotlib._path',
    'matplotlib._contour',
    'matplotlib._image',
    'matplotlib._tri',
    'matplotlib._qhull',
    'matplotlib.colors',
    'matplotlib.patches',
    'matplotlib.lines',

    # Matplotlib dependencies
    'kiwisolver',
    'cycler',
    'pyparsing',
    'python_dateutil',
    'python_dateutil.tz',
    'dateutil',
    'dateutil.tz',
    'six',
    'fonttools',
    'fonttools.ttLib',
    'pillow',
    'PIL',
    'PIL.Image',

    # Standard libraries that might be missed
    'tabulate',
    'urllib',
    'urllib.parse',
    'urllib.request',
    'tempfile',
    'subprocess',
    'platform',
    'shutil',
    'logging',
    'logging.handlers',
    'datetime',
    'argparse',
    'textwrap',
    'getpass',
    'warnings',
    'abc',
    'typing',
    'pathlib',
    're',
    'json',
    'csv',
    'io',
    'time',
    'os',
    'sys',
    'collections',
    'collections.abc',
    'weakref',
    'threading',
    'multiprocessing',

    # Additional pandas dependencies
    'pandas._libs',
    'pandas._libs.tslibs',
    'pandas.util._decorators',
    'pandas.core.dtypes',
    'pandas.core.arrays',
    'pandas.core.ops',

    # Additional numpy dependencies
    'numpy.random',
    'numpy.linalg',
    'numpy.fft',

    # Additional SQLAlchemy dependencies
    'sqlalchemy.sql',
    'sqlalchemy.sql.sqltypes',
    'sqlalchemy.sql.type_api',
]

# Platform-specific hidden imports
if sys.platform.startswith('win'):
    hiddenimports.extend([
        'win32api',
        'win32con',
        'win32process',
        'pywintypes',
        'win32file',
        'win32security',
    ])
elif sys.platform.startswith('darwin'):
    hiddenimports.extend([
        'Foundation',
        'AppKit',
    ])

# Database-specific hidden imports (only if available)
try:
    import mysql.connector
    hiddenimports.extend([
        'mysql.connector.locales',
        'mysql.connector.locales.eng',
    ])
except ImportError:
    pass

try:
    import psycopg2
    hiddenimports.extend([
        'psycopg2._psycopg',
        'psycopg2.tz',
    ])
except ImportError:
    pass

a = Analysis(
    ['db_cli.py'],
    pathex=[],
    binaries=[],
    datas=filtered_matplotlib_datas + pandas_datas + sqlalchemy_datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary GUI frameworks
        'tkinter',
        'tkinter.ttk',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'wx',
        'wxPython',

        # Exclude test frameworks
        'test',
        'tests',
        'testing',
        'unittest',
        'unittest2',
        'pytest',
        'nose',
        'doctest',

        # Exclude development tools
        'IPython',
        'jupyter',
        'jupyter_client',
        'jupyter_core',
        'notebook',
        'nbformat',
        'zmq',

        # Exclude unnecessary matplotlib backends
        'matplotlib.backends.backend_qt5agg',
        'matplotlib.backends.backend_qt4agg',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.backends.backend_gtk3agg',
        'matplotlib.backends.backend_gtk3cairo',
        'matplotlib.backends.backend_webagg',
        'matplotlib.backends.backend_pdf',
        'matplotlib.backends.backend_ps',
        'matplotlib.backends.backend_svg',

        # Large scientific packages not needed
        'scipy',
        'sklearn',
        'scikit-learn',
        'tensorflow',
        'torch',
        'keras',
        'sympy',
        'numba',
        'statsmodels',

        # Other large packages
        'django',
        'flask',
        'requests',
        'urllib3',
        'certifi',
        'chardet',
        'idna',

        # Audio/video packages
        'cv2',
        'moviepy',
        'imageio',
        'skimage',

        # Exclude large data files
        'matplotlib.mpl-data.fonts',
        'matplotlib.mpl-data.sample_data',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate entries and optimize
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Build single executable (recommended for distribution)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,  # Keep symbols for better error reporting
    upx=True,  # Compress with UPX if available
    upx_exclude=[
        # Don't compress these (can cause issues)
        'python*.dll',
        'api-ms-win-*.dll',
        'vcruntime*.dll',
    ],
    runtime_tmpdir=None,
    console=True,  # Console application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt' if sys.platform.startswith('win') else None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

# Alternative: Directory distribution (uncomment for folder instead of single file)
# Faster startup time but multiple files
#
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[
#         'python*.dll',
#         'api-ms-win-*.dll',
#         'vcruntime*.dll',
#     ],
#     name=APP_NAME,
# )

# Build info
print(f"""
🚀 PyInstaller Build Configuration for {APP_NAME} v{VERSION}

Target: Single executable
Platform: {sys.platform}
Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}

Features included:
- All database drivers (MySQL, PostgreSQL, SQLite, DuckDB)
- CSV import/export with pandas
- Data visualization with matplotlib
- URL import capabilities
- Platform-specific optimizations

Build with: pyinstaller db_cli.spec
Output: dist/{APP_NAME}(.exe)

Estimated size: 120-180 MB (single file)
Startup time: 2-4 seconds
""")