#!/usr/bin/env python3
"""
Ambivo Multi-Database CLI - Universal Database Client

This universal database CLI client provides seamless connectivity and management
across multiple database engines with modern enhancements for enterprise use.
Built by the Ambivo team to deliver superior multi-database administration experience.

Features:
- Universal database connectivity (MySQL, PostgreSQL, SQLite, DuckDB)
- Enhanced interactive mode with beautiful table formatting
- Command history and tab completion with readline support
- Intelligent CSV import with automatic column mapping and type inference
- URL CSV import with aria2 high-speed downloads
- Simple data visualization (line, bar, scatter, histogram charts)
- Database-agnostic SQL execution with engine-specific optimizations
- Cross-platform compatibility and consistent user experience
- Professional-grade error handling and user guidance
- Intelligent table creation from CSV structure analysis

Supported Databases:
- MySQL: Production web applications and OLTP workloads
- PostgreSQL: Enterprise applications and complex queries
- SQLite: Embedded applications, testing, and development
- DuckDB: Analytics, data science, and OLAP workloads

Author: Hemant Gosain 'Sunny'
Company: Ambivo
Email: sgosain@ambivo.com
License: MIT Open Source License

Copyright (c) 2025 Hemant Gosain / Ambivo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

GitHub: https://github.com/sgosain/ambivo-db-cli
Company: https://www.ambivo.com
"""

__author__ = "Hemant Gosain 'Sunny'"
__copyright__ = "Copyright (c) 2025 Hemant Gosain / Ambivo"
__license__ = "MIT"
__version__ = "2.1.0"
__maintainer__ = "Hemant Gosain 'Sunny'"
__email__ = "sgosain@ambivo.com"
__status__ = "Production"
__company__ = "Ambivo"

import os
import sys
import warnings
import platform

# Environment variable suppression
os.environ['PYTHONWARNINGS'] = 'ignore'

# Comprehensive warning suppression
warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")

# Specific suppressions
for category in [UserWarning, DeprecationWarning, FutureWarning,
                 PendingDeprecationWarning, ImportWarning, ResourceWarning]:
    warnings.filterwarnings("ignore", category=category)

import argparse
import textwrap
import getpass
import sqlite3
import tempfile
import subprocess
import time
import shutil
import logging
from urllib.parse import urlparse, unquote
from tabulate import tabulate
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
from datetime import datetime

# Add visualization support
MATPLOTLIB_SUPPORT = False
try:
    import matplotlib

    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    MATPLOTLIB_SUPPORT = True
except ImportError:
    MATPLOTLIB_SUPPORT = False

