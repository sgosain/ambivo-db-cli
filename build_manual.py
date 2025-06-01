#!/usr/bin/env python3
"""
Ambivo Database CLI Suite - Manual Build Script
Enhanced manual build with better error handling and cross-platform support

Author: Hemant Gosain 'Sunny'
Company: Ambivo
License: MIT
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path


def clean_build():
    """Clean previous builds"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}/")


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


def check_spec_files():
    """Check if spec files exist, if not use manual approach"""
    mysql_spec = Path("specs/mysql_cli.spec")
    db_spec = Path("specs/db_cli.spec")

    return mysql_spec.exists(), db_spec.exists()


def build_mysql_cli_manual(output_dir):
    """Build MySQL CLI with manual PyInstaller command"""
    print("Building MySQL CLI manually...")

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name=ambivo-mysql-cli',
        '--console',
        '--noupx',
        '--clean',
        '--distpath', output_dir,
        '--workpath', 'build/mysql_cli',

        # Hidden imports
        '--hidden-import=mysql.connector',
        '--hidden-import=mysql.connector.cursor',
        '--hidden-import=mysql.connector.errors',
        '--hidden-import=pandas',
        '--hidden-import=pandas.io.sql',
        '--hidden-import=sqlalchemy',
        '--hidden-import=sqlalchemy.dialects.mysql',
        '--hidden-import=tabulate',
        '--hidden-import=readline',

        # Exclude problematic modules
        '--exclude-module=distutils',
        '--exclude-module=setuptools',
        '--exclude-module=pkg_resources',
        '--exclude-module=psycopg2',
        '--exclude-module=duckdb',
        '--exclude-module=matplotlib',
        '--exclude-module=tkinter',

        # Source file
        'mysql_cli.py'
    ]

    # Add runtime hook if it exists
    if os.path.exists('hooks/rthook_suppress_warnings.py'):
        cmd.extend(['--runtime-hook=hooks/rthook_suppress_warnings.py'])

    print("Command:", ' '.join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ MySQL CLI build successful!")
        return True
    else:
        print("❌ MySQL CLI build failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return False


def build_db_cli_manual(output_dir):
    """Build Multi-DB CLI with manual PyInstaller command"""
    print("Building Multi-Database CLI manually...")

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name=ambivo-db-cli',
        '--console',
        '--noupx',
        '--clean',
        '--distpath', output_dir,
        '--workpath', 'build/db_cli',

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
        '--hidden-import=readline',

        # Exclude problematic modules
        '--exclude-module=distutils',
        '--exclude-module=setuptools',
        '--exclude-module=pkg_resources',
        '--exclude-module=matplotlib',
        '--exclude-module=tkinter',

        # Source file
        'db_cli.py'
    ]

    # Add runtime hook if it exists
    if os.path.exists('hooks/rthook_suppress_warnings.py'):
        cmd.extend(['--runtime-hook=hooks/rthook_suppress_warnings.py'])

    print("Command:", ' '.join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Multi-Database CLI build successful!")
        return True
    else:
        print("❌ Multi-Database CLI build failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return False


def build_with_spec_files(output_dir):
    """Build using spec files if available"""
    mysql_spec_exists, db_spec_exists = check_spec_files()

    mysql_success = False
    db_success = False

    if mysql_spec_exists:
        print("Using mysql_cli.spec file...")
        cmd = [
            "pyinstaller",
            "specs/mysql_cli.spec",
            "--distpath", output_dir,
            "--workpath", "build/mysql_cli",
            "--clean"
        ]
        result = subprocess.run(cmd, check=False)
        mysql_success = result.returncode == 0
        if mysql_success:
            print("✅ MySQL CLI built with spec file")
        else:
            print("❌ MySQL CLI spec build failed, trying manual...")
            mysql_success = build_mysql_cli_manual(output_dir)
    else:
        mysql_success = build_mysql_cli_manual(output_dir)

    if db_spec_exists:
        print("Using db_cli.spec file...")
        cmd = [
            "pyinstaller",
            "specs/db_cli.spec",
            "--distpath", output_dir,
            "--workpath", "build/db_cli",
            "--clean"
        ]
        result = subprocess.run(cmd, check=False)
        db_success = result.returncode == 0
        if db_success:
            print("✅ Multi-DB CLI built with spec file")
        else:
            print("❌ Multi-DB CLI spec build failed, trying manual...")
            db_success = build_db_cli_manual(output_dir)
    else:
        db_success = build_db_cli_manual(output_dir)

    return mysql_success, db_success


def create_convenience_scripts(output_dir):
    """Create convenience batch/shell files."""
    system = platform.system().lower()

    if system == "windows":
        # Windows batch files
        mysql_batch = f"""@echo off
"{os.path.join(output_dir, 'ambivo-mysql-cli.exe')}" %*
"""
        db_batch = f"""@echo off
"{os.path.join(output_dir, 'ambivo-db-cli.exe')}" %*
"""

        with open(os.path.join(output_dir, "mysql.bat"), "w") as f:
            f.write(mysql_batch)
        with open(os.path.join(output_dir, "dbcli.bat"), "w") as f:
            f.write(db_batch)

    else:
        # Unix shell scripts
        mysql_shell = f"""#!/bin/bash
"{os.path.join(output_dir, 'ambivo-mysql-cli')}" "$@"
"""
        db_shell = f"""#!/bin/bash
"{os.path.join(output_dir, 'ambivo-db-cli')}" "$@"
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


def create_readme(output_dir):
    """Create README for binary distribution."""
    system = platform.system().lower()
    arch = platform.machine().lower()

    if arch in ['x86_64', 'amd64']:
        arch = 'x64'
    elif arch in ['i386', 'i686']:
        arch = 'x86'
    elif arch.startswith('arm'):
        arch = 'arm64' if '64' in arch else 'arm'

    readme_content = f"""# Ambivo Database CLI Suite - Binary Distribution

## Platform: {system.title()} {arch.upper()}

### Included Binaries

1. **ambivo-mysql-cli** - Dedicated MySQL CLI client
2. **ambivo-db-cli** - Universal multi-database CLI client

### Quick Start

#### MySQL CLI
```bash
# Connect to MySQL
./ambivo-mysql-cli -H localhost -u root -p

# Execute single query  
./ambivo-mysql-cli -u root -p "SHOW DATABASES"

# Convenience wrapper
./mysql -H localhost -u root -p
```

#### Multi-Database CLI
```bash
# MySQL (default)
./ambivo-db-cli -H localhost -u root -p -d mydb

# PostgreSQL
./ambivo-db-cli postgresql -H localhost -u postgres -p -d mydb

# SQLite
./ambivo-db-cli sqlite -f database.db

# DuckDB (Analytics)
./ambivo-db-cli duckdb -f analytics.db

# Convenience wrapper
./dbcli postgresql -H localhost -u postgres -p -d mydb
```

### Features

- ✅ Standalone executables (no Python installation required)
- ✅ Full database connectivity (MySQL, PostgreSQL, SQLite, DuckDB) 
- ✅ CSV import capabilities with intelligent mapping
- ✅ Command history and tab completion
- ✅ Professional table formatting
- ✅ Cross-platform compatibility

### System Requirements

- **{system.title()}** {arch.upper()}
- No additional dependencies required

### Installation

1. Extract binaries to desired location
2. Add to PATH for global access (optional)
3. Run directly from current directory

### Support

- 📧 Email: sgosain@ambivo.com
- 🏢 Company: https://www.ambivo.com
- 🐛 Issues: https://github.com/sgosain/ambivo-db-cli/issues

Built with ❤️ by Hemant Gosain 'Sunny' at Ambivo
"""

    with open(os.path.join(output_dir, "README.txt"), "w") as f:
        f.write(readme_content)


def create_install_script(output_dir):
    """Create installation script."""
    system = platform.system().lower()

    if system == "windows":
        install_content = f"""@echo off
echo Installing Ambivo Database CLI Suite...

set "INSTALL_DIR=%USERPROFILE%\\ambivo-cli"
mkdir "%INSTALL_DIR%" 2>nul

copy "ambivo-mysql-cli.exe" "%INSTALL_DIR%\\" >nul
copy "ambivo-db-cli.exe" "%INSTALL_DIR%\\" >nul
copy "mysql.bat" "%INSTALL_DIR%\\" >nul  
copy "dbcli.bat" "%INSTALL_DIR%\\" >nul
copy "README.txt" "%INSTALL_DIR%\\" >nul

echo.
echo ✓ Installed to: %INSTALL_DIR%
echo.
echo To use globally, add this to your PATH:
echo %INSTALL_DIR%
echo.
echo Quick test:
echo "%INSTALL_DIR%\\ambivo-mysql-cli.exe" --help
echo "%INSTALL_DIR%\\ambivo-db-cli.exe" --help
echo.
pause
"""
    else:
        install_content = f"""#!/bin/bash
echo "Installing Ambivo Database CLI Suite..."

INSTALL_DIR="$HOME/bin"
mkdir -p "$INSTALL_DIR"

cp ambivo-mysql-cli "$INSTALL_DIR/"
cp ambivo-db-cli "$INSTALL_DIR/"
cp mysql "$INSTALL_DIR/"
cp dbcli "$INSTALL_DIR/"
cp README.txt "$INSTALL_DIR/"

chmod +x "$INSTALL_DIR/ambivo-mysql-cli"
chmod +x "$INSTALL_DIR/ambivo-db-cli"
chmod +x "$INSTALL_DIR/mysql"
chmod +x "$INSTALL_DIR/dbcli"

echo
echo "✓ Installed to: $INSTALL_DIR"
echo
echo "To use globally, add this to your PATH:"
echo "export PATH=\\$PATH:$INSTALL_DIR"
echo "Add the above line to ~/.bashrc or ~/.zshrc"
echo
echo "Quick test:"
echo "$INSTALL_DIR/ambivo-mysql-cli --help"
echo "$INSTALL_DIR/ambivo-db-cli --help"
echo
"""

    script_name = "install.bat" if system == "windows" else "install.sh"
    script_path = os.path.join(output_dir, script_name)

    with open(script_path, "w") as f:
        f.write(install_content)

    if system != "windows":
        os.chmod(script_path, 0o755)


def main():
    """Main build function with enhanced logic."""
    print("🚀 Ambivo Database CLI Suite - Enhanced Manual Build")
    print("=" * 60)

    # Check for required files
    if not os.path.exists("mysql_cli.py"):
        print("❌ mysql_cli.py not found")
        return 1

    if not os.path.exists("db_cli.py"):
        print("❌ db_cli.py not found")
        return 1

    # Check PyInstaller
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed")
        except Exception as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            return 1

    # Clean and create directories
    try:
        clean_build()
        output_dir = create_build_dirs()
        print(f"📁 Output directory: {output_dir}")
    except Exception as e:
        print(f"❌ Failed to create directories: {e}")
        return 1

    # Check spec files availability
    mysql_spec_exists, db_spec_exists = check_spec_files()
    if mysql_spec_exists:
        print("✓ MySQL spec file found")
    if db_spec_exists:
        print("✓ DB CLI spec file found")

    # Build binaries
    try:
        mysql_success, db_success = build_with_spec_files(output_dir)
    except Exception as e:
        print(f"❌ Build failed: {e}")
        return 1

    # Create additional files if builds successful
    if mysql_success or db_success:
        create_convenience_scripts(output_dir)
        create_readme(output_dir)
        create_install_script(output_dir)

        print("\n" + "=" * 60)
        print("📦 Build Summary:")
        print(f"MySQL CLI: {'✅ Success' if mysql_success else '❌ Failed'}")
        print(f"Multi-DB CLI: {'✅ Success' if db_success else '❌ Failed'}")
        print(f"📁 Output: {output_dir}")

        # List created files
        print("\nFiles created:")
        try:
            for file in os.listdir(output_dir):
                file_path = os.path.join(output_dir, file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                    print(f"  📄 {file} ({size:.1f} MB)")
        except Exception as e:
            print(f"Error listing files: {e}")

        print(f"\n🚀 Run installer: {output_dir}/install.*")
        return 0 if (mysql_success and db_success) else 1
    else:
        print("\n❌ All builds failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())