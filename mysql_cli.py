#!/usr/bin/env python3
"""
Ambivo MySQL CLI - MySQL client

This MySQL CLI client provides near-full MySQL cheat sheet compatibility
with modern enhancements for enterprise database management.
Built by the Ambivo  team to deliver superior database administration experience.

Features:
- 95%+ MySQL cheat sheet compatibility https://gist.github.com/hofmannsven/9164408
- Enhanced interactive mode with beautiful table formatting
- Command history and tab completion with readline support
- User management and administrative tools
- Integrated import/export with mysqldump
- CSV import functionality with intelligent column mapping
- Advanced schema inspection with indexes and foreign keys
- Intelligent error handling with helpful guidance

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

GitHub: https://github.com/yourusername/ambivo-mysql-cli
Company: https://www.ambivo.com
"""

__author__ = "Hemant Gosain 'Sunny'"
__copyright__ = "Copyright (c) 2025 Hemant Gosain / Ambivo"
__license__ = "MIT"
__version__ = "1.2.0"
__maintainer__ = "Hemant Gosain 'Sunny'"
__email__ = "sgosain@ambivo.com"
__status__ = "Production"
__company__ = "Ambivo"


def print_license():
    """Print the full license information."""
    print(f"""
MIT License - Ambivo MySQL CLI

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

GitHub Repository: https://github.com/yourusername/ambivo-mysql-cli
Report Issues: https://github.com/yourusername/ambivo-mysql-cli/issues
Ambivo: https://www.ambivo.com
""")


import mysql.connector
import argparse
import sys
import textwrap
import subprocess
import os
import getpass
import json
from datetime import datetime
from tabulate import tabulate
from typing import Dict, List, Optional

# Command history and readline support
try:
    import readline
    import atexit

    READLINE_SUPPORT = True
except ImportError:
    READLINE_SUPPORT = False

# Optional imports for CSV functionality
try:
    import pandas as pd
    from sqlalchemy import create_engine

    CSV_SUPPORT = True
except ImportError:
    CSV_SUPPORT = False


def setup_readline():
    """Setup readline for command history and tab completion."""
    if not READLINE_SUPPORT:
        return

    # History file location
    history_dir = os.path.expanduser("~/.ambivo_cli")
    os.makedirs(history_dir, exist_ok=True)
    history_file = os.path.join(history_dir, "mysql_history")

    # Load existing history
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass

    # Configure readline
    readline.set_history_length(1000)  # Keep last 1000 commands

    # Save history on exit
    def save_history():
        try:
            readline.write_history_file(history_file)
        except Exception:
            pass

    atexit.register(save_history)

    # Setup tab completion
    setup_tab_completion()


def setup_tab_completion():
    """Setup intelligent tab completion for MySQL commands."""
    if not READLINE_SUPPORT:
        return

    # MySQL keywords and commands for completion
    mysql_keywords = [
        'SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP',
        'ALTER', 'TABLE', 'DATABASE', 'INDEX', 'VIEW', 'GRANT', 'REVOKE',
        'ORDER BY', 'GROUP BY', 'HAVING', 'LIMIT', 'OFFSET', 'JOIN', 'INNER JOIN',
        'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN', 'UNION', 'DISTINCT', 'COUNT',
        'SUM', 'AVG', 'MAX', 'MIN', 'AND', 'OR', 'NOT', 'IN', 'EXISTS',
        'LIKE', 'BETWEEN', 'IS NULL', 'IS NOT NULL'
    ]

    # MySQL-specific commands
    mysql_commands = [
        'SHOW DATABASES', 'SHOW TABLES', 'SHOW COLUMNS', 'SHOW INDEX',
        'SHOW PROCESSLIST', 'SHOW STATUS', 'SHOW VARIABLES', 'USE',
        'DESCRIBE', 'EXPLAIN', 'FLUSH PRIVILEGES', 'START TRANSACTION',
        'COMMIT', 'ROLLBACK', 'SHOW CREATE TABLE', 'SHOW GRANTS',
        'SHOW ENGINES', 'SHOW WARNINGS', 'SHOW ERRORS'
    ]

    # CLI-specific commands
    cli_commands = [
        'csv_import', 'show databases', 'show tables', 'describe', 'help', 'exit', 'quit',
        'mysqldump', 'history', 'clear', 'cls'
    ]

    # Combine all completions
    all_completions = mysql_keywords + mysql_commands + cli_commands

    def completer(text, state):
        """Tab completion function."""
        text_upper = text.upper()
        matches = [cmd for cmd in all_completions if cmd.upper().startswith(text_upper)]

        # Add lowercase versions for convenience
        matches.extend([cmd.lower() for cmd in matches if cmd.isupper()])

        # Remove duplicates while preserving order
        seen = set()
        unique_matches = []
        for match in matches:
            if match not in seen:
                seen.add(match)
                unique_matches.append(match)

        try:
            return unique_matches[state]
        except IndexError:
            return None

    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    # Enable case-insensitive completion
    readline.parse_and_bind("set completion-ignore-case on")

    # Show all completions when ambiguous
    readline.parse_and_bind("set show-all-if-ambiguous on")