def get_platform_specific_aria2_check():
    """Get platform-specific aria2 availability check."""
    system = platform.system().lower()

    if system == "windows":
        # Check multiple possible locations on Windows
        possible_paths = [
            "aria2c.exe",  # If in PATH
            "C:\\aria2\\aria2c.exe",  # Common manual install location
            "C:\\Program Files\\aria2\\aria2c.exe",
            "C:\\Program Files (x86)\\aria2\\aria2c.exe"
        ]

        for path in possible_paths:
            try:
                result = subprocess.run([path, '--version'],
                                        capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return True
            except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        return False
    else:
        # Unix-like systems (Linux, macOS)
        try:
            result = subprocess.run(['aria2c', '--version'],
                                    capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
# Add aria2 detection
ARIA2_SUPPORT = get_platform_specific_aria2_check()

# Command history and readline support
try:
    import readline
    import atexit

    READLINE_SUPPORT = True
except ImportError:
    READLINE_SUPPORT = False

# CSV functionality - FIXED: Import pandas properly with error handling
CSV_SUPPORT = False
pd = None  # Initialize to None
create_engine = None

try:
    import pandas as pd
    from sqlalchemy import create_engine

    CSV_SUPPORT = True
except ImportError:
    # Create dummy objects if packages not available
    class DummyPandas:
        def read_csv(self, *args, **kwargs):
            raise ImportError("pandas not available - install with: pip install pandas")

        @property
        def DataFrame(self):
            raise ImportError("pandas not available - install with: pip install pandas")


    class DummySQLAlchemy:
        def __call__(self, *args, **kwargs):
            raise ImportError("sqlalchemy not available - install with: pip install sqlalchemy")


    pd = DummyPandas()
    create_engine = DummySQLAlchemy()
    CSV_SUPPORT = False

# Optional database support
try:
    import mysql.connector

    MYSQL_SUPPORT = True
except ImportError:
    MYSQL_SUPPORT = False

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor

    POSTGRESQL_SUPPORT = True
except ImportError:
    POSTGRESQL_SUPPORT = False

try:
    import duckdb

    DUCKDB_SUPPORT = True
except ImportError:
    DUCKDB_SUPPORT = False


def print_license():
    """Print the full license information."""
    print(f"""
MIT License - Ambivo Multi-Database CLI

{__copyright__}
Company: {__company__}
Website: https://www.ambivo.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

GitHub Repository: https://github.com/sgosain/ambivo-db-cli
Report Issues: https://github.com/sgosain/ambivo-db-cli/issues
Ambivo: https://www.ambivo.com
""")


class DatabaseAdapter(ABC):
    """Abstract base class for database adapters."""

    @abstractmethod
    def connect(self) -> Dict:
        pass

    @abstractmethod
    def execute(self, sql: str, parameters: Optional[List] = None) -> Dict:
        pass

    @abstractmethod
    def get_databases(self) -> Dict:
        pass

    @abstractmethod
    def get_tables(self) -> Dict:
        pass

    @abstractmethod
    def get_table_columns(self, table_name: str) -> Dict:
        pass

    @abstractmethod
    def create_sqlalchemy_engine(self) -> str:
        pass

    @abstractmethod
    def get_column_type_mapping(self) -> Dict:
        pass


class MySQLAdapter(DatabaseAdapter):
    """MySQL database adapter."""

    def __init__(self, host='localhost', port=3306, user='root', password=None,
                 database=None, ssl_disabled=False, timeout=30, charset='utf8mb4'):
        if not MYSQL_SUPPORT:
            raise ImportError("MySQL support requires: pip install mysql-connector-python")

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.ssl_disabled = ssl_disabled
        self.timeout = timeout
        self.charset = charset
        self.connection = None
        self.current_database = database

    def connect(self) -> Dict:
        try:
            config = {
                'host': self.host,
                'port': self.port,
                'user': self.user,
                'password': self.password,
                'autocommit': True,
                'connection_timeout': self.timeout,
                'charset': self.charset,
                'use_unicode': True,
                'use_pure': True  # Force pure Python
            }

            if self.database:
                config['database'] = self.database

            if self.ssl_disabled:
                config['ssl_disabled'] = True

            # Try connection with pure Python first
            try:
                self.connection = mysql.connector.connect(**config)
                return {"success": True, "message": "Connected successfully"}
            except mysql.connector.Error as e:
                # If pure Python fails, try without use_pure (fallback)
                config.pop('use_pure', None)
                self.connection = mysql.connector.connect(**config)
                return {"success": True, "message": "Connected successfully"}

        except mysql.connector.Error as e:
            return {"success": False, "error": f"MySQL Error: {e}"}
        except Exception as e:
            return {"success": False, "error": f"Connection Error: {e}"}

    def execute(self, sql: str, parameters: Optional[List] = None) -> Dict:
        if not self.connection:
            connect_result = self.connect()
            if not connect_result.get('success'):
                return connect_result

        try:
            cursor = self.connection.cursor()

            if parameters:
                cursor.execute(sql, parameters)
            else:
                cursor.execute(sql)

            sql_upper = sql.strip().upper()

            if sql_upper.startswith(('SELECT', 'SHOW', 'DESCRIBE', 'DESC', 'EXPLAIN', 'HELP')):
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                data = cursor.fetchall()
                cursor.close()
                return {
                    "success": True,
                    "data": list(data),
                    "columns": columns,
                    "row_count": len(data)
                }
            elif sql_upper.startswith('USE '):
                cursor.close()
                self.current_database = sql.split()[1].strip('`;')
                return {
                    "success": True,
                    "message": f"Database changed to '{self.current_database}'"
                }
            else:
                affected_rows = cursor.rowcount
                cursor.close()
                return {
                    "success": True,
                    "message": f"Query OK, {affected_rows} row(s) affected",
                    "affected_rows": affected_rows
                }

        except mysql.connector.Error as e:
            return {"success": False, "error": f"MySQL Error {e.errno}: {e.msg}"}
        except Exception as e:
            return {"success": False, "error": f"Execution Error: {e}"}

    def get_databases(self) -> Dict:
        query = """
                SELECT schema_name as 'Database', ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as 'Size (MB)'
                FROM information_schema.tables
                WHERE schema_name NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys')
                GROUP BY schema_name
                ORDER BY schema_name"""
        result = self.execute(query)
        if result.get('success'):
            return result
        else:
            return self.execute("SHOW DATABASES")

    def get_tables(self) -> Dict:
        query = """
                SELECT table_name as 'Table', table_type as 'Type', engine as 'Engine', table_rows as 'Rows'
                FROM information_schema.tables
                WHERE table_schema = DATABASE()
                ORDER BY table_name"""
        result = self.execute(query)
        if result.get('success'):
            return result
        else:
            return self.execute("SHOW TABLES")

    def get_table_columns(self, table_name: str) -> Dict:
        query = f"SHOW COLUMNS FROM {table_name}"
        result = self.execute(query)

        if result.get('success'):
            columns = [row[0] for row in result['data']]
            return {"success": True, "columns": columns}
        else:
            return result

    def create_sqlalchemy_engine(self) -> str:
        return (f"mysql+mysqlconnector://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.current_database}")

    def get_column_type_mapping(self) -> Dict:
        return {
            'int_small': 'TINYINT',
            'int_medium': 'SMALLINT',
            'int_large': 'INT',
            'int_xlarge': 'BIGINT',
            'float': 'DECIMAL(10,2)',
            'bool': 'BOOLEAN',
            'string_small': 'VARCHAR(50)',
            'string_medium': 'VARCHAR(255)',
            'string_large': 'VARCHAR(1000)',
            'text': 'TEXT',
            'auto_increment_pk': 'INT AUTO_INCREMENT PRIMARY KEY'
        }

    def close(self):
        if self.connection:
            self.connection.close()


class PostgreSQLAdapter(DatabaseAdapter):
    """PostgreSQL database adapter."""

    def __init__(self, host='localhost', port=5432, user='postgres', password=None,
                 database='postgres', **kwargs):
        if not POSTGRESQL_SUPPORT:
            raise ImportError("PostgreSQL support requires: pip install psycopg2-binary")

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.current_database = database

    def connect(self) -> Dict:
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                cursor_factory=RealDictCursor
            )
            self.connection.autocommit = True
            return {"success": True, "message": "Connected successfully"}

        except psycopg2.Error as e:
            return {"success": False, "error": f"PostgreSQL Error: {e}"}
        except Exception as e:
            return {"success": False, "error": f"Connection Error: {e}"}

    def execute(self, sql: str, parameters: Optional[List] = None) -> Dict:
        if not self.connection:
            connect_result = self.connect()
            if not connect_result.get('success'):
                return connect_result

        try:
            cursor = self.connection.cursor()

            if parameters:
                cursor.execute(sql, parameters)
            else:
                cursor.execute(sql)

            sql_upper = sql.strip().upper()

            if sql_upper.startswith(('SELECT', 'SHOW', 'EXPLAIN', 'WITH')):
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                data = cursor.fetchall()
                # Convert psycopg2.extras.RealDictRow to tuples
                data = [tuple(row.values()) if hasattr(row, 'values') else tuple(row) for row in data]
                return {
                    "success": True,
                    "data": data,
                    "columns": columns,
                    "row_count": len(data)
                }
            elif sql_upper.startswith('\\C ') or sql_upper.startswith('\\CONNECT'):
                # Handle database switching (PostgreSQL style)
                db_name = sql.split()[1].strip()
                cursor.close()
                # Would need to reconnect with new database
                return {"success": True, "message": f"Database changed to '{db_name}'"}
            else:
                affected_rows = cursor.rowcount
                return {
                    "success": True,
                    "message": f"Query OK, {affected_rows} row(s) affected",
                    "affected_rows": affected_rows
                }

        except psycopg2.Error as e:
            return {"success": False, "error": f"PostgreSQL Error: {e}"}
        except Exception as e:
            return {"success": False, "error": f"Execution Error: {e}"}

    def get_databases(self) -> Dict:
        query = """
                SELECT datname                                   as "Database",
                       pg_size_pretty(pg_database_size(datname)) as "Size"
                FROM pg_database
                WHERE datistemplate = false
                ORDER BY datname"""
        return self.execute(query)

    def get_tables(self) -> Dict:
        query = """
                SELECT table_name   as "Table",
                       table_type   as "Type",
                       'postgresql' as "Engine",
                       'N/A'        as "Rows"
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name"""
        return self.execute(query)

    def get_table_columns(self, table_name: str) -> Dict:
        query = """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = %s
                  AND table_schema = 'public'
                ORDER BY ordinal_position"""
        result = self.execute(query, [table_name])

        if result.get('success'):
            columns = [row[0] for row in result['data']]
            return {"success": True, "columns": columns}
        else:
            return result

    def create_sqlalchemy_engine(self) -> str:
        return (f"postgresql+psycopg2://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.current_database}")

    def get_column_type_mapping(self) -> Dict:
        return {
            'int_small': 'SMALLINT',
            'int_medium': 'INTEGER',
            'int_large': 'INTEGER',
            'int_xlarge': 'BIGINT',
            'float': 'DECIMAL(10,2)',
            'bool': 'BOOLEAN',
            'string_small': 'VARCHAR(50)',
            'string_medium': 'VARCHAR(255)',
            'string_large': 'VARCHAR(1000)',
            'text': 'TEXT',
            'auto_increment_pk': 'SERIAL PRIMARY KEY'
        }

    def close(self):
        if self.connection:
            self.connection.close()


class DuckDBAdapter(DatabaseAdapter):
    """DuckDB database adapter - Perfect for analytics!"""

    def __init__(self, database_path=':memory:', **kwargs):
        if not DUCKDB_SUPPORT:
            raise ImportError("DuckDB support requires: pip install duckdb")

        self.database_path = database_path
        self.connection = None
        self.current_database = os.path.basename(database_path) if database_path != ':memory:' else 'memory'

    def connect(self) -> Dict:
        try:
            if self.database_path == ':memory:':
                self.connection = duckdb.connect()
            else:
                self.connection = duckdb.connect(self.database_path)
            return {"success": True, "message": "Connected successfully"}
        except Exception as e:
            return {"success": False, "error": f"DuckDB Error: {e}"}

    def execute(self, sql: str, parameters: Optional[List] = None) -> Dict:
        if not self.connection:
            connect_result = self.connect()
            if not connect_result.get('success'):
                return connect_result

        try:
            if parameters:
                result = self.connection.execute(sql, parameters)
            else:
                result = self.connection.execute(sql)

            sql_upper = sql.strip().upper()

            if sql_upper.startswith(('SELECT', 'SHOW', 'DESCRIBE', 'DESC', 'EXPLAIN', 'WITH', 'PRAGMA')):
                # DuckDB returns result object
                data = result.fetchall()
                columns = [desc[0] for desc in result.description] if result.description else []
                return {
                    "success": True,
                    "data": data,
                    "columns": columns,
                    "row_count": len(data)
                }
            else:
                # For DML operations, get affected rows
                return {
                    "success": True,
                    "message": "Query executed successfully",
                    "affected_rows": 0  # DuckDB doesn't easily expose this
                }

        except Exception as e:
            return {"success": False, "error": f"DuckDB Error: {e}"}

    def get_databases(self) -> Dict:
        # DuckDB can attach multiple databases
        query = "SHOW DATABASES"
        result = self.execute(query)
        if result.get('success'):
            return result
        else:
            # Fallback - show current database
            return {
                "success": True,
                "data": [(self.current_database, "N/A")],
                "columns": ["Database", "Size"],
                "row_count": 1
            }

    def get_tables(self) -> Dict:
        query = "SHOW TABLES"
        result = self.execute(query)
        if result.get('success'):
            # DuckDB SHOW TABLES just returns table names
            tables_data = []
            for row in result['data']:
                table_name = row[0] if isinstance(row, (list, tuple)) else row
                tables_data.append((table_name, 'BASE TABLE', 'duckdb', 'N/A'))

            return {
                "success": True,
                "data": tables_data,
                "columns": ["Table", "Type", "Engine", "Rows"],
                "row_count": len(tables_data)
            }
        else:
            return result

    def get_table_columns(self, table_name: str) -> Dict:
        query = f"DESCRIBE {table_name}"
        result = self.execute(query)

        if result.get('success'):
            # DuckDB DESCRIBE returns: column_name, column_type, null, key, default, extra
            columns = [row[0] for row in result['data']]
            return {"success": True, "columns": columns}
        else:
            return result

    def create_sqlalchemy_engine(self) -> str:
        return f"duckdb:///{self.database_path}"

    def get_column_type_mapping(self) -> Dict:
        return {
            'int_small': 'TINYINT',
            'int_medium': 'SMALLINT',
            'int_large': 'INTEGER',
            'int_xlarge': 'BIGINT',
            'float': 'DOUBLE',
            'bool': 'BOOLEAN',
            'string_small': 'VARCHAR',
            'string_medium': 'VARCHAR',
            'string_large': 'VARCHAR',
            'text': 'VARCHAR',
            'auto_increment_pk': 'INTEGER PRIMARY KEY'  # DuckDB doesn't have AUTO_INCREMENT
        }

    def close(self):
        if self.connection:
            self.connection.close()


class SQLiteAdapter(DatabaseAdapter):
    """SQLite database adapter."""

    def __init__(self, database_path=':memory:', **kwargs):
        self.database_path = database_path
        self.connection = None
        self.current_database = os.path.basename(database_path) if database_path != ':memory:' else 'memory'

    def connect(self) -> Dict:
        try:
            self.connection = sqlite3.connect(self.database_path)
            self.connection.row_factory = sqlite3.Row
            return {"success": True, "message": "Connected successfully"}
        except Exception as e:
            return {"success": False, "error": f"SQLite Error: {e}"}

    def execute(self, sql: str, parameters: Optional[List] = None) -> Dict:
        if not self.connection:
            connect_result = self.connect()
            if not connect_result.get('success'):
                return connect_result

        try:
            cursor = self.connection.cursor()

            if parameters:
                cursor.execute(sql, parameters)
            else:
                cursor.execute(sql)

            sql_upper = sql.strip().upper()

            if sql_upper.startswith(('SELECT', 'PRAGMA')):
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                data = cursor.fetchall()
                data = [tuple(row) for row in data]
                return {
                    "success": True,
                    "data": data,
                    "columns": columns,
                    "row_count": len(data)
                }
            else:
                affected_rows = cursor.rowcount
                self.connection.commit()
                return {
                    "success": True,
                    "message": f"Query OK, {affected_rows} row(s) affected",
                    "affected_rows": affected_rows
                }

        except Exception as e:
            return {"success": False, "error": f"SQLite Error: {e}"}

    def get_databases(self) -> Dict:
        return {
            "success": True,
            "data": [(self.current_database, "N/A")],
            "columns": ["Database", "Size"],
            "row_count": 1
        }

    def get_tables(self) -> Dict:
        query = """
                SELECT name as 'Table', type as 'Type', 'sqlite' as 'Engine', 'N/A' as 'Rows'
                FROM sqlite_master
                WHERE type = 'table'
                  AND name NOT LIKE 'sqlite_%'
                ORDER BY name"""
        return self.execute(query)

    def get_table_columns(self, table_name: str) -> Dict:
        query = f"PRAGMA table_info({table_name})"
        result = self.execute(query)

        if result.get('success'):
            columns = [row[1] for row in result['data']]
            return {"success": True, "columns": columns}
        else:
            return result

    def create_sqlalchemy_engine(self) -> str:
        return f"sqlite:///{self.database_path}"

    def get_column_type_mapping(self) -> Dict:
        return {
            'int_small': 'INTEGER',
            'int_medium': 'INTEGER',
            'int_large': 'INTEGER',
            'int_xlarge': 'INTEGER',
            'float': 'REAL',
            'bool': 'INTEGER',
            'string_small': 'TEXT',
            'string_medium': 'TEXT',
            'string_large': 'TEXT',
            'text': 'TEXT',
            'auto_increment_pk': 'INTEGER PRIMARY KEY AUTOINCREMENT'
        }

    def close(self):
        if self.connection:
            self.connection.close()


class MultiDatabaseClient:
    """Enhanced database client supporting multiple database engines."""

    def __init__(self, db_type='mysql', **kwargs):
        self.db_type = db_type

        if db_type == 'mysql':
            self.adapter = MySQLAdapter(**kwargs)
        elif db_type == 'postgresql':
            self.adapter = PostgreSQLAdapter(**kwargs)
        elif db_type == 'sqlite':
            self.adapter = SQLiteAdapter(**kwargs)
        elif db_type == 'duckdb':
            self.adapter = DuckDBAdapter(**kwargs)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

        # Set up logging for downloads
        self.logger = logging.getLogger(__name__)

    def connect(self):
        return self.adapter.connect()

    def execute(self, sql: str, parameters: Optional[List] = None):
        return self.adapter.execute(sql, parameters)

    def get_databases(self):
        return self.adapter.get_databases()

    def get_tables(self):
        return self.adapter.get_tables()

    def get_table_columns(self, table_name: str):
        return self.adapter.get_table_columns(table_name)

    def _download_with_aria2(self, url, output_dir=None, filename=None, connections=16):
        """
        Download a file using aria2c with optimized settings for maximum speed.
        """
        if not ARIA2_SUPPORT:
            return {
                "success": False,
                "error": "aria2c not found. Please install aria2: sudo apt-get install aria2 (Ubuntu) or brew install aria2 (Mac)"
            }

        start_time = time.time()

        # Create output directory if it doesn't exist
        if not output_dir:
            output_dir = tempfile.mkdtemp(prefix="duckdb_downloads_")
        os.makedirs(output_dir, exist_ok=True)

        # Generate fallback filename from URL if not provided
        def extract_filename_from_url(url):
            """Extract filename from URL with multiple fallback strategies."""
            try:
                parsed_url = urlparse(url)
                path = unquote(parsed_url.path)

                if path and '/' in path:
                    filename = path.split('/')[-1]
                    if filename and '.' in filename:
                        return filename

                if parsed_url.query:
                    for param in parsed_url.query.split('&'):
                        if 'filename=' in param.lower():
                            return param.split('=', 1)[1]

                domain = parsed_url.netloc.replace('.', '_')
                timestamp = str(int(time.time()))
                return f"download_{domain}_{timestamp}.csv"

            except Exception:
                return f"download_{int(time.time())}.csv"

        if not filename:
            filename = extract_filename_from_url(url)

        if '.' not in filename:
            filename += '.csv'

        # Get list of files before download
        files_before = {}
        try:
            for f in os.listdir(output_dir):
                filepath = os.path.join(output_dir, f)
                if os.path.isfile(filepath):
                    files_before[f] = os.path.getmtime(filepath)
        except OSError:
            files_before = {}

        # Build aria2 command
        cmd = [
            'aria2c',
            url,
            f'--dir={output_dir}',
            f'--out={filename}',
            f'--max-connection-per-server={connections}',
            '--split=16',
            '--min-split-size=1M',
            '--file-allocation=none',
            '--continue=true',
            '--timeout=17',
            '--summary-interval=0',
            '--console-log-level=info',
            '--follow-metalink=true',
            '--check-certificate=false',
            '--max-tries=5',
            '--retry-wait=2',
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '--allow-overwrite=true',
            '--auto-file-renaming=false'
        ]

        try:
            self.logger.info(f"Starting aria2 download for {url} -> {filename}")
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                return {
                    "success": False,
                    "error": f"Download failed with code {result.returncode}: {result.stderr}",
                    "url": url
                }

            # Find the downloaded file (using multiple strategies)
            actual_filename = None

            # Strategy 1: Check specified filename
            if os.path.exists(os.path.join(output_dir, filename)):
                actual_filename = filename

            # Strategy 2: Look for new files
            if not actual_filename:
                try:
                    for f in os.listdir(output_dir):
                        test_path = os.path.join(output_dir, f)
                        if os.path.isfile(test_path):
                            mtime = os.path.getmtime(test_path)
                            if f not in files_before or mtime > files_before.get(f, 0):
                                actual_filename = f
                                break
                except OSError:
                    pass

            if not actual_filename:
                return {
                    "success": False,
                    "error": f"Download completed but couldn't find file in {output_dir}",
                    "url": url
                }

            filepath = os.path.join(output_dir, actual_filename)

            if not os.path.exists(filepath):
                return {
                    "success": False,
                    "error": f"Downloaded file not found at {filepath}",
                    "url": url
                }

            # Calculate statistics
            file_size = os.path.getsize(filepath)
            download_time = time.time() - start_time
            download_speed_MBps = (file_size / (1024 * 1024)) / download_time if download_time > 0 else 0

            return {
                "success": True,
                "filepath": filepath,
                "filename": actual_filename,
                "file_size": file_size,
                "file_size_MB": round(file_size / (1024 * 1024), 2),
                "download_speed_MBps": round(download_speed_MBps, 2),
                "download_time": download_time,
                "url": url,
                "temp_dir": output_dir
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url
            }

    def import_csv_from_url(self, url, table_name, column_mapping=None,
                            chunk_size=1000, interactive=True, create_table=False,
                            connections=16, cleanup_temp=True):
        """
        Import CSV data directly from a URL using aria2 for download.

        Args:
            url (str): URL of the CSV file
            table_name (str): Target table name
            column_mapping (dict, optional): CSV to table column mapping
            chunk_size (int): Rows per chunk for import
            interactive (bool): Show progress and prompts
            create_table (bool): Auto-create table if it doesn't exist
            connections (int): Number of aria2 connections
            cleanup_temp (bool): Remove temporary files after import

        Returns:
            dict: Import result with statistics
        """
        if interactive:
            print(f"🌐 Downloading CSV from URL: {url}")

        # Download the file
        download_result = self._download_with_aria2(url, connections=connections)

        if not download_result.get('success'):
            return download_result

        if interactive:
            print(f"✓ Downloaded {download_result['file_size_MB']} MB in {download_result['download_time']:.1f}s "
                  f"({download_result['download_speed_MBps']:.1f} MB/s)")

        try:
            # Import the downloaded CSV
            import_result = self.import_csv_to_table(
                csv_path=download_result['filepath'],
                table_name=table_name,
                column_mapping=column_mapping,
                chunk_size=chunk_size,
                interactive=interactive,
                create_table=create_table
            )

            # Add download info to result
            if import_result.get('success'):
                import_result['download_info'] = {
                    'url': url,
                    'file_size_MB': download_result['file_size_MB'],
                    'download_time': download_result['download_time'],
                    'download_speed_MBps': download_result['download_speed_MBps']
                }

            return import_result

        finally:
            # Cleanup temporary files if requested
            if cleanup_temp and 'temp_dir' in download_result:
                try:
                    shutil.rmtree(download_result['temp_dir'])
                    if interactive:
                        print("🗑️  Cleaned up temporary files")
                except Exception as e:
                    if interactive:
                        print(f"⚠️  Warning: Could not clean up temp files: {e}")

    def create_chart(self, query, chart_type='line', x_column=None, y_column=None,
                     title=None, output_file=None, show_plot=True, figsize=(10, 6)):
        """
        Create simple charts from SQL query results.

        Args:
            query (str): SQL query to execute
            chart_type (str): 'line', 'bar', 'scatter', 'hist'
            x_column (str): X-axis column name (auto-detected if None)
            y_column (str): Y-axis column name (auto-detected if None)
            title (str): Chart title
            output_file (str): Save chart to file (PNG)
            show_plot (bool): Display plot (if display available)
            figsize (tuple): Figure size (width, height)

        Returns:
            dict: Chart creation result
        """
        if not MATPLOTLIB_SUPPORT:
            return {
                "success": False,
                "error": "Visualization requires matplotlib. Install with: pip install matplotlib"
            }

        # Execute the query
        result = self.execute(query)
        if not result.get('success'):
            return {
                "success": False,
                "error": f"Query failed: {result.get('error')}"
            }

        if not result.get('data') or len(result['data']) == 0:
            return {
                "success": False,
                "error": "Query returned no data"
            }

        columns = result['columns']
        data = result['data']

        # Auto-detect columns if not specified
        if not x_column and len(columns) >= 1:
            x_column = columns[0]
        if not y_column and len(columns) >= 2:
            y_column = columns[1]

        if not x_column or not y_column:
            return {
                "success": False,
                "error": "Could not determine X and Y columns. Please specify them explicitly."
            }

        try:
            # Get column indices
            x_idx = columns.index(x_column)
            y_idx = columns.index(y_column)

            # Extract data
            x_data = [row[x_idx] for row in data]
            y_data = [row[y_idx] for row in data]

            # Convert data types if needed
            def try_convert_numeric(values):
                converted = []
                for val in values:
                    try:
                        if isinstance(val, (int, float)):
                            converted.append(val)
                        elif isinstance(val, str) and val.replace('.', '').replace('-', '').isdigit():
                            converted.append(float(val))
                        else:
                            converted.append(val)
                    except:
                        converted.append(val)
                return converted

            y_data = try_convert_numeric(y_data)

            # Try to convert x_data to dates if they look like dates
            def try_convert_dates(values):
                converted = []
                for val in values:
                    try:
                        if isinstance(val, str):
                            # Try common date formats
                            for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%m/%d/%Y', '%d/%m/%Y']:
                                try:
                                    converted.append(datetime.strptime(val, fmt))
                                    break
                                except ValueError:
                                    continue
                            else:
                                converted.append(val)
                        else:
                            converted.append(val)
                    except:
                        converted.append(val)
                return converted

            if chart_type in ['line', 'scatter']:
                x_data = try_convert_dates(x_data)

            # Create the plot
            plt.figure(figsize=figsize)

            if chart_type == 'line':
                plt.plot(x_data, y_data, marker='o', linewidth=2, markersize=4)
                if isinstance(x_data[0], datetime):
                    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(x_data) // 10)))
                    plt.xticks(rotation=45)

            elif chart_type == 'bar':
                plt.bar(range(len(x_data)), y_data)
                plt.xticks(range(len(x_data)), x_data, rotation=45, ha='right')

            elif chart_type == 'scatter':
                plt.scatter(x_data, y_data, alpha=0.6)
                if isinstance(x_data[0], datetime):
                    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                    plt.xticks(rotation=45)

            elif chart_type == 'hist':
                plt.hist(y_data, bins=min(20, len(set(y_data))), alpha=0.7, edgecolor='black')
                plt.xlabel(y_column)
                plt.ylabel('Frequency')
            else:
                return {
                    "success": False,
                    "error": f"Unsupported chart type: {chart_type}. Use 'line', 'bar', 'scatter', or 'hist'"
                }

            # Set labels and title
            if chart_type != 'hist':
                plt.xlabel(x_column)
                plt.ylabel(y_column)

            if title:
                plt.title(title)
            else:
                plt.title(f"{chart_type.title()} Chart: {y_column} vs {x_column}")

            plt.grid(True, alpha=0.3)
            plt.tight_layout()

            # Save or show
            if output_file:
                plt.savefig(output_file, dpi=150, bbox_inches='tight')
                result_info = {"saved_to": output_file}
            else:
                # Save to temp file for display
                temp_file = os.path.join(tempfile.gettempdir(), f"chart_{int(time.time())}.png")
                plt.savefig(temp_file, dpi=150, bbox_inches='tight')
                result_info = {"temp_file": temp_file}

            if show_plot:
                try:
                    plt.show()
                except:
                    pass  # No display available

            plt.close()

            return {
                "success": True,
                "message": f"{chart_type.title()} chart created successfully",
                "rows_plotted": len(data),
                "x_column": x_column,
                "y_column": y_column,
                **result_info
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Chart creation failed: {str(e)}"
            }

    def quick_analyze(self, table_name, limit=100):
        """
        Quick data analysis with automatic visualizations.

        Args:
            table_name (str): Table to analyze
            limit (int): Row limit for analysis

        Returns:
            dict: Analysis results
        """
        if not MATPLOTLIB_SUPPORT:
            print("📊 Quick analysis (text only - install matplotlib for charts)")
        else:
            print(f"📊 Quick analysis of table '{table_name}' with visualizations")

        results = {}

        # Get table info
        columns_result = self.get_table_columns(table_name)
        if not columns_result.get('success'):
            return columns_result

        columns = columns_result['columns']
        results['columns'] = columns

        # Basic stats
        count_query = f"SELECT COUNT(*) FROM {table_name}"
        count_result = self.execute(count_query)
        if count_result.get('success'):
            total_rows = count_result['data'][0][0]
            results['total_rows'] = total_rows
            print(f"📋 Total rows: {total_rows:,}")

        # Sample data
        sample_query = f"SELECT * FROM {table_name} LIMIT {limit}"
        sample_result = self.execute(sample_query)
        if sample_result.get('success'):
            print(f"📋 Columns: {', '.join(columns)}")
            print(f"📋 Sample data ({len(sample_result['data'])} rows):")
            print_result(sample_result)

        # Try to create automatic visualizations
        if MATPLOTLIB_SUPPORT and len(columns) >= 2:
            print("\n📈 Creating automatic visualizations...")

            # Try different chart combinations
            chart_attempts = [
                # Line chart with first two columns
                {
                    'type': 'line',
                    'query': f"SELECT {columns[0]}, {columns[1]} FROM {table_name} ORDER BY {columns[0]} LIMIT {limit}",
                    'title': f"{columns[1]} over {columns[0]}"
                },
                # Bar chart if we have categorical data
                {
                    'type': 'bar',
                    'query': f"SELECT {columns[0]}, COUNT(*) as count FROM {table_name} GROUP BY {columns[0]} ORDER BY count DESC LIMIT 20",
                    'title': f"Distribution of {columns[0]}"
                }
            ]

            for i, chart_config in enumerate(chart_attempts):
                try:
                    chart_result = self.create_chart(
                        query=chart_config['query'],
                        chart_type=chart_config['type'],
                        title=chart_config['title'],
                        show_plot=False
                    )
                    if chart_result.get('success'):
                        print(f"✓ Created {chart_config['type']} chart: {chart_config['title']}")
                        if 'temp_file' in chart_result:
                            print(f"  Saved to: {chart_result['temp_file']}")
                    else:
                        print(f"⚠️ Could not create {chart_config['type']} chart: {chart_result.get('error')}")
                except Exception as e:
                    print(f"⚠️ Chart creation error: {e}")

        results['success'] = True
        return results

    def import_csv_to_table(self, csv_path: str, table_name: str,
                            column_mapping: Optional[Dict] = None,
                            chunk_size: int = 1000,
                            interactive: bool = True,
                            create_table: bool = False):
        """Universal CSV import that works with any supported database."""
        # FIXED: Check both CSV_SUPPORT and that pd/create_engine are available
        if not CSV_SUPPORT or pd is None or create_engine is None:
            return {
                "success": False,
                "error": "CSV import requires pandas and sqlalchemy. Install with: pip install pandas sqlalchemy"
            }

        if not os.path.exists(csv_path):
            return {"success": False, "error": f"CSV file not found: {csv_path}"}

        # Additional safety check - test that pandas actually works
        try:
            # Test pandas functionality
            test_df = pd.DataFrame({'test': [1, 2, 3]})
            if len(test_df) != 3:
                raise Exception("pandas not working properly")
        except Exception as e:
            return {"success": False, "error": f"pandas not properly loaded: {e}"}

        try:
            # Create SQLAlchemy engine
            engine_url = self.adapter.create_sqlalchemy_engine()
            engine = create_engine(engine_url)

            # Read CSV sample for analysis
            try:
                csv_sample = pd.read_csv(csv_path, nrows=100)
                csv_headers = csv_sample.columns.tolist()
            except Exception as e:
                return {"success": False, "error": f"Error reading CSV headers: {e}"}

            # Check if table exists
            table_exists = self._table_exists(table_name)

            if not table_exists:
                if create_table:
                    create_result = self._create_table_from_csv(table_name, csv_sample, interactive)
                    if not create_result.get('success'):
                        return create_result
                    if interactive:
                        print(f"✓ Created table '{table_name}'")
                else:
                    return {"success": False,
                            "error": f"Table '{table_name}' doesn't exist. Use --create-table flag to create it automatically."}

            # Get table columns
            columns_result = self.get_table_columns(table_name)
            if not columns_result.get('success'):
                return columns_result

            table_columns = columns_result['columns']

            # Handle column mapping
            if column_mapping is None:
                column_mapping = self._auto_map_columns(csv_headers, table_columns, interactive)
                if column_mapping is None:
                    return {"success": False, "message": "Import cancelled by user"}

            # Import data
            total_rows = 0
            start_time = datetime.now()

            if interactive:
                print(f"\nStarting CSV import to table '{table_name}'...")

            for chunk_number, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunk_size), 1):
                # Apply column mapping
                mapped_chunk = chunk[list(column_mapping.keys())].copy()
                mapped_chunk.columns = [column_mapping[col] for col in mapped_chunk.columns]

                # Clean data
                for col in mapped_chunk.select_dtypes(include=['object']).columns:
                    mapped_chunk[col] = mapped_chunk[col].astype(str).str.strip()
                    mapped_chunk[col] = mapped_chunk[col].replace('nan', None)

                # Import to database
                mapped_chunk.to_sql(table_name, engine, if_exists='append', index=False)

                total_rows += len(chunk)
                elapsed_time = (datetime.now() - start_time).total_seconds()
                rows_per_second = total_rows / elapsed_time if elapsed_time > 0 else 0

                if interactive:
                    print(f"Processed chunk {chunk_number}: {total_rows} total rows "
                          f"({rows_per_second:.1f} rows/second)")

            return {
                "success": True,
                "message": f"CSV import completed successfully!",
                "total_rows": total_rows,
                "elapsed_time": elapsed_time,
                "rows_per_second": rows_per_second
            }

        except Exception as e:
            return {"success": False, "error": f"Import error: {str(e)}"}
        finally:
            if 'engine' in locals():
                engine.dispose()

    def _table_exists(self, table_name: str) -> bool:
        """Check if table exists (database-agnostic)."""
        if self.db_type == 'mysql':
            query = f"""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = DATABASE() AND table_name = '{table_name}'
            """
        elif self.db_type == 'postgresql':
            query = f"""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = '{table_name}'
            """
        elif self.db_type == 'sqlite':
            query = f"""
            SELECT COUNT(*) FROM sqlite_master 
            WHERE type='table' AND name='{table_name}'
            """
        elif self.db_type == 'duckdb':
            try:
                # DuckDB: try to describe the table
                result = self.execute(f"DESCRIBE {table_name}")
                return result.get('success', False)
            except:
                return False
        else:
            return False

        result = self.execute(query)
        return (result.get('success') and
                result.get('data') and
                result['data'][0][0] > 0)

    def _auto_map_columns(self, csv_headers: List[str], table_columns: List[str], interactive: bool) -> Optional[Dict]:
        """Auto-map CSV columns to table columns."""
        column_mapping = {}

        for csv_col in csv_headers:
            if csv_col in table_columns:
                column_mapping[csv_col] = csv_col
            else:
                csv_col_lower = csv_col.lower()
                for table_col in table_columns:
                    if csv_col_lower == table_col.lower():
                        column_mapping[csv_col] = table_col
                        break

        if interactive:
            print("\nAutomatic column mapping:")
            for csv_col, table_col in column_mapping.items():
                print(f"  CSV: '{csv_col}' -> Table: '{table_col}'")

            unmapped_cols = set(csv_headers) - set(column_mapping.keys())
            if unmapped_cols:
                print("\nWarning: The following CSV columns couldn't be mapped:")
                for col in unmapped_cols:
                    print(f"  - {col}")

                print(f"\nAvailable table columns: {', '.join(table_columns)}")
                user_input = input("\nDo you want to continue with partial mapping? (y/n): ")
                if user_input.lower() != 'y':
                    return None

        return column_mapping

    def _create_table_from_csv(self, table_name: str, csv_sample, interactive: bool = True):
        """Create table from CSV structure (database-agnostic)."""
        # FIXED: Ensure csv_sample is a valid pandas DataFrame
        if not CSV_SUPPORT or pd is None:
            return {"success": False, "error": "pandas not available for table creation"}

        try:
            type_mapping = self.adapter.get_column_type_mapping()
            columns_sql = []

            for col_name in csv_sample.columns:
                clean_col_name = self._clean_column_name(col_name)
                col_data = csv_sample[col_name].dropna()

                if len(col_data) == 0:
                    col_type = type_mapping['string_medium']
                elif col_data.dtype == 'int64':
                    if (col_name.lower() in ['id', 'pk', 'primary_key'] and
                            col_data.min() >= 1 and
                            len(col_data) == len(col_data.unique())):
                        col_type = type_mapping['auto_increment_pk']
                    else:
                        max_val = col_data.max()
                        if max_val <= 127:
                            col_type = type_mapping['int_small']
                        elif max_val <= 32767:
                            col_type = type_mapping['int_medium']
                        else:
                            col_type = type_mapping['int_large']
                elif col_data.dtype == 'float64':
                    col_type = type_mapping['float']
                elif col_data.dtype == 'bool':
                    col_type = type_mapping['bool']
                else:
                    max_length = col_data.astype(str).str.len().max()
                    if max_length <= 50:
                        col_type = type_mapping['string_small']
                    elif max_length <= 255:
                        col_type = type_mapping['string_medium']
                    elif max_length <= 1000:
                        col_type = type_mapping['string_large']
                    else:
                        col_type = type_mapping['text']

                columns_sql.append(f"{clean_col_name} {col_type}")

            create_sql = f"CREATE TABLE {table_name} (\n  " + ",\n  ".join(columns_sql) + "\n)"

            if interactive:
                print(f"\nProposed table structure:")
                print(create_sql)
                user_input = input("\nCreate this table? (y/n): ")
                if user_input.lower() != 'y':
                    return {"success": False, "message": "Table creation cancelled by user"}

            result = self.execute(create_sql)
            return result

        except Exception as e:
            return {"success": False, "error": f"Error creating table: {str(e)}"}

    def _clean_column_name(self, col_name: str) -> str:
        """Clean column name for database compatibility."""
        clean_name = col_name.strip().replace(' ', '_').replace('-', '_')
        return ''.join(c for c in clean_name if c.isalnum() or c == '_')

    def close(self):
        self.adapter.close()


