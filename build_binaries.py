#!/usr/bin/env python3
"""
Ambivo Database CLI Suite - Binary Builder
Builds standalone executables for Mac, Windows, and Linux

Author: Hemant Gosain 'Sunny'
Company: Ambivo
License: MIT
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False


def install_pyinstaller():
    """Install PyInstaller if not present."""
    print("Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])


def create_build_dirs():
    """Create necessary build directories."""
    dirs = ["dist", "build", "binaries"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)

    # Platform-specific directories
    system = platform.system().lower()
    arch = platform.machine().lower()

    if arch in ['x86_64', 'amd64']:
        arch = 'x64'
    elif arch in ['i386', 'i686']:
        arch = 'x86'
    elif arch.startswith('arm'):
        arch = 'arm64' if '64' in arch else 'arm'

    platform_dir = f"binaries/{system}-{arch}"
    Path(platform_dir).mkdir(parents=True, exist_ok=True)
    return platform_dir


def create_warning_hook():
    """Create warning suppression hook."""
    hooks_dir = Path('hooks')
    hooks_dir.mkdir(exist_ok=True)

    hook_content = '''import warnings
import os
import sys

# Suppress all warnings
os.environ['PYTHONWARNINGS'] = 'ignore'
warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")

# Suppress specific warning categories
for category in [UserWarning, DeprecationWarning, FutureWarning, 
                PendingDeprecationWarning, ImportWarning, ResourceWarning]:
    warnings.filterwarnings("ignore", category=category)

# Redirect stderr to suppress remaining warnings
import io
sys.stderr = io.StringIO()
'''

    hook_file = hooks_dir / 'rthook_suppress_warnings.py'
    with open(hook_file, 'w') as f:
        f.write(hook_content)

    return str(hook_file)


def check_spec_files():
    """Check if spec files exist."""
    mysql_spec = Path("specs/mysql_cli.spec")
    db_spec = Path("specs/db_cli.spec")
    return mysql_spec.exists(), db_spec.exists()


def build_mysql_cli_with_spec(output_dir):
    """Build mysql_cli.py binary using spec file."""
    print("Building MySQL CLI binary using spec file...")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "specs/mysql_cli.spec",
        "--distpath", output_dir,
        "--workpath", "build/mysql_cli",
        "--clean"
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✓ MySQL CLI binary created in {output_dir}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Spec file build failed: {e}")
        return False


def build_db_cli_with_spec(output_dir):
    """Build db_cli.py binary using spec file."""
    print("Building Multi-Database CLI binary using spec file...")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "specs/db_cli.spec",
        "--distpath", output_dir,
        "--workpath", "build/db_cli",
        "--clean"
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✓ Multi-Database CLI binary created in {output_dir}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Spec file build failed: {e}")
        return False


def build_mysql_cli_manual(output_dir, hook_file):
    """Fallback: Build MySQL CLI with direct PyInstaller command."""
    print("Building MySQL CLI manually (fallback)...")

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name=ambivo-mysql-cli',
        '--console',
        '--clean',
        '--distpath', output_dir,
        '--workpath', 'build/mysql_cli_manual',

        # Hidden imports
        '--hidden-import=mysql.connector',
        '--hidden-import=mysql.connector.cursor',
        '--hidden-import=mysql.connector.errors',
        '--hidden-import=mysql.connector.conversion',
        '--hidden-import=pandas',
        '--hidden-import=pandas.io.sql',
        '--hidden-import=sqlalchemy',
        '--hidden-import=sqlalchemy.engine',
        '--hidden-import=sqlalchemy.dialects.mysql',
        '--hidden-import=sqlalchemy.dialects.mysql.mysqlconnector',
        '--hidden-import=tabulate',
        '--hidden-import=importlib_metadata',

        # Exclude modules
        '--exclude-module=psycopg2',
        '--exclude-module=duckdb',
        '--exclude-module=matplotlib',
        '--exclude-module=tkinter',
        '--exclude-module=PyQt5',
        '--exclude-module=PyQt6',

        # Runtime hook
        f'--runtime-hook={hook_file}',

        # Source file
        'mysql_cli.py'
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✓ MySQL CLI manual build successful")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Manual build failed: {e}")
        return False


def build_db_cli_manual(output_dir, hook_file):
    """Fallback: Build Multi-DB CLI with direct PyInstaller command."""
    print("Building Multi-Database CLI manually (fallback)...")

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name=ambivo-db-cli',
        '--console',
        '--clean',
        '--distpath', output_dir,
        '--workpath', 'build/db_cli_manual',

        # Hidden imports for all databases
        '--hidden-import=mysql.connector',
        '--hidden-import=mysql.connector.cursor',
        '--hidden-import=mysql.connector.errors',
        '--hidden-import=psycopg2',
        '--hidden-import=psycopg2.extras',
        '--hidden-import=duckdb',
        '--hidden-import=sqlite3',
        '--hidden-import=pandas',
        '--hidden-import=pandas.io.sql',
        '--hidden-import=sqlalchemy',
        '--hidden-import=sqlalchemy.engine',
        '--hidden-import=sqlalchemy.dialects.mysql',
        '--hidden-import=sqlalchemy.dialects.postgresql',
        '--hidden-import=sqlalchemy.dialects.sqlite',
        '--hidden-import=tabulate',
        '--hidden-import=importlib_metadata',

        # Exclude modules
        '--exclude-module=matplotlib',
        '--exclude-module=tkinter',
        '--exclude-module=PyQt5',
        '--exclude-module=PyQt6',

        # Runtime hook
        f'--runtime-hook={hook_file}',

        # Source file
        'db_cli.py'
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✓ Multi-Database CLI manual build successful")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Manual build failed: {e}")
        return False


def create_convenience_scripts(output_dir):
    """Create convenience scripts (platform-aware)."""
    system = platform.system().lower()

    if system == "windows":
        # Windows batch files
        mysql_batch = f"""@echo off