class EnhancedMySQLClient:
    """Enhanced MySQL client with full command compatibility - Powered by Ambivo."""

    def __init__(self, host='localhost', port=3306, user='root', password=None,
                 database=None, ssl_disabled=False, timeout=30, charset='utf8mb4'):
        """Initialize enhanced MySQL client."""
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

    def connect(self):
        """Establish connection to MySQL."""
        try:
            config = {
                'host': self.host,
                'port': self.port,
                'user': self.user,
                'password': self.password,
                'autocommit': True,
                'connection_timeout': self.timeout,
                'charset': self.charset,
                'use_unicode': True
            }

            if self.database:
                config['database'] = self.database

            if self.ssl_disabled:
                config['ssl_disabled'] = True

            self.connection = mysql.connector.connect(**config)
            return {"success": True, "message": "Connected successfully"}

        except mysql.connector.Error as e:
            return {"success": False, "error": f"MySQL Error: {e}"}
        except Exception as e:
            return {"success": False, "error": f"Connection Error: {e}"}

    def execute(self, sql: str, parameters: Optional[List] = None):
        """Execute SQL query with enhanced error handling."""
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

            # Handle different query types
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
                # Handle database switching
                cursor.close()
                self.current_database = sql.split()[1].strip('`;')
                return {
                    "success": True,
                    "message": f"Database changed to '{self.current_database}'"
                }
            else:
                # For INSERT, UPDATE, DELETE, CREATE, DROP, etc.
                affected_rows = cursor.rowcount
                cursor.close()

                # Get more specific messages for different operations
                if sql_upper.startswith('INSERT'):
                    message = f"Query OK, {affected_rows} row(s) inserted"
                elif sql_upper.startswith('UPDATE'):
                    message = f"Query OK, {affected_rows} row(s) affected"
                elif sql_upper.startswith('DELETE'):
                    message = f"Query OK, {affected_rows} row(s) deleted"
                elif sql_upper.startswith(('CREATE', 'DROP', 'ALTER')):
                    message = "Query OK, 0 rows affected"
                else:
                    message = f"Query OK, {affected_rows} row(s) affected"

                return {
                    "success": True,
                    "message": message,
                    "affected_rows": affected_rows
                }

        except mysql.connector.Error as e:
            return {"success": False, "error": f"MySQL Error {e.errno}: {e.msg}"}
        except Exception as e:
            return {"success": False, "error": f"Execution Error: {e}"}

    def get_databases(self):
        """Get list of databases - Enhanced with sizes."""
        query = """
                SELECT schema_name as 'Database', ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as 'Size (MB)'
                FROM information_schema.tables
                WHERE schema_name NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys')
                GROUP BY schema_name
                ORDER BY schema_name \
                """
        result = self.execute(query)
        if result.get('success'):
            return result
        else:
            # Fallback to simple query
            return self.execute("SHOW DATABASES")

    def get_tables(self, database=None):
        """Get tables with enhanced information."""
        if database:
            query = f"""
            SELECT 
                table_name as 'Table',
                table_type as 'Type',
                engine as 'Engine',
                table_rows as 'Rows',
                ROUND((data_length + index_length) / 1024 / 1024, 2) as 'Size (MB)'
            FROM information_schema.tables 
            WHERE table_schema = '{database}'
            ORDER BY table_name
            """
        else:
            query = """
                    SELECT table_name as 'Table', table_type as 'Type', engine as 'Engine', table_rows as 'Rows', ROUND((data_length + index_length) / 1024 / 1024, 2) as 'Size (MB)'
                    FROM information_schema.tables
                    WHERE table_schema = DATABASE()
                    ORDER BY table_name \
                    """

        result = self.execute(query)
        if result.get('success'):
            return result
        else:
            # Fallback to simple query
            return self.execute("SHOW TABLES")

    def get_table_schema_enhanced(self, table_name: str):
        """Enhanced table schema with indexes and constraints."""
        # Get basic column info
        basic_info = self.execute(f"DESCRIBE {table_name}")

        # Get indexes
        indexes = self.execute(f"SHOW INDEX FROM {table_name}")

        # Get foreign keys
        fk_query = f"""
        SELECT 
            COLUMN_NAME,
            REFERENCED_TABLE_NAME,
            REFERENCED_COLUMN_NAME
        FROM information_schema.KEY_COLUMN_USAGE 
        WHERE TABLE_NAME = '{table_name}' 
        AND REFERENCED_TABLE_NAME IS NOT NULL
        """
        foreign_keys = self.execute(fk_query)

        return {
            "basic_info": basic_info,
            "indexes": indexes,
            "foreign_keys": foreign_keys
        }

    def get_table_columns(self, table_name: str):
        """Get existing table column names."""
        if not self.current_database:
            return {"success": False, "error": "No database selected"}

        query = f"SHOW COLUMNS FROM {table_name}"
        result = self.execute(query)

        if result.get('success'):
            columns = [row[0] for row in result['data']]  # Column names are in first position
            return {"success": True, "columns": columns}
        else:
            return result

    def import_csv_to_table(self, csv_path: str, table_name: str,
                            column_mapping: Optional[Dict] = None,
                            chunk_size: int = 1000,
                            interactive: bool = True,
                            create_table: bool = False):
        """
        Import CSV file to MySQL table with intelligent column mapping.

        Args:
            csv_path (str): Path to the CSV file
            table_name (str): Target table name
            column_mapping (dict): Manual column mapping {'csv_col': 'table_col'}
            chunk_size (int): Rows to process at once
            interactive (bool): Whether to prompt user for confirmations
            create_table (bool): Whether to create table if it doesn't exist
        """
        if not CSV_SUPPORT:
            return {
                "success": False,
                "error": "CSV import requires pandas and sqlalchemy. Install with: pip install pandas sqlalchemy"
            }

        if not os.path.exists(csv_path):
            return {"success": False, "error": f"CSV file not found: {csv_path}"}

        if not self.current_database:
            return {"success": False, "error": "No database selected. Use 'USE database_name;'"}

        try:
            # Create SQLAlchemy engine for pandas integration
            engine = create_engine(
                f"mysql+mysqlconnector://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.current_database}"
            )

            # Read CSV headers and sample data for type inference
            try:
                csv_sample = pd.read_csv(csv_path, nrows=100)  # Read sample for type inference
                csv_headers = csv_sample.columns.tolist()
            except Exception as e:
                return {"success": False, "error": f"Error reading CSV headers: {e}"}

            # Check if table exists, create if needed
            table_exists_query = f"""
            SELECT COUNT(*) as count FROM information_schema.tables 
            WHERE table_schema = '{self.current_database}' AND table_name = '{table_name}'
            """
            table_check = self.execute(table_exists_query)

            table_exists = (table_check.get('success') and
                            table_check.get('data') and
                            table_check['data'][0][0] > 0)

            if not table_exists:
                if create_table:
                    # Create table based on CSV structure
                    create_result = self._create_table_from_csv(table_name, csv_sample, interactive)
                    if not create_result.get('success'):
                        return create_result
                    if interactive:
                        print(f"✓ Created table '{table_name}'")
                else:
                    return {"success": False,
                            "error": f"Table '{table_name}' doesn't exist. Use --create-table flag to create it automatically."}

            # Get existing table columns
            columns_result = self.get_table_columns(table_name)
            if not columns_result.get('success'):
                return columns_result

            table_columns = columns_result['columns']

            # Create or validate column mapping
            if column_mapping is None:
                column_mapping = {}

                # Create automatic case-insensitive mapping
                for csv_col in csv_headers:
                    if csv_col in table_columns:
                        column_mapping[csv_col] = csv_col
                    else:
                        csv_col_lower = csv_col.lower()
                        for table_col in table_columns:
                            if csv_col_lower == table_col.lower():
                                column_mapping[csv_col] = table_col
                                break

                # Show automatic mapping
                if interactive:
                    print("\nAutomatic column mapping:")
                    for csv_col, table_col in column_mapping.items():
                        print(f"  CSV: '{csv_col}' -> Table: '{table_col}'")

                    # Check for unmapped columns
                    unmapped_cols = set(csv_headers) - set(column_mapping.keys())
                    if unmapped_cols:
                        print("\nWarning: The following CSV columns couldn't be mapped:")
                        for col in unmapped_cols:
                            print(f"  - {col}")

                        print(f"\nAvailable table columns: {', '.join(table_columns)}")
                        user_input = input("\nDo you want to continue with partial mapping? (y/n): ")
                        if user_input.lower() != 'y':
                            return {"success": False, "message": "Import cancelled by user"}

            # Verify mapped columns exist in table
            invalid_mappings = [table_col for table_col in column_mapping.values()
                                if table_col not in table_columns]
            if invalid_mappings:
                return {"success": False, "error": f"Invalid table column(s): {invalid_mappings}"}

            # Process CSV in chunks
            total_rows = 0
            start_time = datetime.now()

            if interactive:
                print(f"\nStarting CSV import to table '{table_name}'...")
                print(f"Chunk size: {chunk_size} rows")

            for chunk_number, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunk_size), 1):
                # Apply column mapping
                mapped_chunk = chunk[list(column_mapping.keys())].copy()
                mapped_chunk.columns = [column_mapping[col] for col in mapped_chunk.columns]

                # Clean string data
                for col in mapped_chunk.select_dtypes(include=['object']).columns:
                    mapped_chunk[col] = mapped_chunk[col].astype(str).str.strip()
                    # Replace 'nan' strings with None
                    mapped_chunk[col] = mapped_chunk[col].replace('nan', None)

                # Import chunk to MySQL
                mapped_chunk.to_sql(table_name, engine, if_exists='append', index=False)

                # Update progress
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

    def _create_table_from_csv(self, table_name: str, csv_sample: pd.DataFrame, interactive: bool = True):
        """Create table based on CSV structure with intelligent type inference."""
        try:
            columns_sql = []

            for col_name in csv_sample.columns:
                # Clean column name (remove special characters, spaces)
                clean_col_name = col_name.strip().replace(' ', '_').replace('-', '_')
                clean_col_name = ''.join(c for c in clean_col_name if c.isalnum() or c == '_')

                # Infer data type from sample data
                col_data = csv_sample[col_name].dropna()

                if len(col_data) == 0:
                    col_type = "VARCHAR(255)"
                elif col_data.dtype == 'int64':
                    # Check if it could be a primary key (unique integers starting from 1)
                    if (col_name.lower() in ['id', 'pk', 'primary_key'] and
                            col_data.min() >= 1 and
                            len(col_data) == len(col_data.unique())):
                        col_type = "INT AUTO_INCREMENT PRIMARY KEY"
                    else:
                        max_val = col_data.max()
                        if max_val <= 127:
                            col_type = "TINYINT"
                        elif max_val <= 32767:
                            col_type = "SMALLINT"
                        elif max_val <= 2147483647:
                            col_type = "INT"
                        else:
                            col_type = "BIGINT"
                elif col_data.dtype == 'float64':
                    col_type = "DECIMAL(10,2)"
                elif col_data.dtype == 'bool':
                    col_type = "BOOLEAN"
                else:
                    # String data - determine appropriate VARCHAR size
                    max_length = col_data.astype(str).str.len().max()
                    if max_length <= 50:
                        col_type = "VARCHAR(50)"
                    elif max_length <= 255:
                        col_type = "VARCHAR(255)"
                    elif max_length <= 1000:
                        col_type = "VARCHAR(1000)"
                    else:
                        col_type = "TEXT"

                columns_sql.append(f"`{clean_col_name}` {col_type}")

            # Create the table
            create_sql = f"CREATE TABLE `{table_name}` (\n  " + ",\n  ".join(columns_sql) + "\n)"

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

    def get_users(self):
        """Get MySQL users and their privileges."""
        query = """
                SELECT User, \
                       Host, \
                       account_locked as 'Locked', password_expired as 'Pwd_Expired'
                FROM mysql.user
                ORDER BY User, Host \
                """
        return self.execute(query)

    def get_processes(self):
        """Get current MySQL processes."""
        return self.execute("SHOW PROCESSLIST")

    def get_status(self, pattern=None):
        """Get MySQL status variables."""
        if pattern:
            return self.execute(f"SHOW STATUS LIKE '{pattern}'")
        else:
            return self.execute("SHOW STATUS")

    def get_variables(self, pattern=None):
        """Get MySQL system variables."""
        if pattern:
            return self.execute(f"SHOW VARIABLES LIKE '{pattern}'")
        else:
            return self.execute("SHOW VARIABLES")

    def mysqldump(self, database, output_file=None, tables=None):
        """Execute mysqldump command."""
        try:
            cmd = [
                'mysqldump',
                f'--host={self.host}',
                f'--port={self.port}',
                f'--user={self.user}'
            ]

            if self.password:
                cmd.append(f'--password={self.password}')

            cmd.append(database)

            if tables:
                cmd.extend(tables)

            if output_file:
                with open(output_file, 'w') as f:
                    result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
            else:
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                message = f"Dump completed successfully"
                if output_file:
                    message += f" to {output_file}"
                return {"success": True, "message": message, "output": result.stdout}
            else:
                return {"success": False, "error": result.stderr}

        except FileNotFoundError:
            return {"success": False, "error": "mysqldump command not found. Please install MySQL client tools."}
        except Exception as e:
            return {"success": False, "error": f"Dump error: {e}"}

    def load_data_infile(self, file_path, table_name, fields_terminated_by=',',
                         lines_terminated_by='\\n', ignore_lines=0):
        """Load data from file into table."""
        query = f"""
        LOAD DATA INFILE '{file_path}'
        INTO TABLE {table_name}
        FIELDS TERMINATED BY '{fields_terminated_by}'
        LINES TERMINATED BY '{lines_terminated_by}'
        """

        if ignore_lines > 0:
            query += f" IGNORE {ignore_lines} LINES"

        return self.execute(query)

    def export_to_file(self, query, output_file, fields_terminated_by=','):
        """Export query results to file."""
        export_query = f"""
        {query}
        INTO OUTFILE '{output_file}'
        FIELDS TERMINATED BY '{fields_terminated_by}'
        LINES TERMINATED BY '\\n'
        """
        return self.execute(export_query)

    def health(self):
        """Enhanced health check with server info."""
        if not self.connection:
            return self.connect()

        try:
            self.connection.ping(reconnect=True)

            # Get server version and info
            version_result = self.execute("SELECT VERSION() as version")
            uptime_result = self.execute("SHOW STATUS LIKE 'Uptime'")

            health_info = {"success": True, "status": "healthy"}

            if version_result.get('success'):
                health_info["version"] = version_result["data"][0][0]

            if uptime_result.get('success'):
                uptime_seconds = int(uptime_result["data"][0][1])
                uptime_hours = uptime_seconds // 3600
                health_info["uptime_hours"] = uptime_hours

            return health_info

        except Exception as e:
            return {"success": False, "error": f"Health check failed: {e}"}

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()