def print_result(result, format_output=True):
    """Print query results in formatted table."""
    if not result.get('success'):
        print(f"Error: {result.get('error', 'Unknown error')}")
        return

    if 'data' in result and 'columns' in result:
        columns = result['columns']
        data = result['data']

        if not data:
            print("Empty set")
            return

        if format_output and columns:
            print(tabulate(data, headers=columns, tablefmt="grid"))
            print(f"{len(data)} row(s) in set")
        else:
            if columns:
                print(f"Columns: {', '.join(columns)}")
            for row in data:
                print(row)
            print(f"({len(data)} rows)")
    elif 'message' in result:
        print(result['message'])
    else:
        print("Query executed successfully")


def handle_csv_import(client, command):
    """Handle CSV import command."""
    parts = command.split()
    if len(parts) < 3:
        print("Usage: csv_import <file> <table> [--create-table] [--chunk-size=N]")
        return

    csv_file = parts[1]
    table_name = parts[2]
    create_table = '--create-table' in parts

    # Parse chunk size
    chunk_size = 1000
    for part in parts:
        if part.startswith('--chunk-size='):
            try:
                chunk_size = int(part.split('=')[1])
            except ValueError:
                print("Invalid chunk size")
                return

    result = client.import_csv_to_table(
        csv_path=csv_file,
        table_name=table_name,
        create_table=create_table,
        chunk_size=chunk_size
    )

    if result.get('success'):
        print(f"✓ Import successful: {result['total_rows']} rows imported")
        print(f"Time: {result['elapsed_time']:.2f}s, Speed: {result['rows_per_second']:.1f} rows/s")
    else:
        print(f"✗ Import failed: {result.get('error')}")