set "DIR=%~dp0"
"%DIR%ambivo-mysql-cli.exe" %*
"""
        db_batch = f"""@echo off
set "DIR=%~dp0"
"%DIR%ambivo-db-cli.exe" %*
"""

        with open(os.path.join(output_dir, "mysql.bat"), "w") as f:
            f.write(mysql_batch)
        with open(os.path.join(output_dir, "dbcli.bat"), "w") as f:
            f.write(db_batch)

    else:
        # Unix shell scripts
        mysql_shell = f"""#!/bin/bash
DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
exec "$DIR/ambivo-mysql-cli" "$@"
"""
        db_shell = f"""#!/bin/bash
DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
exec "$DIR/ambivo-db-cli" "$@"
"""

        mysql_script = os.path.join(output_dir, "mysql")
        db_script = os.path.join(output_dir, "dbcli")

        with open(mysql_script, "w") as f:
            f.write(mysql_shell)
        with open(db_script, "w") as f:
            f.write(db_shell)

        # Make executable
        os.chmod(mysql_script, 0o755)
        os.chmod(db_script, 0o755)


def create_platform_readme(output_dir):
    """Create platform-specific README."""
    system = platform.system().lower()
    arch = platform.machine().lower()

    if arch in ['x86_64', 'amd64']:
        arch = 'x64'
    elif arch in ['i386', 'i686']:
        arch = 'x86'
    elif arch.startswith('arm'):
        arch = 'arm64' if '64' in arch else 'arm'

    # Platform-specific content
    if system == "darwin":  # macOS
        platform_content = """
## macOS Installation

### Option 1: Applications Folder (Recommended)
1. Copy binaries to /Applications/
2. Add to PATH in ~/.zshrc: `export PATH=$PATH:/Applications`

### Option 2: User Installation
1. Run: `./install.sh`
2. Follow the prompts

### Usage
```bash
# Direct execution
./ambivo-mysql-cli -H localhost -u root
./ambivo-db-cli mysql -H localhost -u root

# If in Applications folder
ambivo-mysql-cli -H localhost -u root
ambivo-db-cli mysql -H localhost -u root
```
"""
    else:
        platform_content = f"""
## {system.title()} Installation

### Quick Installation
1. Run: `./install.sh` (Linux) or `install.bat` (Windows)
2. Follow the prompts

### Manual Installation
1. Copy binaries to desired location
2. Add to PATH (optional)
3. Run directly

### Usage
```bash
# Interactive mode (recommended for beginners)
./ambivo-mysql-cli
./ambivo-db-cli

# Command line mode
./ambivo-mysql-cli -H localhost -u root -p
./ambivo-db-cli mysql -H localhost -u root -p -d mydb
```
"""

    readme_content = f"""# Ambivo Database CLI Suite - {system.title()} {arch.upper()}

