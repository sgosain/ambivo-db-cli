# Ambivo Database CLI Suite

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Multi-DB Support](https://img.shields.io/badge/Multi--Database-Support-brightgreen.svg)](https://github.com/sgosain/ambivo-db-cli)
[![URL Import](https://img.shields.io/badge/URL%20Import-aria2-orange.svg)](https://aria2.github.io/)
[![Data Visualization](https://img.shields.io/badge/Charts-matplotlib-red.svg)](https://matplotlib.org/)
[![Powered by Ambivo](https://img.shields.io/badge/Powered%20by-Ambivo-blue.svg)](https://www.ambivo.com)

**Professional Database CLI Suite - Universal Database Management Tools with Enhanced Data Processing**

A comprehensive suite of database CLI tools with advanced features including URL-based CSV imports, data visualization, and intelligent analytics. This collection provides both specialized MySQL tools and universal multi-database connectivity for modern enterprise database management.

## 🚀 Tools Overview

### 🐬 `mysql_cli.py` - Dedicated MySQL Client
Professional MySQL CLI with 95%+ compatibility with the popular [MySQL cheat sheet](https://gist.github.com/hofmannsven/9164408), enhanced with modern enterprise features and CSV import capabilities.

### 🌐 `db_cli.py` - Universal Multi-Database Client ⭐ **Enhanced**
Universal database client supporting MySQL, PostgreSQL, SQLite, and DuckDB with:
- **🌐 URL CSV Import**: Direct import from web URLs with aria2 acceleration
- **📊 Data Visualization**: Built-in charts (line, bar, scatter, histogram)
- **🤖 Quick Analysis**: Automatic data exploration with intelligent insights
- **🎯 Platform Intelligence**: Smart installation guidance for dependencies

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
- **🌐 URL CSV Import**: Direct import from web sources with high-speed downloads
- **📈 Data Visualization**: Built-in charts and quick analysis tools
- **Cross-Platform Compatibility**: Consistent experience across operating systems
- **Enterprise Error Handling**: Database-specific error codes with helpful guidance
- **Advanced Schema Inspection**: Tables, indexes, foreign keys, and relationships

### 🔧 Administrative Tools
- **User Management**: Built-in user and privilege management
- **Process Monitoring**: Real-time database process inspection
- **Performance Metrics**: Status variables and system monitoring
- **Import/Export**: Integrated backup and restore capabilities
- **🎯 Quick Analysis**: Automatic table exploration with visualizations

### 🌐 **NEW: Enhanced Data Import & Visualization**
- **URL Import**: Direct CSV import from any public URL
- **Multi-connection Downloads**: Up to 32 parallel connections with aria2
- **Automatic Charts**: Line charts, bar charts, scatter plots, histograms
- **Quick Analysis**: One-command table exploration with auto-generated visualizations
- **Platform-Specific Setup**: Intelligent installation guidance for all dependencies

## 🏢 About Ambivo

This suite is developed and maintained by **Ambivo**, a technology company focused on building innovative business management solutions. Learn more at [ambivo.com](https://www.ambivo.com).

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/sgosain/ambivo-db-cli.git
cd ambivo-db-cli

# Install Python dependencies
pip install -r requirements.txt

# Install database-specific drivers as needed
pip install mysql-connector-python  # For MySQL
pip install psycopg2-binary         # For PostgreSQL
pip install duckdb                  # For DuckDB
# SQLite is built into Python

# Install enhanced features (optional but recommended)
pip install matplotlib              # For data visualization
pip install pandas sqlalchemy       # For advanced CSV processing

# Make scripts executable
chmod +x mysql_cli.py db_cli.py
```

### 🌐 URL Import Dependencies (Optional)

For high-speed URL CSV imports, install aria2 on your target platform:

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y aria2

# Fedora/RHEL
sudo dnf install aria2

# macOS (Homebrew)
brew install aria2

# macOS (MacPorts)
sudo port install aria2

# Windows (Chocolatey)
choco install aria2

# Windows (Scoop)
scoop install aria2

# Windows (winget)
winget install aria2.aria2
```

*Note: URL import will work without aria2 but with slower single-threaded downloads*

### Interactive Setup (Recommended for Beginners)

```bash
# Just run without arguments for guided setup
./mysql_cli.py
./db_cli.py

# The tools will walk you through connection setup automatically!
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

### Enterprise MySQL Management with Enhanced Features
```bash
$ ./mysql_cli.py -u admin -p
Enter password for admin@localhost: ****
🐬 Connecting to MySQL...
✓ Connected successfully!
Server version: 8.0.32-MySQL
📊 Features: ✓ CSV Import | ✓ URL Import | ✓ Charts

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

### 🌐 **NEW: URL Import and Data Visualization**
```bash
$ ./db_cli.py mysql -H localhost -u root
🔍 Checking dependencies...
  aria2 (URL import): ✓ Available
  matplotlib (charts): ✓ Available
  pandas (CSV import): ✓ Available

mysql [sales_db]> url_import https://example.com/sales_data.csv sales --create-table --connections=16
🌐 Downloading CSV from URL: https://example.com/sales_data.csv
✓ Downloaded 15.2 MB in 3.4s (4.5 MB/s)
✓ Created table 'sales'
✓ URL import successful: 50000 rows imported
  Download: 15.2 MB in 3.4s (4.5 MB/s)
  Import: 85.0s, 588.2 rows/s

mysql [sales_db]> chart line "SELECT date, revenue FROM sales ORDER BY date"
✓ line chart created: 365 data points
  Saved to: /tmp/chart_1640995200.png

mysql [sales_db]> analyze sales
📊 Quick analysis of table 'sales' with visualizations
📋 Total rows: 50,000
📋 Columns: date, product_id, quantity, price, customer_id, revenue
📈 Creating automatic visualizations...
✓ Created line chart: revenue over date
✓ Created bar chart: Distribution of product_id
  Saved to: /tmp/chart_1640995201.png
  Saved to: /tmp/chart_1640995202.png
```

### Multi-Database Analytics Workflow with DuckDB
```bash
$ ./db_cli.py duckdb -f analytics.db
🔌 Connecting to DUCKDB...
✓ Connected successfully!
📊 Features: ✓ CSV Import | ✓ URL Import | ✓ Charts

duckdb> url_import https://data.gov/large_dataset.csv government_data --create-table --connections=32
🌐 Downloading CSV from URL: https://data.gov/large_dataset.csv
✓ Downloaded 156.7 MB in 8.2s (19.1 MB/s)
✓ URL import successful: 2000000 rows imported

duckdb> SELECT region, AVG(budget), COUNT(*) FROM government_data GROUP BY region
+----------+----------------+----------+
| region   | avg(budget)    | count(*) |
+==========+================+==========+
| North    |    1250000.00  |    45231 |
| South    |     890000.00  |    38904 |
| East     |    1120000.00  |    41205 |
| West     |    1380000.00  |    42389 |
+----------+----------------+----------+

duckdb> chart bar "SELECT region, AVG(budget) FROM government_data GROUP BY region" --title="Average Budget by Region"
✓ bar chart created: 4 data points
  Saved to: /tmp/budget_analysis.png
```

### PostgreSQL Enterprise Setup
```bash
$ ./db_cli.py postgresql -H pg-cluster.company.com -u admin -d enterprise
🔌 Connecting to POSTGRESQL...
✓ Connected successfully!
💻 Platform: Linux x86_64 | Python 3.11

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

### 🌐 Enhanced CSV Import Capabilities
Both CLIs support intelligent CSV import with:
- **🆕 URL Import**: Direct import from any public URL with aria2 acceleration
- **Automatic table creation** from CSV structure
- **Smart column mapping** with case-insensitive matching
- **Type inference** for optimal database schemas
- **Chunked processing** for large files (configurable chunk sizes)
- **Progress tracking** and performance metrics
- **🚀 High-speed downloads**: Up to 32 parallel connections

```bash
# Local CSV import
csv_import large_data.csv products --create-table --chunk-size=5000

# 🆕 URL import with high-speed download
url_import https://example.com/data.csv users --create-table --connections=32

# Advanced options
url_import https://big-dataset.com/data.csv logs --chunk-size=10000 --create-table
```

### 📊 **NEW: Data Visualization & Analysis**
Transform your database queries into visual insights:

```bash
# Line charts for time series
chart line "SELECT date, sales FROM revenue ORDER BY date"

# Bar charts for categories  
chart bar "SELECT category, COUNT(*) FROM products GROUP BY category"

# Scatter plots for correlations
chart scatter "SELECT price, rating FROM products"

# Histograms for distributions
chart hist "SELECT age FROM customers"

# Quick analysis with automatic charts
analyze sales_data
analyze customer_behavior
```

### 🎯 **NEW: Platform Intelligence**
The CLI automatically detects your platform and provides specific installation instructions:

```bash
# Automatic platform detection and guidance
🔍 Checking dependencies...
  aria2 (URL import): ✗ Missing
  matplotlib (charts): ✓ Available
  pandas (CSV import): ✓ Available

📥 To install aria2 on Linux:
  sudo apt update && sudo apt install -y aria2

📈 To install matplotlib:
  pip install matplotlib
```

### Database-Specific Features

#### MySQL CLI Exclusive Features
- Full MySQL cheat sheet compatibility
- Enhanced user and privilege management
- Integrated mysqldump support
- MySQL-specific performance monitoring
- **🆕 Enhanced CSV import** with MySQL optimizations

#### Multi-Database CLI Universal Features
- Seamless database engine switching
- Consistent interface across all databases
- Database-agnostic SQL execution
- Cross-platform table and schema inspection
- **🆕 URL-based data import** from any public source
- **🆕 Universal visualization** across all database types
- **🆕 Quick analysis** with automatic insights

## 🎯 When to Use Which Tool

### Use `mysql_cli.py` when:
- ✅ Working exclusively with MySQL
- ✅ Need full MySQL cheat sheet compatibility
- ✅ Require advanced MySQL administrative features
- ✅ Want optimized MySQL-specific functionality
- ✅ **🆕 Need fast CSV imports** for MySQL workflows

### Use `db_cli.py` when:
- ✅ Working with multiple database types
- ✅ Need analytics capabilities (DuckDB)
- ✅ Want consistent interface across databases
- ✅ Require SQLite or PostgreSQL connectivity
- ✅ Building multi-database applications
- ✅ **🆕 Need URL-based data import** from web sources
- ✅ **🆕 Want data visualization** and quick analysis
- ✅ **🆕 Working with large datasets** requiring parallel downloads

## 🏆 Why Choose Ambivo Database CLI Suite?

### vs. Standard Database CLIs
- ✅ **Unified experience** across different database engines
- ✅ **Enhanced table formatting** with professional grid layouts
- ✅ **Intelligent error handling** with helpful guidance
- ✅ **Modern interactive features** (history, tab completion)
- ✅ **🆕 URL-based imports** directly from web sources
- ✅ **🆕 Built-in visualization** without external tools
- ✅ **🆕 Platform intelligence** with smart setup guidance

### vs. GUI Database Tools
- ✅ **Lightweight and fast** - no heavy interface overhead
- ✅ **Scriptable and automatable** for DevOps workflows
- ✅ **SSH-friendly** for remote server management
- ✅ **Version control friendly** for database scripts
- ✅ **Professional command-line experience**
- ✅ **🆕 Built-in analytics** without switching tools

### vs. Other CLI Tools
- ✅ **Full backward compatibility** with existing MySQL knowledge
- ✅ **Multi-database support** in single tool suite
- ✅ **Enterprise-grade features** designed for production use
- ✅ **Active development** by experienced database professionals
- ✅ **MIT open source license** - free for commercial use
- ✅ **🆕 Modern data workflows** with URL import and visualization

## 📦 Installation Options

### Method 1: Complete Installation (Recommended)
```bash
git clone https://github.com/sgosain/ambivo-db-cli.git
cd ambivo-db-cli

# Install all Python dependencies
pip install -r requirements.txt

# Install system dependencies for enhanced features
# Ubuntu/Debian
sudo apt update && sudo apt install -y aria2

# macOS
brew install aria2

# Windows
choco install aria2

# Test all features
./mysql_cli.py --help
./db_cli.py --help
```

### Method 2: Individual Database Support
```bash
# Core dependencies
pip install tabulate

# MySQL only
pip install mysql-connector-python

# PostgreSQL only  
pip install psycopg2-binary

# Analytics (DuckDB) only
pip install duckdb

# Enhanced features
pip install pandas sqlalchemy matplotlib  # CSV + Visualization
```

### Method 3: 🆕 Pre-built Binaries (Coming Soon)
```bash
# Download from releases
wget https://github.com/sgosain/ambivo-db-cli/releases/latest/ambivo-db-cli-linux-x64.tar.gz
tar -xzf ambivo-db-cli-linux-x64.tar.gz
cd linux-x64/
./install.sh
```

## 🔧 Dependencies

### Core Dependencies (Required)
- `Python 3.8+` (updated minimum version)
- `tabulate` - Table formatting

### Database Drivers (Install as needed)
- `mysql-connector-python` - MySQL support
- `psycopg2-binary` - PostgreSQL support  
- `duckdb` - DuckDB analytics support
- `sqlite3` - Built into Python

### Enhanced Features (Highly Recommended)
- `pandas` + `sqlalchemy` - Advanced CSV import and processing
- `matplotlib` - **🆕 Data visualization and charts**
- `readline` - Command history and tab completion

### System Dependencies (Optional but Recommended)
- `aria2` - **🆕 High-speed URL downloads** (install via system package manager)
  - **Ubuntu/Debian**: `sudo apt install aria2`
  - **macOS**: `brew install aria2`
  - **Windows**: `choco install aria2` or `winget install aria2.aria2`

### Feature Matrix
| Feature | Core | MySQL | PostgreSQL | DuckDB | Visualization | URL Import |
|---------|------|-------|------------|--------|---------------|------------|
| **Basic Connectivity** | ✅ | ✅ | ✅ | ✅ | - | - |
| **CSV Import** | ✅ | ✅ | ✅ | ✅ | - | - |
| **🆕 URL Import** | - | ✅ | ✅ | ✅ | - | ✅ |
| **🆕 Charts** | - | ✅ | ✅ | ✅ | ✅ | - |
| **🆕 Quick Analysis** | - | ✅ | ✅ | ✅ | ✅ | - |

## 📚 Documentation

### Command Reference
- **MySQL CLI**: Full MySQL cheat sheet compatibility + enhanced features
- **Multi-DB CLI**: Universal commands across all databases + visualization
- **🆕 URL Import**: Direct data loading from web sources
- **🆕 Visualization**: Built-in charting and analysis tools
- **CSV Import**: Advanced data loading capabilities
- **Administrative Tools**: User management and monitoring

### Examples Repository
- Production deployment scripts
- Data migration examples
- **🆕 Analytics workflow templates** with visualization
- **🆕 URL import examples** for various data sources
- Administrative automation

### 🆕 New Interactive Features
```bash
# Enhanced help system
help                    # Shows all commands including new features
url_import --help       # Specific help for URL imports
chart --help           # Chart creation help
analyze --help         # Quick analysis help

# Feature detection
show features          # Display available features for current environment
check dependencies     # Verify all optional dependencies
```

## 📞 Support & Community

- 📧 **Email**: sgosain@ambivo.com
- 🏢 **Company**: [Ambivo](https://www.ambivo.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/sgosain/ambivo-db-cli/issues)
- 📖 **Documentation**: [Wiki](https://github.com/sgosain/ambivo-db-cli/wiki)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/sgosain/ambivo-db-cli/discussions)

*Note: Software is provided AS-IS with no formal support, but the community and maintainers are active and helpful.*

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help makes these tools better for everyone.

- See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
- Check [Issues](https://github.com/sgosain/ambivo-db-cli/issues) for open tasks
- Join [Discussions](https://github.com/sgosain/ambivo-db-cli/discussions) for feature requests

## 📈 Roadmap

### Power features  ✅
- **🌐 URL CSV Import**: Direct import from web sources with aria2 acceleration
- **📊 Data Visualization**: Built-in charts (line, bar, scatter, histogram)
- **🤖 Quick Analysis**: Automatic table exploration with visualizations
- **🎯 Platform Intelligence**: Smart dependency detection and installation guidance
- **⚡ Performance Enhancements**: Multi-connection downloads and optimized imports

### Upcoming Features 🚧
- 🔐 Enhanced security features and connection encryption
- 📊 Advanced analytics functions and statistical operations
- 🚀 Additional database engine support (MongoDB, Redis)
- 🤖 AI-powered query optimization suggestions
- 📱 Web interface for remote database management
- 🔄 Real-time data streaming and live chart updates
- 📈 Export capabilities for charts and reports

## 📊 Performance Benchmarks

### URL Import Performance
- **Single connection**: ~5-10 MB/s
- **16 connections (default)**: ~50-100 MB/s  
- **32 connections**: ~100-200 MB/s
- **Network dependent**: Actual speeds vary by source

### CSV Processing Performance
- **Local files**: 5,000-15,000 rows/second
- **URL imports**: 2,000-10,000 rows/second (network dependent)
- **Memory usage**: ~50-200MB for large datasets
- **Chunked processing**: Handles files larger than available RAM

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

---

## 🚀 **What's New in v2.1.0**

- **🌐 URL CSV Import**: Import data directly from any public URL
- **📊 Data Visualization**: Built-in charts without external tools  
- **🤖 Quick Analysis**: One-command table exploration
- **🎯 Platform Intelligence**: Smart setup guidance for all platforms
- **⚡ Performance**: Multi-connection downloads up to 200 MB/s
- **🔧 Enhanced Dependencies**: Better handling of optional features

*Upgrade today to experience the next generation of database CLI tools!*