def handle_url_import(client, command):
    """Handle URL CSV import command."""
    parts = command.split()
    if len(parts) < 3:
        print("Usage: url_import <url> <table> [--create-table] [--chunk-size=N] [--connections=N]")
        return

    url = parts[1]
    table_name = parts[2]
    create_table = '--create-table' in parts

    # Parse parameters
    chunk_size = 1000
    connections = 16

    for part in parts:
        if part.startswith('--chunk-size='):
            try:
                chunk_size = int(part.split('=')[1])
            except ValueError:
                print("Invalid chunk size")
                return
        elif part.startswith('--connections='):
            try:
                connections = int(part.split('=')[1])
            except ValueError:
                print("Invalid connections count")
                return

    result = client.import_csv_from_url(
        url=url,
        table_name=table_name,
        create_table=create_table,
        chunk_size=chunk_size,
        connections=connections
    )

    if result.get('success'):
        print(f"✓ URL import successful: {result['total_rows']} rows imported")
        if 'download_info' in result:
            dl_info = result['download_info']
            print(
                f"  Download: {dl_info['file_size_MB']} MB in {dl_info['download_time']:.1f}s ({dl_info['download_speed_MBps']:.1f} MB/s)")
        print(f"  Import: {result['elapsed_time']:.2f}s, {result['rows_per_second']:.1f} rows/s")
    else:
        print(f"✗ URL import failed: {result.get('error')}")