## Quick Start - Interactive Mode 

Just run without arguments for guided setup:
```bash
./ambivo-mysql-cli
./ambivo-db-cli
```

{platform_content}

## Features

- ✅ Standalone executables (no Python installation required)
- ✅ Interactive setup for beginners
- ✅ Full database connectivity (MySQL, PostgreSQL, SQLite, DuckDB)
- ✅ CSV import with intelligent mapping
- ✅ Command history and tab completion
- ✅ Professional table formatting
- ✅ Cross-platform compatibility

## Database Support

### MySQL CLI (`ambivo-mysql-cli`)
- Dedicated MySQL client
- 95%+ MySQL cheat sheet compatibility
- Optimized for MySQL workflows

### Multi-Database CLI (`ambivo-db-cli`)
- Universal database client
- Supports: MySQL, PostgreSQL, SQLite, DuckDB
- Consistent interface across all databases

## Examples

```bash
# MySQL - Production web applications
./ambivo-mysql-cli -H prod-server -u admin -d app_db

# PostgreSQL - Enterprise applications  
./ambivo-db-cli postgresql -H pg-server -u postgres -d warehouse

# SQLite - Development and testing
./ambivo-db-cli sqlite -f local_app.db

# DuckDB - Analytics and data science
./ambivo-db-cli duckdb -f analytics.db
```

## CSV Import Examples

```bash
# In interactive mode
mysql> csv_import data.csv users --create-table
postgresql> csv_import large_data.csv products --chunk-size=5000
duckdb> CREATE TABLE sales AS SELECT * FROM 'sales_data.csv'
```

## System Requirements

- **Platform**: {system.title()} {arch.upper()}
- **Dependencies**: None (standalone executables)
- **Memory**: 512MB+ recommended for large CSV imports
- **Storage**: ~50MB for both binaries

## Support

- 📧 **Email**: sgosain@ambivo.com
- 🏢 **Company**: https://www.ambivo.com
- 🐛 **Issues**: https://github.com/sgosain/ambivo-db-cli/issues
- 📚 **Documentation**: https://github.com/sgosain/ambivo-db-cli

## Version Information

- **CLI Version**: 2.1.0
- **Build Date**: Local build
- **Platform**: {system}-{arch}

Built with ❤️ by Hemant Gosain 'Sunny' at Ambivo
"""

    with open(os.path.join(output_dir, "README.txt"), "w") as f:
        f.write(readme_content)


def create_install_script(output_dir):
    """Create platform-specific installation script."""
    system = platform.system().lower()

    if system == "windows":
        install_content = """@echo off
echo 🚀 Installing Ambivo Database CLI Suite for Windows...

set "INSTALL_DIR=%USERPROFILE%\\AppData\\Local\\Ambivo"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

copy *.exe "%INSTALL_DIR%\\" >nul
copy *.bat "%INSTALL_DIR%\\" >nul
copy README.txt "%INSTALL_DIR%\\" >nul

echo.
echo ✅ Installed to: %INSTALL_DIR%
echo.
echo To use globally, add this to your PATH:
echo %INSTALL_DIR%
echo.
echo Quick test:
echo "%INSTALL_DIR%\\ambivo-mysql-cli.exe" --help
echo "%INSTALL_DIR%\\ambivo-db-cli.exe" --help
echo.
echo 💡 Tip: Run without arguments for interactive setup
pause
"""
    elif system == "darwin":  # macOS
        install_content = """#!/bin/bash
echo "🍎 Installing Ambivo Database CLI Suite for macOS..."

# Option 1: Applications folder (if writable)
if [ -w "/Applications" ]; then
    echo "Installing to /Applications (system-wide access)..."
    cp ambivo-mysql-cli "/Applications/"
    cp ambivo-db-cli "/Applications/"
    echo "✅ Installed to /Applications"
    echo ""
    echo "You can now run:"
    echo "/Applications/ambivo-mysql-cli"
    echo "/Applications/ambivo-db-cli"
    echo ""
    echo "Or add to PATH in ~/.zshrc:"
    echo "export PATH=\\$PATH:/Applications"