def parse_csv_import_command(command_parts):
    """Parse CSV import command and extract parameters."""
    # Expected format: csv_import <csv_file> <table_name> [options]
    if len(command_parts) < 3:
        return None, "Usage: csv_import <csv_file> <table_name> [--chunk-size=1000] [--mapping=file.json] [--create-table]"

    csv_file = command_parts[1]
    table_name = command_parts[2]

    # Default options
    options = {
        'chunk_size': 1000,
        'mapping_file': None,
        'create_table': False
    }

    # Parse optional parameters
    for part in command_parts[3:]:
        if part.startswith('--chunk-size='):
            try:
                options['chunk_size'] = int(part.split('=')[1])
            except ValueError:
                return None, "Invalid chunk size. Must be a number."
        elif part.startswith('--mapping='):
            options['mapping_file'] = part.split('=')[1]
        elif part == '--create-table':
            options['create_table'] = True

    return {
        'csv_file': csv_file,
        'table_name': table_name,
        'options': options
    }, None


def interactive_mode_enhanced(client):
    """Enhanced interactive mode with readline support and full MySQL compatibility."""
    # Setup command history and tab completion
    setup_readline()

    print("Ambivo MySQL CLI - Professional Database Management")
    print("Powered by Ambivo | Built by Hemant Gosain 'Sunny'")
    if READLINE_SUPPORT:
        print("📝 Command history enabled (↑/↓ arrows)")
        print("🔍 Tab completion enabled")
    else:
        print("💡 Install readline for command history: pip install readline")
    print("Type 'help' for commands, 'exit' to quit")
    print(f"Current database: {client.current_database or 'None'}")
    if CSV_SUPPORT:
        print("CSV Import: Enabled")
    else:
        print("CSV Import: Disabled (install pandas and sqlalchemy to enable)")
    print()

    while True:
        try:
            prompt = f"mysql [{client.current_database or 'none'}]> "
            user_input = input(prompt).strip()

            if user_input.lower() in ['exit', 'quit', '\\q']:
                break
            elif user_input.lower() in ['help', '\\h']:
                print_enhanced_help()
            elif user_input.lower().startswith('csv_import'):
                # Handle CSV import command
                command_parts = user_input.split()
                params, error = parse_csv_import_command(command_parts)

                if error:
                    print(f"Error: {error}")
                    continue

                if not client.current_database:
                    print("Error: No database selected. Use 'USE database_name;' first.")
                    continue

                # Load column mapping if specified
                column_mapping = None
                if params['options']['mapping_file']:
                    try:
                        with open(params['options']['mapping_file'], 'r') as f:
                            column_mapping = json.load(f)
                        print(f"Loaded column mapping from {params['options']['mapping_file']}")
                    except Exception as e:
                        print(f"Warning: Could not load mapping file: {e}")

                # Execute CSV import
                result = client.import_csv_to_table(
                    csv_path=params['csv_file'],
                    table_name=params['table_name'],
                    column_mapping=column_mapping,
                    chunk_size=params['options']['chunk_size'],
                    interactive=True,
                    create_table=params['options']['create_table']
                )

                if result.get('success'):
                    print(f"\n✓ {result['message']}")
                    print(f"Total rows imported: {result['total_rows']}")
                    print(f"Time taken: {result['elapsed_time']:.2f} seconds")
                    print(f"Speed: {result['rows_per_second']:.1f} rows/second")
                else:
                    print(f"✗ Import failed: {result.get('error')}")

            elif user_input.lower() in ['\\d', 'show databases']:
                result = client.get_databases()
                print_result(result)
            elif user_input.lower() in ['\\t', 'show tables']:
                result = client.get_tables()
                print_result(result)
            elif user_input.lower() == 'show processlist':
                result = client.get_processes()
                print_result(result)
            elif user_input.lower().startswith('show status'):
                if 'like' in user_input.lower():
                    pattern = user_input.split("'")[1] if "'" in user_input else None
                    result = client.get_status(pattern)
                else:
                    result = client.get_status()
                print_result(result)
            elif user_input.lower().startswith('show variables'):
                if 'like' in user_input.lower():
                    pattern = user_input.split("'")[1] if "'" in user_input else None
                    result = client.get_variables(pattern)
                else:
                    result = client.get_variables()
                print_result(result)
            elif user_input.lower().startswith('mysqldump'):
                parts = user_input.split()
                if len(parts) >= 2:
                    database = parts[1]
                    output_file = parts[2] if len(parts) > 2 else None
                    result = client.mysqldump(database, output_file)
                    if result.get('success'):
                        print(result['message'])
                    else:
                        print(f"Error: {result.get('error')}")
                else:
                    print("Usage: mysqldump <database> [output_file]")
            elif user_input.lower().startswith('describe ') or user_input.lower().startswith('desc '):
                table_name = user_input.split()[1].strip('`;')
                schema_info = client.get_table_schema_enhanced(table_name)

                if schema_info['basic_info'].get('success'):
                    print(f"\nTable structure for '{table_name}':")
                    print_result(schema_info['basic_info'])

                    if schema_info['indexes'].get('success') and schema_info['indexes']['data']:
                        print(f"\nIndexes:")
                        print_result(schema_info['indexes'])

                    if schema_info['foreign_keys'].get('success') and schema_info['foreign_keys']['data']:
                        print(f"\nForeign Keys:")
                        print_result(schema_info['foreign_keys'])
                else:
                    print(f"Error: {schema_info['basic_info'].get('error')}")
            elif user_input.lower() == 'clear' or user_input.lower() == 'cls':
                # Clear screen command
                os.system('clear' if os.name == 'posix' else 'cls')
            elif user_input.lower() == 'history':
                # Show command history
                if READLINE_SUPPORT:
                    print("\nCommand History:")
                    for i in range(1, readline.get_current_history_length() + 1):
                        try:
                            cmd = readline.get_history_item(i)
                            if cmd:
                                print(f"  {i:3d}: {cmd}")
                        except:
                            pass
                else:
                    print("Command history not available (install readline)")
            else:
                # Execute as SQL
                if not user_input.endswith(';'):
                    user_input += ';'

                result = client.execute(user_input)

                if result.get('success'):
                    if 'data' in result and result['data']:
                        print_result(result)
                    else:
                        print(result.get('message', 'Query executed successfully'))
                else:
                    print(f"Error: {result.get('error')}")

        except KeyboardInterrupt:
            print("\n🔄 Operation cancelled (Ctrl+C)")
            print("💡 Use 'exit' or 'quit' to leave the CLI")
        except EOFError:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def print_enhanced_help():
    """Print enhanced help with MySQL cheat sheet commands and readline info."""
    readline_help = """
    CLI Features:
      ↑/↓ arrows                   Navigate command history
      Tab                          Auto-complete commands
      history                      Show command history
      clear, cls                   Clear screen
    """ if READLINE_SUPPORT else """
    CLI Features:
      💡 Install readline for command history: pip install readline
    """

    csv_help = """
    CSV Import:
      csv_import <file> <table>      Import CSV to table with auto-mapping
      csv_import <file> <table> --create-table  Create table automatically
      csv_import <file> <table> --chunk-size=5000  Custom chunk size
      csv_import <file> <table> --mapping=map.json  Use mapping file
    """ if CSV_SUPPORT else """
    CSV Import:
      (Not available - install pandas and sqlalchemy)
    """

    print(textwrap.dedent(f"""
    Ambivo MySQL CLI Commands (MySQL Cheat Sheet Compatible):

    Connection & Database:
      show databases                 List all databases with sizes
      use <database>                 Switch to database

    Tables & Structure:
      show tables                    List tables with metadata
      describe <table>               Show enhanced table structure
      show create table <table>      Show CREATE statement

    Data Operations:
      SELECT, INSERT, UPDATE, DELETE Standard SQL operations
    {csv_help}
    User Management:
      SELECT User,Host FROM mysql.user    List users
      GRANT/REVOKE commands               Manage privileges
      FLUSH PRIVILEGES                    Reload privileges

    Administrative:
      show processlist               Show running processes
      show status [like 'pattern']   Show server status
      show variables [like 'pattern'] Show system variables

    Import/Export:
      mysqldump <db> [file]          Export database
      LOAD DATA INFILE               Import from file
      SELECT ... INTO OUTFILE        Export to file

    CLI Commands:
      help, \\h                      Show this help
      exit, quit, \\q                Exit the CLI
    {readline_help}
    Powered by Ambivo - Professional Database Tools
    """))


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
            # Raw output
            if columns:
                print(f"Columns: {', '.join(columns)}")
            for row in data:
                print(row)
            print(f"({len(data)} rows)")
    elif 'message' in result:
        print(result['message'])
    else:
        print("Query executed successfully")