def handle_chart_command(client, command):
    """Handle chart creation command."""
    parts = command.split('"')
    if len(parts) < 3:
        print('Usage: chart <type> "SQL query" [--title="Title"] [--output=file.png]')
        print('Types: line, bar, scatter, hist')
        return

    chart_type = parts[0].split()[1].strip()
    query = parts[1].strip()

    # Parse additional options
    title = None
    output_file = None

    if len(parts) > 2:
        options = parts[2].strip()
        if '--title=' in options:
            title = options.split('--title=')[1].split()[0].strip('"')
        if '--output=' in options:
            output_file = options.split('--output=')[1].split()[0].strip()

    result = client.create_chart(
        query=query,
        chart_type=chart_type,
        title=title,
        output_file=output_file
    )

    if result.get('success'):
        print(f"✓ {chart_type} chart created: {result['rows_plotted']} data points")
        if 'saved_to' in result:
            print(f"  Saved to: {result['saved_to']}")
        elif 'temp_file' in result:
            print(f"  Saved to: {result['temp_file']}")
    else:
        print(f"✗ Chart creation failed: {result.get('error')}")


def interactive_mode(client, db_type):
    """Enhanced interactive mode with new features."""
    print(f"\n{db_type.upper()} Enhanced Interactive Mode")
    print("commands: csv_import, url_import, chart, analyze")
    print("Type 'help' for commands, 'exit' to quit")

    # Show feature availability
    features = []
    if ARIA2_SUPPORT:
        features.append("✓ URL Import (aria2)")
    else:
        features.append("✗ URL Import (install aria2)")

    if MATPLOTLIB_SUPPORT:
        features.append("✓ Charts (matplotlib)")
    else:
        features.append("✗ Charts (install matplotlib)")

    if CSV_SUPPORT:
        features.append("✓ CSV Import (pandas)")
    else:
        features.append("✗ CSV Import (install pandas)")

    print(f"Features: {' | '.join(features)}")
    print()

    while True:
        try:
            prompt = f"{db_type}> "
            user_input = input(prompt).strip()

            if user_input.lower() in ['exit', 'quit', '\\q']:
                break
            elif user_input.lower() in ['help', '\\h']:
                print_enhanced_help(db_type)
            elif user_input.lower().startswith('url_import'):
                handle_url_import(client, user_input)
            elif user_input.lower().startswith('chart '):
                handle_chart_command(client, user_input)
            elif user_input.lower().startswith('analyze '):
                table_name = user_input.split()[1].strip()
                client.quick_analyze(table_name)
            elif user_input.lower().startswith('csv_import'):
                handle_csv_import(client, user_input)
            elif user_input.lower() in ['show databases', '\\l']:
                result = client.get_databases()
                print_result(result)
            elif user_input.lower() in ['show tables', '\\dt']:
                result = client.get_tables()
                print_result(result)
            elif user_input.lower().startswith('describe ') or user_input.lower().startswith('\\d '):
                table_name = user_input.split()[1].strip()
                result = client.get_table_columns(table_name)
                if result.get('success'):
                    print(f"\nColumns in table '{table_name}':")
                    for col in result['columns']:
                        print(f"  - {col}")
                else:
                    print(f"Error: {result.get('error')}")
            else:
                # Execute as SQL
                result = client.execute(user_input)
                print_result(result)

        except KeyboardInterrupt:
            print("\nOperation cancelled")
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")


