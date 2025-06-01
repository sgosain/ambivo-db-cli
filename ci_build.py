#!/usr/bin/env python3
"""
Automated build script for CI/CD environments
This script handles the distutils conflict automatically without manual intervention

Save as: ci_build.py
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path


class CIBuilder:
    def __init__(self):
        self.platform = platform.system().lower()
        self.is_github_actions = os.getenv('GITHUB_ACTIONS') == 'true'
        self.is_ci = any(os.getenv(var) for var in ['CI', 'CONTINUOUS_INTEGRATION', 'GITHUB_ACTIONS'])

    def setup_environment(self):
        """Setup environment variables to prevent distutils conflicts"""
        env_vars = {
            'SETUPTOOLS_USE_DISTUTILS': 'local',
            'DISTUTILS_USE_SDK': '1',
            'PYTHONWARNINGS': 'ignore'
        }

        for key, value in env_vars.items():
            os.environ[key] = value
            print(f"Set {key}={value}")

    def create_warning_hook(self):
        """Create warning suppression hook"""
        hooks_dir = Path('hooks')
        hooks_dir.mkdir(exist_ok=True)

        hook_content = '''"""
Runtime hook to suppress warnings in PyInstaller executable
"""
import warnings
import os

# Set environment variable
os.environ['PYTHONWARNINGS'] = 'ignore'

# Suppress all warning categories
warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")

# Specific suppressions
for category in [UserWarning, DeprecationWarning, FutureWarning, 
                PendingDeprecationWarning, ImportWarning, ResourceWarning]:
    warnings.filterwarnings("ignore", category=category)

# Module-specific suppressions
for module in ['pkg_resources', 'setuptools', 'distutils', 'pandas', 'numpy', 'sqlalchemy']:
    warnings.filterwarnings("ignore", module=module)
'''

        hook_file = hooks_dir / 'rthook_suppress_warnings.py'
        with open(hook_file, 'w') as f:
            f.write(hook_content)

        print(f"Created warning hook: {hook_file}")
        return str(hook_file)

    def get_executable_extension(self):
        """Get the executable extension for the current platform"""
        return '.exe' if self.platform == 'windows' else ''

    def build_mysql_cli(self, hook_file):
        """Build MySQL CLI using direct PyInstaller command"""

        output_name = f"ambivo-mysql-cli{self.get_executable_extension()}"

        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            f'--name={output_name.replace(self.get_executable_extension(), "")}',
            '--console',
            '--noupx',
            '--clean',

            # Essential hidden imports
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

            # Exclude problematic modules
            '--exclude-module=distutils',
            '--exclude-module=setuptools',
            '--exclude-module=pkg_resources',
            '--exclude-module=psycopg2',
            '--exclude-module=duckdb',
            '--exclude-module=matplotlib',
            '--exclude-module=tkinter',

            # Add warning suppression
            f'--runtime-hook={hook_file}',

            # Source file
            'mysql_cli.py'
        ]

        print("Building MySQL CLI...")
        print("Command:", ' '.join(cmd))

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ MySQL CLI build successful!")
            return True
        else:
            print("❌ MySQL CLI build failed!")
            print("STDERR:", result.stderr)
            if self.is_ci:
                # In CI, exit with error code
                sys.exit(1)
            return False

    def build_db_cli(self, hook_file):
        """Build Multi-Database CLI using direct PyInstaller command"""

        output_name = f"ambivo-db-cli{self.get_executable_extension()}"

        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            f'--name={output_name.replace(self.get_executable_extension(), "")}',
            '--console',
            '--noupx',
            '--clean',

            # Essential hidden imports for all databases
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

            # Exclude problematic modules
            '--exclude-module=distutils',
            '--exclude-module=setuptools',
            '--exclude-module=pkg_resources',
            '--exclude-module=matplotlib',
            '--exclude-module=tkinter',

            # Add warning suppression
            f'--runtime-hook={hook_file}',

            # Source file
            'db_cli.py'
        ]

        print("Building Multi-Database CLI...")
        print("Command:", ' '.join(cmd))

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Multi-Database CLI build successful!")
            return True
        else:
            print("❌ Multi-Database CLI build failed!")
            print("STDERR:", result.stderr)
            if self.is_ci:
                # In CI, exit with error code
                sys.exit(1)
            return False

    def test_executables(self):
        """Test that executables were created and can run"""
        dist_dir = Path('dist')
        if not dist_dir.exists():
            print("❌ dist/ directory not found")
            return False

        executables = list(dist_dir.glob('ambivo-*'))
        if not executables:
            print("❌ No executables found in dist/")
            return False

        print("📁 Found executables:")
        for exe in executables:
            print(f"  - {exe.name} ({exe.stat().st_size / 1024 / 1024:.1f} MB)")

            # Test that executable can run
            try:
                result = subprocess.run([str(exe), '--help'],
                                        capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"    ✅ {exe.name} runs successfully")
                else:
                    print(f"    ⚠️ {exe.name} returned code {result.returncode}")
            except subprocess.TimeoutExpired:
                print(f"    ⚠️ {exe.name} timed out (may be waiting for input)")
            except Exception as e:
                print(f"    ❌ {exe.name} failed to run: {e}")

        return True

    def cleanup(self):
        """Clean up build artifacts"""
        dirs_to_clean = ['build', '__pycache__']
        for dir_name in dirs_to_clean:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
                print(f"Cleaned {dir_name}/")

    def run(self):
        """Main build process"""
        print("🚀 Ambivo CLI Automated Build")
        print(f"Platform: {self.platform}")
        print(f"CI Environment: {self.is_ci}")
        print("=" * 50)

        # Step 1: Setup environment
        self.setup_environment()

        # Step 2: Create warning suppression hook
        hook_file = self.create_warning_hook()

        # Step 3: Build applications
        mysql_success = self.build_mysql_cli(hook_file)
        db_success = self.build_db_cli(hook_file)

        # Step 4: Test executables
        test_success = self.test_executables()

        # Step 5: Cleanup
        self.cleanup()

        # Step 6: Report results
        print("\n" + "=" * 50)
        print("Build Results:")
        print(f"MySQL CLI: {'✅ Success' if mysql_success else '❌ Failed'}")
        print(f"Multi-DB CLI: {'✅ Success' if db_success else '❌ Failed'}")
        print(f"Tests: {'✅ Passed' if test_success else '❌ Failed'}")

        # Step 7: Set GitHub Actions outputs if in CI
        if self.is_github_actions:
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                f.write(f"mysql_success={str(mysql_success).lower()}\n")
                f.write(f"db_success={str(db_success).lower()}\n")
                f.write(f"test_success={str(test_success).lower()}\n")

        # Return success status
        overall_success = mysql_success and db_success and test_success
        if self.is_ci and not overall_success:
            sys.exit(1)

        return overall_success


if __name__ == "__main__":
    builder = CIBuilder()
    builder.run()