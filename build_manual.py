#!/usr/bin/env python3
"""
Manual PyInstaller build script that bypasses problematic hooks
Save as: build_manual.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def clean_build():
    """Clean previous builds"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}/")


def disable_problematic_hooks():
    """Temporarily disable problematic PyInstaller hooks"""
    import PyInstaller
    pyinstaller_path = Path(PyInstaller.__file__).parent
    hooks_path = pyinstaller_path / "hooks" / "pre_safe_import_module"

    distutils_hook = hooks_path / "hook-distutils.py"
    setuptools_hook = hooks_path / "hook-setuptools.py"

    # Backup and disable hooks
    for hook_file in [distutils_hook, setuptools_hook]:
        if hook_file.exists():
            backup_file = hook_file.with_suffix('.py.backup')
            if not backup_file.exists():
                shutil.copy2(hook_file, backup_file)
                print(f"Backed up {hook_file}")

            # Create empty hook file
            with open(hook_file, 'w') as f:
                f.write('# Temporarily disabled hook\ndef pre_safe_import_module(hook_api):\n    pass\n')
            print(f"Disabled {hook_file}")


def restore_hooks():
    """Restore original hooks"""
    import PyInstaller
    pyinstaller_path = Path(PyInstaller.__file__).parent
    hooks_path = pyinstaller_path / "hooks" / "pre_safe_import_module"

    for hook_name in ["hook-distutils.py", "hook-setuptools.py"]:
        hook_file = hooks_path / hook_name
        backup_file = hook_file.with_suffix('.backup')

        if backup_file.exists():
            shutil.copy2(backup_file, hook_file)
            print(f"Restored {hook_file}")


def build_mysql_cli():
    """Build MySQL CLI with manual PyInstaller command"""

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name=ambivo-mysql-cli',
        '--console',
        '--noupx',  # Disable UPX
        '--clean',

        # Hidden imports
        '--hidden-import=mysql.connector',
        '--hidden-import=mysql.connector.cursor',
        '--hidden-import=mysql.connector.errors',
        '--hidden-import=pandas',
        '--hidden-import=pandas.io.sql',
        '--hidden-import=sqlalchemy',
        '--hidden-import=sqlalchemy.dialects.mysql',
        '--hidden-import=tabulate',

        # Exclude problematic modules
        '--exclude-module=distutils',
        '--exclude-module=setuptools',
        '--exclude-module=pkg_resources',
        '--exclude-module=psycopg2',
        '--exclude-module=duckdb',
        '--exclude-module=matplotlib',
        '--exclude-module=tkinter',

        # Add runtime hook
        '--runtime-hook=hooks/rthook_suppress_warnings.py',

        # Source file
        'mysql_cli.py'
    ]

    print("Building MySQL CLI...")
    print("Command:", ' '.join(cmd))

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Build successful!")
        print("Executable location: dist/ambivo-mysql-cli.exe")
    else:
        print("❌ Build failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

    return result.returncode == 0


def build_db_cli():
    """Build Multi-DB CLI with manual PyInstaller command"""

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name=ambivo-db-cli',
        '--console',
        '--noupx',
        '--clean',

        # Hidden imports for all databases
        '--hidden-import=mysql.connector',
        '--hidden-import=psycopg2',
        '--hidden-import=duckdb',
        '--hidden-import=sqlite3',
        '--hidden-import=pandas',
        '--hidden-import=pandas.io.sql',
        '--hidden-import=sqlalchemy',
        '--hidden-import=sqlalchemy.dialects.mysql',
        '--hidden-import=sqlalchemy.dialects.postgresql',
        '--hidden-import=sqlalchemy.dialects.sqlite',
        '--hidden-import=tabulate',

        # Exclude problematic modules
        '--exclude-module=distutils',
        '--exclude-module=setuptools',
        '--exclude-module=pkg_resources',
        '--exclude-module=matplotlib',
        '--exclude-module=tkinter',

        # Add runtime hook
        '--runtime-hook=hooks/rthook_suppress_warnings.py',

        # Source file
        'db_cli.py'
    ]

    print("Building Multi-Database CLI...")
    print("Command:", ' '.join(cmd))

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Build successful!")
        print("Executable location: dist/ambivo-db-cli.exe")
    else:
        print("❌ Build failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

    return result.returncode == 0


def main():
    """Main build process"""
    print("🚀 Ambivo CLI Manual Build Script")
    print("=" * 50)

    # Step 1: Clean previous builds
    clean_build()

    # Step 2: Disable problematic hooks
    try:
        disable_problematic_hooks()

        # Step 3: Build applications
        mysql_success = build_mysql_cli()
        db_success = build_db_cli()

        # Step 4: Report results
        print("\n" + "=" * 50)
        print("Build Results:")
        print(f"MySQL CLI: {'✅ Success' if mysql_success else '❌ Failed'}")
        print(f"Multi-DB CLI: {'✅ Success' if db_success else '❌ Failed'}")

        if mysql_success or db_success:
            print("\n📁 Output files in dist/ directory")

    finally:
        # Step 5: Always restore hooks
        restore_hooks()
        print("\n🔄 Hooks restored")


if __name__ == "__main__":
    main()