def print_enhanced_help(db_type):
    """Print enhanced help with new features."""
    print("""
    📊 Enhanced Database Commands:

    Data Import:
      csv_import <file> <table>         Import local CSV file
      url_import <url> <table>          Import CSV from URL (requires aria2)
      url_import <url> <table> --create-table --connections=16

    Data Visualization:
      chart line "SELECT date, value FROM data"     Create line chart
      chart bar "SELECT category, count FROM stats" Create bar chart
      chart scatter "SELECT x, y FROM points"       Create scatter plot
      analyze <table>                              Quick analysis with auto-charts

    Database Operations:
      show databases, \\l          List databases
      show tables, \\dt            List tables  
      describe <table>, \\d <table> Show table structure

    General:
      help, \\h                    Show this help
      exit, quit, \\q              Exit CLI

    Chart Types: line, bar, scatter, hist
    URL Import: Supports any public CSV URL, uses aria2 for fast downloads
    """)


def print_help(db_type):
    """Print database-specific help."""
    common_help = """
    Common Commands:
      show databases, \\l          List databases
      show tables, \\dt            List tables
      describe <table>, \\d <table> Show table structure
      csv_import <file> <table>    Import CSV file
      csv_import <file> <table> --create-table  Auto-create table
      url_import <url> <table>     Import CSV from URL
      chart <type> "SQL query"     Create charts
      analyze <table>              Quick table analysis
      help, \\h                    Show this help
      exit, quit, \\q              Exit CLI
    """

    db_specific = {
        'mysql': """
    MySQL Specific:
      use <database>               Switch database
      show processlist             Show running processes
      show status                  Show server status
      show variables               Show system variables
        """,
        'postgresql': """
    PostgreSQL Specific:
      \\c <database>               Connect to database
      \\du                         List users
      \\timing                     Toggle timing display
      SELECT version();            Show PostgreSQL version
        """,
        'duckdb': """
    DuckDB Specific:
      .tables                      List tables (alternative)
      .schema <table>              Show table schema
      PRAGMA database_list;        List attached databases
      SELECT * FROM duckdb_extensions();  Show extensions
        """,
        'sqlite': """
    SQLite Specific:
      .tables                      List tables (alternative)
      .schema <table>              Show table schema
      PRAGMA table_info(<table>);  Table information
      ATTACH DATABASE 'file' AS name;  Attach database
        """
    }

    print(common_help)
    if db_type in db_specific:
        print(db_specific[db_type])