else
    # Option 2: User local bin
    echo "Installing to ~/.local/bin (user access)..."
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
    cp ambivo-mysql-cli "$INSTALL_DIR/"
    cp ambivo-db-cli "$INSTALL_DIR/"
    cp mysql "$INSTALL_DIR/"
    cp dbcli "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR"/*
    echo "✅ Installed to: $INSTALL_DIR"
    echo ""
    echo "Add to PATH by adding this to your ~/.zshrc:"
    echo "export PATH=\\$PATH:$INSTALL_DIR"
fi

echo ""
echo "💡 Tip: Run without arguments for interactive setup"
"""
    else:  # Linux
        install_content = """#!/bin/bash
echo "🐧 Installing Ambivo Database CLI Suite for Linux..."

INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

# Copy executables
cp ambivo-mysql-cli "$INSTALL_DIR/"
cp ambivo-db-cli "$INSTALL_DIR/"
cp mysql "$INSTALL_DIR/"
cp dbcli "$INSTALL_DIR/"
cp README.txt "$INSTALL_DIR/"

# Make executable
chmod +x "$INSTALL_DIR/ambivo-mysql-cli"
chmod +x "$INSTALL_DIR/ambivo-db-cli"
chmod +x "$INSTALL_DIR/mysql"
chmod +x "$INSTALL_DIR/dbcli"

echo "✅ Installed to: $INSTALL_DIR"
echo ""
echo "Add to PATH by adding this to your ~/.bashrc or ~/.zshrc:"
echo "export PATH=\\$PATH:$INSTALL_DIR"
echo ""
echo "Or run directly:"
echo "$INSTALL_DIR/ambivo-mysql-cli"
echo "$INSTALL_DIR/ambivo-db-cli"
echo ""
echo "💡 Tip: Run without arguments for interactive setup"
"""

    script_name = "install.bat" if system == "windows" else "install.sh"
    script_path = os.path.join(output_dir, script_name)

    with open(script_path, "w") as f:
        f.write(install_content)

    if system != "windows":
        os.chmod(script_path, 0o755)


def create_dmg_on_macos(output_dir):
    """Create DMG file on macOS (with fallback methods)."""
    if platform.system().lower() != "darwin":
        return False

    arch = platform.machine().lower()
    if arch in ['x86_64', 'amd64']:
        arch = 'x64'
    elif arch.startswith('arm'):
        arch = 'arm64'

    dmg_name = f"ambivo-db-cli-macos-{arch}.dmg"

    # Method 1: Try create-dmg (professional)
    try:
        subprocess.run(['create-dmg', '--version'], capture_output=True, check=True)

        print("Creating professional macOS DMG package...")

        # Create temporary directory for DMG contents
        dmg_temp = Path("dmg_temp")
        if dmg_temp.exists():
            shutil.rmtree(dmg_temp)
        dmg_temp.mkdir()

        # Copy files to temp directory
        shutil.copy(f"{output_dir}/ambivo-mysql-cli", dmg_temp)
        shutil.copy(f"{output_dir}/ambivo-db-cli", dmg_temp)
        shutil.copy(f"{output_dir}/mysql", dmg_temp)
        shutil.copy(f"{output_dir}/dbcli", dmg_temp)
        shutil.copy(f"{output_dir}/README.txt", dmg_temp)
        shutil.copy(f"{output_dir}/install.sh", dmg_temp)

        # Create Applications symlink (remove if exists)
        apps_link = dmg_temp / "Applications"
        if apps_link.exists():
            apps_link.unlink()
        apps_link.symlink_to("/Applications")

        # Remove existing DMG if it exists
        if os.path.exists(dmg_name):
            os.remove(dmg_name)

        # Create DMG with create-dmg
        cmd = [
            'create-dmg',
            '--volname', 'Ambivo Database CLI Suite',
            '--window-pos', '200', '120',
            '--window-size', '800', '600',
            '--icon-size', '80',
            '--icon', 'ambivo-mysql-cli', '200', '190',
            '--icon', 'ambivo-db-cli', '400', '190',
            '--icon', 'Applications', '600', '190',
            '--hide-extension', 'ambivo-mysql-cli',
            '--hide-extension', 'ambivo-db-cli',
            '--app-drop-link', '600', '190',
            dmg_name,
            str(dmg_temp)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Clean up temp directory
        shutil.rmtree(dmg_temp)

        if result.returncode == 0:
            print(f"✅ Professional DMG created: {dmg_name}")
            return True
        else:
            print(f"⚠️ create-dmg failed: {result.stderr}")
            # Fall through to Method 2

    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ create-dmg not available")
        # Fall through to Method 2

    # Method 2: Simple hdiutil (basic but functional)
    try:
        print("Creating basic macOS DMG package with hdiutil...")

        # Create temporary directory for DMG contents
        dmg_temp = Path("dmg_temp_simple")
        if dmg_temp.exists():
            shutil.rmtree(dmg_temp)
        dmg_temp.mkdir()

        # Copy files to temp directory
        shutil.copy(f"{output_dir}/ambivo-mysql-cli", dmg_temp)
        shutil.copy(f"{output_dir}/ambivo-db-cli", dmg_temp)
        shutil.copy(f"{output_dir}/mysql", dmg_temp)
        shutil.copy(f"{output_dir}/dbcli", dmg_temp)
        shutil.copy(f"{output_dir}/README.txt", dmg_temp)
        shutil.copy(f"{output_dir}/install.sh", dmg_temp)

        # Remove existing DMG if it exists
        if os.path.exists(dmg_name):
            os.remove(dmg_name)

        # Create simple DMG with hdiutil
        cmd = [
            'hdiutil', 'create',
            '-srcfolder', str(dmg_temp),
            '-volname', 'Ambivo Database CLI Suite',
            '-format', 'UDZO',
            dmg_name
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Clean up temp directory
        shutil.rmtree(dmg_temp)

        if result.returncode == 0:
            print(f"✅ Basic DMG created: {dmg_name}")
            return True
        else:
            print(f"❌ hdiutil failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ DMG creation failed: {e}")
        return False


def main():
    """Enhanced main build function."""
    print("🚀 Ambivo Database CLI Suite - Enhanced Binary Builder")
    print("=" * 60)

    # Check for required files
    if not os.path.exists("mysql_cli.py"):
        print("❌ mysql_cli.py not found")
        return 1

    if not os.path.exists("db_cli.py"):
        print("❌ db_cli.py not found")
        return 1

    # Check and install PyInstaller
    if not check_pyinstaller():
        try:
            install_pyinstaller()
        except Exception as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            return 1

    # Create warning suppression hook
    hook_file = create_warning_hook()

    # Create build directories
    try:
        output_dir = create_build_dirs()
        print(f"📁 Output directory: {output_dir}")
    except Exception as e:
        print(f"❌ Failed to create directories: {e}")
        return 1

    # Check for spec files
    mysql_spec_exists, db_spec_exists = check_spec_files()

    # Build binaries (try spec files first, fallback to manual)
    mysql_success = False
    db_success = False

    # MySQL CLI
    if mysql_spec_exists:
        mysql_success = build_mysql_cli_with_spec(output_dir)
        if not mysql_success:
            print("Falling back to manual build for MySQL CLI...")
            mysql_success = build_mysql_cli_manual(output_dir, hook_file)
    else:
        mysql_success = build_mysql_cli_manual(output_dir, hook_file)

    # Multi-Database CLI
    if db_spec_exists:
        db_success = build_db_cli_with_spec(output_dir)
        if not db_success:
            print("Falling back to manual build for Multi-DB CLI...")
            db_success = build_db_cli_manual(output_dir, hook_file)
    else:
        db_success = build_db_cli_manual(output_dir, hook_file)

    if not mysql_success or not db_success:
        print(f"❌ Build failed - MySQL: {mysql_success}, DB: {db_success}")
        return 1

    # Create additional files
    create_convenience_scripts(output_dir)
    create_platform_readme(output_dir)
    create_install_script(output_dir)

    # Create DMG on macOS if possible
    if platform.system().lower() == "darwin":
        create_dmg_on_macos(output_dir)

    print("\n" + "=" * 60)
    print("✅ Build completed successfully!")
    print(f"📦 Binaries available in: {output_dir}")
    print("\nFiles created:")

    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            print(f"  📄 {file} ({size:.1f} MB)")

    print(f"\n🚀 Run install script: {output_dir}/install.*")

    # Platform-specific tips
    system = platform.system().lower()
    if system == "darwin":
        print("🍎 macOS: Look for .dmg file for easy installation")
    elif system == "windows":
        print("🪟 Windows: Run install.bat as administrator for system-wide installation")
    else:
        print("🐧 Linux: Run ./install.sh or add to PATH manually")

    return 0


if __name__ == "__main__":
    sys.exit(main())