# Ambivo Database CLI Suite

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Multi-DB Support](https://img.shields.io/badge/Multi--Database-Support-brightgreen.svg)](https://github.com/sgosain/ambivo-db-cli)
[![Powered by Ambivo](https://img.shields.io/badge/Powered%20by-Ambivo-blue.svg)](https://www.ambivo.com)

**Professional Database CLI Suite - Universal Database Management Tools**

A comprehensive suite of database CLI tools built by **Hemant Gosain 'Sunny'** at **Ambivo**. This collection provides both specialized MySQL tools and universal multi-database connectivity for modern enterprise database management.

## 🚀 Tools Overview

### 🐬 `mysql_cli.py` - Dedicated MySQL Client
Professional MySQL CLI with 95%+ compatibility with the popular [MySQL cheat sheet](https://gist.github.com/hofmannsven/9164408), enhanced with modern enterprise features.

### 🌐 `db_cli.py` - Universal Multi-Database Client
Universal database client supporting MySQL, PostgreSQL, SQLite, and DuckDB with seamless switching and consistent interface across all database engines.

## ✨ Key Features

### 🎯 Universal Database Support
- **MySQL**: Production web applications and OLTP workloads
- **PostgreSQL**: Enterprise applications and complex queries  
- **SQLite**: Embedded applications, testing, and development
- **DuckDB**: Analytics, data science, and OLAP workloads

### 📊 Professional Features
- **Beautiful Table Formatting**: Grid layouts with professional presentation
- **Command History & Tab Completion**: Readline support for enhanced productivity
- **Intelligent CSV Import**: Automatic column mapping and type inference
- **Cross-Platform Compatibility**: Consistent experience across operating systems
- **Enterprise Error Handling**: Database-specific error codes with helpful guidance
- **Advanced Schema Inspection**: Tables, indexes, foreign keys, and relationships

### 🔧 Administrative Tools
- **User Management**: Built-in user and privilege management
- **Process Monitoring**: Real-time database process inspection
- **Performance Metrics**: Status variables and system monitoring
- **Import/Export**: Integrated backup and restore capabilities

## 🏢 About Ambivo

This suite is developed and maintained by **Ambivo**, a technology company focused on building innovative data management solutions. Learn more at [ambivo.com](https://www.ambivo.com).

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/sgosain/ambivo-db-cli.git
cd ambivo-db-cli

# Install base dependencies
pip install -r requirements.txt

# Install database-specific drivers as needed
pip install mysql-connector-python  # For MySQL
pip install psycopg2-binary         # For PostgreSQL
pip install duckdb                  # For DuckDB
# SQLite is built into Python

# Make scripts executable
chmod +x mysql_cli.py db_cli.py
```

### MySQL CLI Usage

```bash
# Dedicated MySQL client with full cheat sheet compatibility
./mysql_cli.py -H localhost -u root -p

# Connect to specific database
./mysql_cli.py -H mysql.server.com -u admin -d production -p

# Execute single query
./mysql_cli.py -u root -p "SHOW DATABASES"
```

### Multi-Database CLI Usage

```bash
# MySQL (default - backward compatible)
./db_cli.py -H localhost -u root -p password -d mydb
./db_cli.py mysql -H localhost -u root -p password -d mydb

# PostgreSQL
./db_cli.py postgresql -H localhost -u postgres -p password -d mydb

# SQLite
./db_cli.py sqlite -f /path/to/database.db

# DuckDB (Analytics)
./db_cli.py duckdb -f /path/to/analytics.db
```

## 📖 Usage Examples

### Enterprise MySQL Management
```bash
$ ./mysql_cli.py -u admin -p
Enter password for admin@localhost: ****
🐬 Connecting to MySQL...
✓ Connected successfully!
Server version: 8.0.32-MySQL
📊 CSV Import: Enabled
🔍 Tab completion enabled

mysql [production_db]> show databases
+--------------------+-----------+
| Database           | Size (MB) |
+====================+===========+
| production_db      |   2847.32 |
| staging_db         |    156.78 |
| analytics_warehouse|   8923.12 |
+--------------------+-----------+

mysql [production_db]> csv_import data.csv users --create-table
✓ Created table 'users'
✓ Import successful: 50000 rows imported
Time: 12.34s, Speed: 4051.9 rows/s
```

### Multi-Database Analytics Workflow
```bash
$ ./db_cli.py duckdb -f analytics.db
🔌 Connecting to DUCKDB...
✓ Connected successfully!
📊 CSV Import: Enabled

duckdb> CREATE TABLE sales AS SELECT * FROM 'large_sales_data.csv'
Query executed successfully

duckdb> SELECT region, SUM(revenue) FROM sales GROUP BY region
+----------+-------------+
| region   | sum(revenue)|
+==========+=============+
| North    |   1250000.00|
| South    |    890000.00|
| East     |   1120000.00|
| West     |   1380000.00|
+----------+-------------+
```

### PostgreSQL Enterprise Setup
```bash
$ ./db_cli.py postgresql -H pg-cluster.company.com -u admin -d enterprise
🔌 Connecting to POSTGRESQL...
✓ Connected successfully!

postgresql> \l
+------------------+--------+
| Database         | Size   |
+==================+========+
| enterprise       | 156 MB |
| analytics        | 2.1 GB |
| reporting        | 89 MB  |
+------------------+--------+

postgresql> SELECT version();
PostgreSQL 14.7 on x86_64-pc-linux-gnu, compiled by gcc
```

## 🛠 Advanced Features

### CSV Import Capabilities
Both CLIs support intelligent CSV import with:
- **Automatic table creation** from CSV structure
- **Smart column mapping** with case-insensitive matching
- **Type inference** for optimal database schemas
- **Chunked processing** for large files
- **Progress tracking** and performance metrics

```bash
# MySQL CLI
csv_import large_data.csv products --create-table --chunk-size=5000

# Multi-DB CLI (works with all databases)
csv_import data.csv users --create-table
```

### Database-Specific Features

#### MySQL CLI Exclusive Features
- Full MySQL cheat sheet compatibility
- Enhanced user and privilege management
- Integrated mysqldump support
- MySQL-specific performance monitoring

#### Multi-Database CLI Universal Features
- Seamless database engine switching
- Consistent interface across all databases
- Database-agnostic SQL execution
- Cross-platform table and schema inspection

## 🎯 When to Use Which Tool

### Use `mysql_cli.py` when:
- ✅ Working exclusively with MySQL
- ✅ Need full MySQL cheat sheet compatibility
- ✅ Require advanced MySQL administrative features
- ✅ Want optimized MySQL-specific functionality

### Use `db_cli.py` when:
- ✅ Working with multiple database types
- ✅ Need analytics capabilities (DuckDB)
- ✅ Want consistent interface across databases
- ✅ Require SQLite or PostgreSQL connectivity
- ✅ Building multi-database applications

## 🏆 Why Choose Ambivo Database CLI Suite?

### vs. Standard Database CLIs
- ✅ **Unified experience** across different database engines
- ✅ **Enhanced table formatting** with professional grid layouts
- ✅ **Intelligent error handling** with helpful guidance
- ✅ **Modern interactive features** (history, tab completion)
- ✅ **Advanced CSV capabilities** with automatic mapping

### vs. GUI Database Tools
- ✅ **Lightweight and fast** - no heavy interface overhead
- ✅ **Scriptable and automatable** for DevOps workflows
- ✅ **SSH-friendly** for remote server management
- ✅ **Version control friendly** for database scripts
- ✅ **Professional command-line experience**

### vs. Other CLI Tools
- ✅ **Full backward compatibility** with existing MySQL knowledge
- ✅ **Multi-database support** in single tool suite
- ✅ **Enterprise-grade features** designed for production use
- ✅ **Active development** by experienced database professionals
- ✅ **MIT open source license** - free for commercial use

## 📦 Installation Options

### Method 1: Direct Installation (Recommended)
```bash
git clone https://github.com/sgosain/ambivo-db-cli.git
cd ambivo-db-cli
pip install -r requirements.txt

# Test MySQL CLI
./mysql_cli.py --help

# Test Multi-DB CLI  
./db_cli.py --help
```

### Method 2: Individual Database Support
```bash
# MySQL only
pip install mysql-connector-python tabulate

# PostgreSQL only  
pip install psycopg2-binary tabulate

# Analytics (DuckDB) only
pip install duckdb tabulate

# Full CSV support
pip install pandas sqlalchemy
```

## 🔧 Dependencies

### Core Dependencies (Required)
- `Python 3.7+`
- `tabulate` - Table formatting

### Database Drivers (Install as needed)
- `mysql-connector-python` - MySQL support
- `psycopg2-binary` - PostgreSQL support  
- `duckdb` - DuckDB analytics support
- `sqlite3` - Built into Python

### Enhanced Features (Optional)
- `pandas` + `sqlalchemy` - Advanced CSV import
- `readline` - Command history and tab completion

## 📚 Documentation

### Command Reference
- **MySQL CLI**: Full MySQL cheat sheet compatibility
- **Multi-DB CLI**: Universal commands across all databases
- **CSV Import**: Advanced data loading capabilities
- **Administrative Tools**: User management and monitoring

### Examples Repository
- Production deployment scripts
- Data migration examples
- Analytics workflow templates
- Administrative automation

## 📞 Support & Community

- 📧 **Email**: sgosain@ambivo.com
- 🏢 **Company**: [Ambivo](https://www.ambivo.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/sgosain/ambivo-db-cli/issues)
- 📖 **Documentation**: [Wiki](https://github.com/sgosain/ambivo-db-cli/wiki)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/sgosain/ambivo-db-cli/discussions)

*Note: Software is provided AS-IS with no formal support, but the community and maintainers are active and helpful.*

## 🤝 Contributing

We welcome contributions from the database community! Whether you're fixing bugs, adding features, or improving documentation, your help makes these tools better for everyone.

- See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
- Check [Issues](https://github.com/sgosain/ambivo-db-cli/issues) for open tasks
- Join [Discussions](https://github.com/sgosain/ambivo-db-cli/discussions) for feature requests

## 📈 Roadmap

### Upcoming Features
- 🔐 Enhanced security features and connection encryption
- 📊 Built-in query performance profiling
- 🚀 Additional database engine support (MongoDB, Redis)
- 🤖 AI-powered query optimization suggestions
- 📱 Web interface for remote database management

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License - Ambivo Database CLI Suite

Copyright (c) 2025 Hemant Gosain / Ambivo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

**Built with 🛡️ by Hemant Gosain 'Sunny' at Ambivo**

*Professional database CLI tools for modern enterprises and developers*

[![Ambivo](https://img.shields.io/badge/Visit-Ambivo.com-blue?style=for-the-badge)](https://www.ambivo.com)