def check_dependencies():
    """Check and report on optional dependencies with platform-specific instructions."""
    print("🔍 Checking dependencies...")

    # Detect platform
    system = platform.system().lower()
    architecture = platform.machine().lower()

    deps = {
        "aria2 (URL import)": ARIA2_SUPPORT,
        "matplotlib (charts)": MATPLOTLIB_SUPPORT,
        "pandas (CSV import)": CSV_SUPPORT
    }

    for dep, available in deps.items():
        status = "✓ Available" if available else "✗ Missing"
        print(f"  {dep}: {status}")

    # Platform-specific aria2 installation instructions
    if not ARIA2_SUPPORT:
        print(f"\n📥 To install aria2 on {platform.system()}:")

        if system == "linux":
            # Detect Linux distribution
            try:
                with open('/etc/os-release', 'r') as f:
                    os_release = f.read().lower()

                if 'ubuntu' in os_release or 'debian' in os_release:
                    print("  sudo apt update && sudo apt install -y aria2")
                elif 'fedora' in os_release or 'rhel' in os_release or 'centos' in os_release:
                    print("  sudo dnf install aria2  # (Fedora/RHEL 8+)")
                    print("  sudo yum install aria2  # (CentOS/RHEL 7)")
                elif 'arch' in os_release:
                    print("  sudo pacman -S aria2")
                elif 'alpine' in os_release:
                    print("  sudo apk add aria2")
                else:
                    print("  # Use your distribution's package manager:")
                    print("  sudo apt install aria2      # Debian/Ubuntu")
                    print("  sudo dnf install aria2      # Fedora/RHEL")
                    print("  sudo pacman -S aria2        # Arch Linux")
            except:
                print("  sudo apt install aria2          # Debian/Ubuntu")
                print("  sudo dnf install aria2          # Fedora/RHEL")
                print("  sudo pacman -S aria2            # Arch Linux")

        elif system == "darwin":  # macOS
            print("  # Using Homebrew (recommended):")
            print("  brew install aria2")
            print("  ")
            print("  # Using MacPorts:")
            print("  sudo port install aria2")
            print("  ")
            print("  # Or download from: https://aria2.github.io/")

        elif system == "windows":
            if architecture in ['amd64', 'x86_64']:
                arch_str = "x64"
            else:
                arch_str = "x86"

            print(f"  # Method 1: Using Chocolatey (recommended):")
            print("  choco install aria2")
            print("  ")
            print("  # Method 2: Using Scoop:")
            print("  scoop install aria2")
            print("  ")
            print("  # Method 3: Manual download:")
            print(f"  # Download aria2-{arch_str} from https://aria2.github.io/")
            print("  # Extract to C:\\aria2\\ and add to PATH")
            print("  ")
            print("  # Method 4: Using winget:")
            print("  winget install aria2.aria2")
        else:
            print(f"  # Platform '{system}' detected - manual installation required:")
            print("  # Download from: https://aria2.github.io/")

    if not MATPLOTLIB_SUPPORT:
        print(f"\n📈 To install matplotlib:")
        print("  pip install matplotlib")
        print("  # or")
        print("  python -m pip install matplotlib")

    # Show platform info
    print(f"\n💻 Platform: {platform.system()} {platform.release()} ({platform.machine()})")

    # Python environment info
    print(f"🐍 Python: {platform.python_version()} ({platform.python_implementation()})")

    print()


def print_banner():
    """Print a friendly banner with platform and version info."""
    system_info = f"{platform.system()} {platform.machine()}"
    python_info = f"Python {platform.python_version()}"

    print("=" * 70)
    print("🐬 Ambivo Multi-Database CLI v2.1.0")
    print("   Universal Database Client - MySQL, PostgreSQL, SQLite, DuckDB")
    print("   Enhanced with URL Import & Data Visualization")
    print("   Built by Hemant Gosain 'Sunny' | Ambivo")
    print(f"   Platform: {system_info} | {python_info}")
    print("=" * 70)
    print()


def print_quick_help():
    """Print quick help for first-time users."""
    print("Quick Start:")
    print("  -H <host>     Database host (default: localhost)")
    print("  -u <user>     Username (default: root)")
    print("  -p <pass>     Password (will prompt if not provided)")
    print("  -d <db>       Database name (optional)")
    print("  --help        Full help")
    print()
    print("Examples:")
    print("  ambivo-db-cli mysql -H localhost -u root")
    print("  ambivo-db-cli postgresql -H myserver -u postgres -d myapp")
    print("  ambivo-db-cli sqlite -f /path/to/database.db")
    print("  ambivo-db-cli duckdb -f analytics.db")
    print()
    print("New Features:")
    print("  url_import https://example.com/data.csv table --create-table")
    print("  chart line \"SELECT date, sales FROM data ORDER BY date\"")
    print("  analyze sales_table")
    print()


def interactive_connection_setup():
    """Interactive setup for connection parameters."""
    print("🔧 Connection Setup")
    print("Type 'h' for help, 'q' to quit")
    print()

    # Get database type
    while True:
        db_type = input("Database type [mysql/postgresql/sqlite/duckdb] (default: mysql): ").strip().lower()
        if not db_type:
            db_type = "mysql"
        if db_type in ['h', 'help']:
            print_quick_help()
            continue
        if db_type in ['q', 'quit', 'exit']:
            return None
        if db_type in ['mysql', 'postgresql', 'sqlite', 'duckdb']:
            break
        print("Invalid database type. Please choose: mysql, postgresql, sqlite, or duckdb")

    connection_params = {'db_type': db_type}

    if db_type in ['mysql', 'postgresql']:
        # Network database setup
        host = input(f"Host (default: localhost): ").strip()
        connection_params['host'] = host if host else 'localhost'

        if db_type == 'mysql':
            port = input("Port (default: 3306): ").strip()
            connection_params['port'] = int(port) if port else 3306
            user = input("Username (default: root): ").strip()
            connection_params['user'] = user if user else 'root'
        else:  # postgresql
            port = input("Port (default: 5432): ").strip()
            connection_params['port'] = int(port) if port else 5432
            user = input("Username (default: postgres): ").strip()
            connection_params['user'] = user if user else 'postgres'

        database = input("Database name (optional): ").strip()
        if database:
            connection_params['database'] = database

        # Password prompt
        password = getpass.getpass(f"Password for {connection_params['user']}@{connection_params['host']}: ")
        if password:
            connection_params['password'] = password

    elif db_type in ['sqlite', 'duckdb']:
        # File-based database setup
        while True:
            db_file = input(f"{db_type.upper()} file path (or 'memory' for in-memory): ").strip()
            if db_file.lower() in ['memory', ':memory:', '']:
                connection_params['database_path'] = ':memory:'
                break
            elif os.path.exists(db_file) or input(f"File doesn't exist. Create new? (y/n): ").lower() == 'y':
                connection_params['database_path'] = db_file
                break
            else:
                print("Please provide a valid file path or 'memory'")

    return connection_params


