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


def build_mysql_cli(output_dir):
    """Build mysql_cli.py binary using spec file."""
    print("Building MySQL CLI binary using spec file...")

    cmd = [
        "pyinstaller",
        "specs/mysql_cli.spec",     # 👈 USE SPEC FILE
        "--distpath", output_dir,
        "--workpath", "build/mysql_cli",
        "--clean"
    ]

    subprocess.run(cmd, check=True)
    print(f"✓ MySQL CLI binary created in {output_dir}")


def build_db_cli(output_dir):
    """Build db_cli.py binary using spec file."""
    print("Building Multi-Database CLI binary using spec file...")

    cmd = [
        "pyinstaller",
        "specs/db_cli.spec",        # 👈 USE SPEC FILE
        "--distpath", output_dir,
        "--workpath", "build/db_cli",
        "--clean"
    ]

    subprocess.run(cmd, check=True)
    print(f"✓ Multi-Database CLI binary created in {output_dir}")


def create_batch_files(output_dir):
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

### Examples

```bash
# Import CSV data
./ambivo-mysql-cli -u root -p
mysql> csv_import data.csv users --create-table

# Analytics with DuckDB
./ambivo-db-cli duckdb -f analytics.db
duckdb> CREATE TABLE sales AS SELECT * FROM 'sales_data.csv'
duckdb> SELECT region, SUM(revenue) FROM sales GROUP BY region

# Multi-database workflow
./ambivo-db-cli postgresql -H prod-server -u admin -d warehouse
postgresql> \\dt  # List tables
postgresql> csv_import large_dataset.csv products --chunk-size=5000
```

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
    """Main build function."""
    print("Ambivo Database CLI Suite - Binary Builder")
    print("=" * 50)

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

    # Create build directories
    try:
        output_dir = create_build_dirs()
        print(f"📁 Output directory: {output_dir}")
    except Exception as e:
        print(f"❌ Failed to create directories: {e}")
        return 1

    # Build binaries
    try:
        build_mysql_cli(output_dir)
        build_db_cli(output_dir)
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

    # Create convenience files
    create_batch_files(output_dir)
    create_readme(output_dir)
    create_install_script(output_dir)

    print("\n" + "=" * 50)
    print("✅ Build completed successfully!")
    print(f"📦 Binaries available in: {output_dir}")
    print("\nFiles created:")

    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            print(f"  📄 {file} ({size:.1f} MB)")

    print(f"\n🚀 Run install script: {output_dir}/install.*")
    return 0


if __name__ == "__main__":
    sys.exit(main())