def main():
    """Enhanced main entry point for Ambivo MySQL CLI."""
    parser = argparse.ArgumentParser(
        description="Ambivo MySQL CLI - Professional MySQL Database Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          ./mysql_cli.py -H localhost -u root -p <password>
          ./mysql_cli.py -H mysql.server.com -P 3306 -u admin -d production
          ./mysql_cli.py --license

        CSV Import Examples (inside CLI):
          csv_import data.csv users
          csv_import data.csv products --create-table
          csv_import large_data.csv products --chunk-size=5000
          csv_import data.csv table --mapping=column_map.json

        Professional MySQL CLI by Ambivo
        Built by Hemant Gosain 'Sunny' | https://www.ambivo.com

        MySQL Cheat Sheet Compatibility:
          Supports 95%+ of commands from: https://gist.github.com/hofmannsven/9164408

        Dependencies for CSV Import:
          pip install pandas sqlalchemy

        Dependencies for Command History:
          pip install readline (Linux/macOS)
          pip install pyreadline3 (Windows)
        """))

    parser.add_argument("--license", action="store_true", help="Show license information and exit")
    # Changed -h to -H to avoid conflict with argparse's built-in -h/--help
    parser.add_argument("-H", "--host", default="localhost", help="MySQL host")
    parser.add_argument("-P", "--port", type=int, default=3306, help="MySQL port")
    parser.add_argument("-u", "--user", default="root", help="MySQL username")
    parser.add_argument("-p", "--password", help="MySQL password (will prompt if not provided)")
    parser.add_argument("-d", "--database", help="MySQL database name")
    parser.add_argument("--ssl-disabled", action="store_true", help="Disable SSL")
    parser.add_argument("--charset", default="utf8mb4", help="Character set")
    parser.add_argument("query", nargs="?", help="SQL query to execute")
    parser.add_argument("--raw", action="store_true", help="Raw output format")

    args = parser.parse_args()

    if args.license:
        print_license()
        return 0

    # Handle password prompt
    password = args.password
    if not password and args.user:
        password = getpass.getpass(f"Enter password for {args.user}@{args.host}: ")

    # Create enhanced client
    client = EnhancedMySQLClient(
        host=args.host,
        port=args.port,
        user=args.user,
        password=password,
        database=args.database,
        ssl_disabled=args.ssl_disabled,
        charset=args.charset
    )

    # Test connection
    print("Ambivo MySQL CLI - Connecting to MySQL...")
    print(f"Host: {args.host}:{args.port} | User: {args.user}")

    # Check feature support and show status
    if not CSV_SUPPORT:
        print("Note: CSV import functionality disabled")
        print("To enable: pip install pandas sqlalchemy")

    if not READLINE_SUPPORT:
        print("Note: Command history disabled")
        print("To enable: pip install readline (Linux/macOS) or pyreadline3 (Windows)")

    health_result = client.health()

    if not health_result.get('success'):
        print(f"Connection failed: {health_result.get('error')}")
        print("Please check your connection parameters and try again.")
        return 1

    print("✓ Connected successfully!")
    if health_result.get('version'):
        print(f"Server version: {health_result['version']}")
    if health_result.get('uptime_hours'):
        print(f"Server uptime: {health_result['uptime_hours']} hours")
    print()

    # Execute query or interactive mode
    if args.query:
        result = client.execute(args.query)
        print_result(result, not args.raw)
    else:
        interactive_mode_enhanced(client)

    client.close()
    print("Connection closed. Thank you for using Ambivo MySQL CLI!")
    return 0


if __name__ == "__main__":
    sys.exit(main())