def main():
    """Enhanced main entry point with better UX."""
    # Show banner
    print_banner()

    # Check dependencies
    check_dependencies()

    # Check if this is likely a first run (no arguments provided)
    if len(sys.argv) == 1:
        print("Welcome! It looks like this is your first time using Ambivo DB CLI.")
        print("Let's get you connected to your database.")
        print()

        user_choice = input("Would you like to (c)onnect interactively or see (h)elp? [c/h]: ").strip().lower()

        if user_choice in ['h', 'help']:
            print_quick_help()
            return 0
        elif user_choice in ['q', 'quit', 'exit']:
            print("Goodbye!")
            return 0
        elif user_choice in ['c', 'connect', 's', 'setup', '']:
            # Interactive setup
            params = interactive_connection_setup()
            if not params:
                print("Setup cancelled. Goodbye!")
                return 0

            # Create client with interactive params
            try:
                db_type = params.pop('db_type')
                client = MultiDatabaseClient(db_type, **params)

                # Test connection
                print(f"\n🔌 Connecting to {db_type.upper()}...")
                result = client.connect()

                if not result.get('success'):
                    print(f"❌ Connection failed: {result.get('error')}")
                    return 1

                print("✅ Connected successfully!")
                print()

                # Start interactive mode
                try:
                    interactive_mode(client, db_type)
                finally:
                    client.close()
                    print(f"\n👋 Disconnected from {db_type.upper()}. Goodbye!")

                return 0

            except Exception as e:
                print(f"❌ Error creating client: {e}")
                return 1
        else:
            print("Invalid choice. Use --help for command line options.")
            return 1

    # Continue with original argument parsing for command line usage
    parser = argparse.ArgumentParser(
        description="Ambivo Multi-Database CLI - MySQL (default), PostgreSQL, SQLite, and DuckDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          # MySQL (default - backward compatible)
          ambivo-db-cli -H localhost -u root -p password -d mydb
          ambivo-db-cli mysql -H localhost -u root -p password -d mydb

          # Other databases
          ambivo-db-cli postgresql -H localhost -u postgres -p password -d mydb
          ambivo-db-cli sqlite -f /path/to/database.db
          ambivo-db-cli duckdb -f /path/to/analytics.db

        Enhanced Features:
          # URL Import with aria2
          url_import https://example.com/data.csv users --create-table

          # Data Visualization  
          chart line "SELECT date, sales FROM data ORDER BY date"
          chart bar "SELECT category, COUNT(*) FROM products GROUP BY category"

          # Quick Analysis
          analyze sales_data

        Dependencies:
          MySQL:      pip install mysql-connector-python (default)
          PostgreSQL: pip install psycopg2-binary
          DuckDB:     pip install duckdb
          SQLite:     Built-in with Python
          CSV:        pip install pandas sqlalchemy
          Charts:     pip install matplotlib
          URL Import: aria2 (system package)
        """))

    # Add MySQL arguments to main parser for backward compatibility
    parser.add_argument("-H", "--host", default="localhost", help="MySQL host (default mode)")
    parser.add_argument("-P", "--port", type=int, default=3306, help="MySQL port (default mode)")
    parser.add_argument("-u", "--user", default="root", help="MySQL username (default mode)")
    parser.add_argument("-p", "--password", help="MySQL password (default mode)")
    parser.add_argument("-d", "--database", help="MySQL database name (default mode)")
    parser.add_argument("--ssl-disabled", action="store_true", help="Disable SSL (MySQL)")
    parser.add_argument("--charset", default="utf8mb4", help="Character set (MySQL)")
    parser.add_argument("query", nargs="?", help="SQL query to execute directly")
    parser.add_argument("--raw", action="store_true", help="Raw output format")
    parser.add_argument("--no-banner", action="store_true", help="Skip banner display")

    # Optional subcommand for explicit database selection
    subparsers = parser.add_subparsers(dest='db_type', help='Database type (optional - defaults to mysql)')

    # MySQL parser (explicit)
    mysql_parser = subparsers.add_parser('mysql', help='MySQL database (explicit)')
    mysql_parser.add_argument("-H", "--host", default="localhost", help="MySQL host")
    mysql_parser.add_argument("-P", "--port", type=int, default=3306, help="MySQL port")
    mysql_parser.add_argument("-u", "--user", default="root", help="MySQL username")
    mysql_parser.add_argument("-p", "--password", help="MySQL password")
    mysql_parser.add_argument("-d", "--database", help="MySQL database name")
    mysql_parser.add_argument("--ssl-disabled", action="store_true", help="Disable SSL")
    mysql_parser.add_argument("--charset", default="utf8mb4", help="Character set")

    # PostgreSQL parser
    pg_parser = subparsers.add_parser('postgresql', help='PostgreSQL database')
    pg_parser.add_argument("-H", "--host", default="localhost", help="PostgreSQL host")
    pg_parser.add_argument("-P", "--port", type=int, default=5432, help="PostgreSQL port")
    pg_parser.add_argument("-u", "--user", default="postgres", help="PostgreSQL username")
    pg_parser.add_argument("-p", "--password", help="PostgreSQL password")
    pg_parser.add_argument("-d", "--database", default="postgres", help="PostgreSQL database name")

    # SQLite parser
    sqlite_parser = subparsers.add_parser('sqlite', help='SQLite database')
    sqlite_parser.add_argument("-f", "--file", default=":memory:", help="SQLite database file (default: in-memory)")

    # DuckDB parser
    duckdb_parser = subparsers.add_parser('duckdb', help='DuckDB database (analytics)')
    duckdb_parser.add_argument("-f", "--file", default=":memory:", help="DuckDB database file (default: in-memory)")

    args = parser.parse_args()

    # Show banner unless suppressed
    if not getattr(args, 'no_banner', False):
        print_banner()
        check_dependencies()

    # Default to MySQL if no subcommand specified
    if not args.db_type:
        args.db_type = 'mysql'
        print("🐬 Defaulting to MySQL (use 'ambivo-db-cli <db_type>' to specify different database)")

    # Check dependencies and create client
    try:
        if args.db_type == 'mysql':
            if not MYSQL_SUPPORT:
                print("❌ MySQL support requires: pip install mysql-connector-python")
                return 1

            # Only prompt for password if user is specified and password is not
            password = args.password
            if not password and args.user and not args.query:
                # Interactive mode - prompt for password
                password = getpass.getpass(f"Enter password for {args.user}@{args.host}: ")
            elif not password and args.user and args.query:
                # Command line query mode - show helpful message
                print(
                    f"❌ Password required for user '{args.user}'. Use -p <password> or run without arguments for interactive setup.")
                return 1

            client = MultiDatabaseClient(
                db_type='mysql',
                host=args.host,
                port=args.port,
                user=args.user,
                password=password,
                database=args.database,
                ssl_disabled=getattr(args, 'ssl_disabled', False),
                charset=getattr(args, 'charset', 'utf8mb4')
            )

        elif args.db_type == 'postgresql':
            if not POSTGRESQL_SUPPORT:
                print("❌ PostgreSQL support requires: pip install psycopg2-binary")
                return 1

            password = args.password
            if not password and args.user and not args.query:
                password = getpass.getpass(f"Enter password for {args.user}@{args.host}: ")
            elif not password and args.user and args.query:
                print(
                    f"❌ Password required for user '{args.user}'. Use -p <password> or run without arguments for interactive setup.")
                return 1

            client = MultiDatabaseClient(
                db_type='postgresql',
                host=args.host,
                port=args.port,
                user=args.user,
                password=password,
                database=args.database
            )

        elif args.db_type == 'sqlite':
            client = MultiDatabaseClient(
                db_type='sqlite',
                database_path=args.file
            )

        elif args.db_type == 'duckdb':
            if not DUCKDB_SUPPORT:
                print("❌ DuckDB support requires: pip install duckdb")
                return 1

            client = MultiDatabaseClient(
                db_type='duckdb',
                database_path=args.file
            )

    except ImportError as e:
        print(f"❌ Dependency missing: {e}")
        return 1
    except Exception as e:
        print(f"❌ Client creation failed: {e}")
        return 1

    # Connect to database
    print(f"🔌 Connecting to {args.db_type.upper()}...")

    if args.db_type == 'mysql':
        print(f"   Host: {args.host}:{args.port}")
        print(f"   User: {args.user}")
        print(f"   Database: {args.database or 'none'}")
    elif args.db_type == 'postgresql':
        print(f"   Host: {args.host}:{args.port}")
        print(f"   User: {args.user}")
        print(f"   Database: {args.database}")
    elif args.db_type in ['sqlite', 'duckdb']:
        db_file = args.file if args.file != ':memory:' else 'in-memory'
        print(f"   Database: {db_file}")

    result = client.connect()

    if not result.get('success'):
        print(f"❌ Connection failed: {result.get('error')}")
        return 1

    print("✅ Connected successfully!")

    # Show feature status
    features = []
    if CSV_SUPPORT:
        features.append("✓ CSV Import")
    else:
        features.append("✗ CSV Import")

    if ARIA2_SUPPORT:
        features.append("✓ URL Import")
    else:
        features.append("✗ URL Import")

    if MATPLOTLIB_SUPPORT:
        features.append("✓ Charts")
    else:
        features.append("✗ Charts")

    print(f"📊 Features: {' | '.join(features)}")
    print()

    # Handle direct query execution (MySQL compatibility)
    if args.query:
        result = client.execute(args.query)
        print_result(result, not getattr(args, 'raw', False))
        client.close()
        return 0

    # Start interactive mode
    try:
        interactive_mode(client, args.db_type)
    finally:
        client.close()
        print(f"\n👋 Disconnected from {args.db_type.upper()}. Goodbye!")

    return 0


if __name__ == "__main__":
    sys.exit(main())