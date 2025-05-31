# Ambivo Database CLI Suite - Binary Distribution

## 📦 Download Links

### Latest Release Binaries

| Platform | Architecture | Download | Size |
|----------|--------------|----------|------|
| **Linux** | x64 | [ambivo-db-cli-linux-x64.tar.gz](https://github.com/sgosain/ambivo-db-cli/releases/latest/download/ambivo-db-cli-linux-x64.tar.gz) | ~15MB |
| **macOS** | Intel (x64) | [ambivo-db-cli-macos-x64.tar.gz](https://github.com/sgosain/ambivo-db-cli/releases/latest/download/ambivo-db-cli-macos-x64.tar.gz) | ~16MB |
| **macOS** | Apple Silicon (ARM64) | [ambivo-db-cli-macos-arm64.tar.gz](https://github.com/sgosain/ambivo-db-cli/releases/latest/download/ambivo-db-cli-macos-arm64.tar.gz) | ~16MB |
| **Windows** | x64 | [ambivo-db-cli-windows-x64.zip](https://github.com/sgosain/ambivo-db-cli/releases/latest/download/ambivo-db-cli-windows-x64.zip) | ~18MB |

## 🚀 Quick Installation

### 1. Download and Extract

**Linux/macOS:**
```bash
# Download for your platform
curl -L -o ambivo-db-cli.tar.gz "https://github.com/sgosain/ambivo-db-cli/releases/latest/download/ambivo-db-cli-linux-x64.tar.gz"

# Extract
tar -xzf ambivo-db-cli.tar.gz
cd linux-x64/  # or your platform directory
```

**Windows:**
```cmd
# Download ambivo-db-cli-windows-x64.zip
# Extract to a folder
# Open Command Prompt in that folder
```

### 2. Install (Optional)

**Linux/macOS:**
```bash
# Run the install script
./install.sh

# Or manually copy to your PATH
cp ambivo-mysql-cli ambivo-db-cli ~/bin/
```

**Windows:**
```cmd
# Run the install script
install.bat

# Or manually copy to a folder in your PATH
```

### 3. Test Installation

```bash
# Test MySQL CLI
ambivo-mysql-cli --help

# Test Multi-Database CLI
ambivo-db-cli --help

# Use convenience wrappers
mysql --help       # MySQL CLI shortcut
dbcli --help       # Multi-DB CLI shortcut
```

## 🎯 Usage Examples

### MySQL Database Management

```bash
# Connect to MySQL
mysql -H localhost -u root -p

# In interactive mode
mysql> show databases;
mysql> use production_db;
mysql> show tables;
mysql> csv_import data.csv users --create-table

# Single query execution
mysql -u root -p "SELECT COUNT(*) FROM users"
```

### Multi-Database Analytics

```bash
# PostgreSQL for enterprise data
dbcli postgresql -H pg-server -u admin -p -d warehouse
postgresql> \dt
postgresql> SELECT * FROM sales_summary;

# SQLite for local development
dbcli sqlite -f local_app.db
sqlite> .tables
sqlite> csv_import test_data.csv products

# DuckDB for analytics
dbcli duckdb -f analytics.db
duckdb> CREATE TABLE sales AS SELECT * FROM 'large_sales.csv';
duckdb> SELECT region, SUM(revenue) FROM sales GROUP BY region;
```

## ✨ Key Features

### 🌐 Universal Database Support
- **MySQL**: Production web applications, OLTP workloads
- **PostgreSQL**: Enterprise applications, complex queries
- **SQLite**: Development, testing, embedded applications
- **DuckDB**: Analytics, data science, OLAP workloads

### 📊 Professional Features
- **Beautiful Table Formatting**: Grid layouts with aligned columns
- **Command History**: Navigate previous commands with ↑/↓ arrows
- **Tab Completion**: Auto-complete SQL keywords and commands
- **CSV Import**: Intelligent column mapping and type inference
- **Cross-Platform**: Consistent experience on all operating systems

### 🚀 Enterprise Ready
- **Standalone Executables**: No Python installation required
- **Professional Error Handling**: Database-specific guidance
- **Advanced Schema Inspection**: Tables, indexes, foreign keys
- **Performance Monitoring**: Status variables and metrics
- **Backup & Restore**: Integrated dump and load capabilities

## 📝 Command Reference

### Common Commands (Both CLIs)

| Command | Description |
|---------|-------------|
| `help` | Show available commands |
| `show databases` | List all databases |
| `show tables` | List tables in current database |
| `describe <table>` | Show table structure |
| `csv_import <file> <table>` | Import CSV with auto-mapping |
| `csv_import <file> <table> --create-table` | Auto-create table from CSV |
| `exit` | Quit the CLI |

### MySQL CLI Specific

| Command | Description |
|---------|-------------|
| `use <database>` | Switch to database |
| `show processlist` | Show running processes |
| `show status` | Show server status |
| `show variables` | Show system variables |
| `mysqldump <db> <file>` | Export database |

### Multi-Database CLI Specific

| Command | Description |
|---------|-------------|
| Database selection during startup | `dbcli mysql\|postgresql\|sqlite\|duckdb` |
| Universal commands | Work across all database types |
| Consistent interface | Same commands, different engines |

## 🛠 Advanced Usage

### CSV Import Examples

```bash
# Basic import with auto-mapping
csv_import sales_data.csv products

# Create table automatically from CSV structure
csv_import customer_data.csv customers --create-table

# Large file with custom chunk size
csv_import big_dataset.csv orders --chunk-size=5000

# With custom column mapping file
csv_import data.csv table --mapping=columns.json
```

### Scripting and Automation

```bash
# Execute single queries
mysql -u root -p "SELECT COUNT(*) FROM users WHERE active=1"

# Pipe SQL files
cat schema.sql | mysql -u root -p

# Environment variables for connection
export MYSQL_HOST=prod-server
export MYSQL_USER=admin
mysql -H $MYSQL_HOST -u $MYSQL_USER -p

# Batch processing
for db in db1 db2 db3; do
    mysql -u root -p -d $db "OPTIMIZE TABLE users"
done
```

### Performance Monitoring

```bash
# MySQL performance analysis
mysql> show status like 'connections';
mysql> show variables like 'max_connections';
mysql> show processlist;

# DuckDB analytics performance
duckdb> PRAGMA threads=4;
duckdb> EXPLAIN SELECT * FROM large_table WHERE date > '2024-01-01';
```

## 🔧 Troubleshooting

### Connection Issues

**MySQL Connection Failed:**
```bash
# Check if MySQL is running
mysql -H localhost -u root -p --ssl-disabled

# Test with different port
mysql -H localhost -P 3307 -u root -p
```

**PostgreSQL Connection Failed:**
```bash
# Verify connection parameters
dbcli postgresql -H localhost -P 5432 -u postgres -p

# Check if PostgreSQL is accepting connections
```

### Import Issues

**CSV Import Failed:**
```bash
# Check file permissions
ls -la data.csv

# Test with smaller chunk size
csv_import data.csv table --chunk-size=1000

# Create table manually first
CREATE TABLE test (id INT, name VARCHAR(255));
csv_import data.csv test
```

**Type Conversion Errors:**
```bash
# Use --create-table for automatic type inference
csv_import data.csv table --create-table

# Check CSV data format
head -5 data.csv
```

## 📈 Performance Tips

### Large Dataset Handling

1. **Use appropriate chunk sizes**: Start with 1000, increase for better performance
2. **Create indexes after import**: Faster bulk loading without indexes
3. **Use DuckDB for analytics**: Optimized for analytical workloads
4. **Monitor memory usage**: Adjust chunk size based on available RAM

### Database-Specific Optimizations

**MySQL:**
- Use `--ssl-disabled` for local connections (faster)
- Set `innodb_buffer_pool_size` appropriately
- Use `LOAD DATA INFILE` for very large files

**PostgreSQL:**
- Increase `shared_buffers` for better performance
- Use `COPY` command for bulk imports
- Consider connection pooling for multiple imports

**DuckDB:**
- Perfect for read-heavy analytical workloads
- Automatically optimizes for columnar storage
- Excellent performance with Parquet files

## 🏢 Enterprise Features

### Security
- SSL/TLS connections supported
- No credential storage in binaries
- Password prompting for interactive use

### Monitoring
- Connection health checks
- Performance metrics display
- Process monitoring capabilities

### Backup & Recovery
- Integrated mysqldump support
- Cross-database data migration
- CSV export capabilities
- Automated backup scripting

### Compliance
- Audit trail through command history
- Secure connection protocols
- Role-based access (database level)
- Data privacy protection

## 🔐 Security Best Practices

### Connection Security
```bash
# Use SSL connections (enabled by default)
mysql -H prod-server -u admin -p

# Disable SSL only for local development
mysql -H localhost -u root -p --ssl-disabled

# Use environment variables for automation
export MYSQL_PASSWORD="secure_password"
mysql -H server -u admin -p
```

### Access Control
```bash
# Check user privileges
mysql> SHOW GRANTS FOR 'username'@'host';

# Create read-only user for analytics
mysql> CREATE USER 'analyst'@'%' IDENTIFIED BY 'password';
mysql> GRANT SELECT ON analytics.* TO 'analyst'@'%';
```

## 📊 Integration Examples

### Data Pipeline Integration

```bash
#!/bin/bash
# ETL Pipeline Example

# Extract from PostgreSQL
dbcli postgresql -H source-db -u etl -p -d warehouse << EOF
\copy (SELECT * FROM raw_data WHERE updated_at > '2024-01-01') TO '/tmp/extract.csv' CSV HEADER;
EOF

# Transform and Load into MySQL
mysql -u etl -p -d production << EOF
csv_import /tmp/extract.csv processed_data --create-table
EOF

# Analytics with DuckDB
dbcli duckdb -f analytics.db << EOF
CREATE TABLE daily_metrics AS
SELECT date_trunc('day', timestamp) as day,
       COUNT(*) as records,
       AVG(value) as avg_value
FROM '/tmp/extract.csv'
GROUP BY day;
EOF
```

### Business Intelligence

```bash
# Generate daily reports
mysql -u reporting -p -d analytics "
SELECT
    DATE(created_at) as date,
    COUNT(*) as new_customers,
    SUM(revenue) as daily_revenue
FROM customer_orders
WHERE created_at >= CURDATE() - INTERVAL 7 DAY
GROUP BY DATE(created_at)
ORDER BY date DESC
" > daily_report.csv

# Load into analytics database
dbcli duckdb -f bi_warehouse.db
duckdb> csv_import daily_report.csv daily_metrics --create-table
```

## 🤖 Automation Scripts

### Backup Automation

```bash
#!/bin/bash
# automated_backup.sh

BACKUP_DIR="/backups/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# Backup all databases
for db in production staging analytics; do
    echo "Backing up $db..."
    mysql -u backup -p "$db" > "$BACKUP_DIR/${db}_$(date +%H%M).sql"
done

# Compress backups
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"

echo "✓ Backups completed: $BACKUP_DIR.tar.gz"
```

### Health Monitoring

```bash
#!/bin/bash
# health_check.sh

# Check MySQL health
mysql -u monitor -p << EOF
SELECT
    'MySQL Status' as check_type,
    IF(@@read_only = 0, 'READ-WRITE', 'READ-ONLY') as status,
    CONCAT(ROUND(
        (SELECT SUM(data_length + index_length) / 1024 / 1024 / 1024
         FROM information_schema.tables), 2), ' GB') as total_size;
EOF

# Check PostgreSQL health
dbcli postgresql -H pg-server -u monitor -p -d postgres << EOF
SELECT
    'PostgreSQL Status' as check_type,
    pg_is_in_recovery() as is_replica,
    pg_size_pretty(pg_database_size('production')) as db_size;
EOF
```

## 📚 Documentation Links

### Official Documentation
- **MySQL**: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)
- **PostgreSQL**: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
- **SQLite**: [https://www.sqlite.org/docs.html](https://www.sqlite.org/docs.html)
- **DuckDB**: [https://duckdb.org/docs/](https://duckdb.org/docs/)

### Ambivo Resources
- **Company**: [https://www.ambivo.com](https://www.ambivo.com)
- **Support**: sgosain@ambivo.com
- **GitHub**: [https://github.com/sgosain/ambivo-db-cli](https://github.com/sgosain/ambivo-db-cli)
- **Issues**: [Report Issues](https://github.com/sgosain/ambivo-db-cli/issues)

## 🎯 Use Cases

### Development Teams
- **Local Development**: SQLite for rapid prototyping
- **Integration Testing**: PostgreSQL for realistic testing
- **Performance Testing**: MySQL for production simulation
- **Data Analysis**: DuckDB for development analytics

### Data Teams
- **ETL Pipelines**: Multi-database connectivity
- **Analytics**: DuckDB for fast analytical queries
- **Data Migration**: Cross-database data movement
- **Reporting**: Automated report generation

### DevOps Teams
- **Database Administration**: Professional CLI tools
- **Monitoring**: Performance metrics and health checks
- **Backup Management**: Automated backup scripting
- **Deployment**: Database schema management

### Business Intelligence
- **Data Warehousing**: Multi-source data integration
- **Report Generation**: Automated business reporting
- **Analytics**: Fast analytical query processing
- **Dashboard Backends**: Data preparation for visualization

## 🏆 Why Choose Ambivo CLI Suite?

### vs. Standard Database CLIs
✅ **Unified Interface**: Same commands across different databases
✅ **Enhanced Features**: Professional table formatting, command history
✅ **Intelligent CSV Import**: Automatic type inference and column mapping
✅ **Cross-Platform**: Consistent experience on all operating systems
✅ **Enterprise Ready**: Professional error handling and guidance

### vs. GUI Database Tools
✅ **Lightweight**: No heavy GUI overhead or resource consumption
✅ **Scriptable**: Perfect for automation and DevOps workflows
✅ **SSH-Friendly**: Works seamlessly over remote connections
✅ **Version Control**: Database scripts work well with Git
✅ **Fast**: Immediate startup and execution

### vs. Other CLI Tools
✅ **Multi-Database**: Single tool suite for all database types
✅ **Backward Compatible**: Full MySQL cheat sheet compatibility
✅ **Modern Features**: Command history, tab completion, beautiful formatting
✅ **Professional**: Built by database experts for enterprise use
✅ **Open Source**: MIT license, free for commercial use

## 🔄 Updates and Versioning

### Staying Updated
```bash
# Check current version
mysql --version
dbcli --version

# Download latest binaries
curl -s https://api.github.com/repos/sgosain/ambivo-db-cli/releases/latest \
| grep browser_download_url \
| grep $(uname -s | tr '[:upper:]' '[:lower:]') \
| cut -d '"' -f 4 \
| wget -qi -
```

### Version History
- **v2.0.0**: Multi-database support, enhanced CSV import
- **v1.2.0**: Command history, tab completion, performance improvements
- **v1.0.0**: Initial MySQL CLI with cheat sheet compatibility

## 💬 Community and Support

### Getting Help
1. **Documentation**: Check this README and inline help commands
2. **GitHub Issues**: [Report bugs or request features](https://github.com/sgosain/ambivo-db-cli/issues)
3. **Email Support**: sgosain@ambivo.com
4. **Community**: [GitHub Discussions](https://github.com/sgosain/ambivo-db-cli/discussions)

### Contributing
We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Professional Support
For enterprise support, training, or custom development:
- **Email**: sgosain@ambivo.com
- **Company**: [Ambivo](https://www.ambivo.com)

## 📄 License

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

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

**Built with ❤️ by Hemant Gosain 'Sunny' at Ambivo**

*Professional database CLI tools for modern enterprises and developers*

[![Download Latest](https://img.shields.io/badge/Download-Latest%20Release-blue?style=for-the-badge)](https://github.com/sgosain/ambivo-db-cli/releases/latest)
[![Powered by Ambivo](https://img.shields.io/badge/Powered%20by-Ambivo-blue?style=for-the-badge)](https://www.ambivo.com)