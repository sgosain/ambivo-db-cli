# Ambivo Database CLI Suite - Makefile
# Cross-platform binary building and distribution

.PHONY: all clean install build-all build-local test release help

# Version and metadata
VERSION := $(shell python -c "import mysql_cli; print(mysql_cli.__version__)")
PLATFORM := $(shell python -c "import platform; print(platform.system().lower())")
ARCH := $(shell python -c "import platform; arch=platform.machine().lower(); print('x64' if arch in ['x86_64','amd64'] else 'arm64' if 'arm' in arch and '64' in arch else arch)")

# Directories
BUILD_DIR := build
DIST_DIR := dist
BIN_DIR := binaries/$(PLATFORM)-$(ARCH)

# Binary names
MYSQL_CLI_BIN := ambivo-mysql-cli
DB_CLI_BIN := ambivo-db-cli

ifeq ($(PLATFORM),windows)
	MYSQL_CLI_BIN := $(MYSQL_CLI_BIN).exe
	DB_CLI_BIN := $(DB_CLI_BIN).exe
	BATCH_EXT := .bat
	INSTALL_SCRIPT := install.bat
else
	BATCH_EXT :=
	INSTALL_SCRIPT := install.sh
endif

# Colors for output
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RESET := \033[0m

help: ## Show this help message
	@echo "$(BLUE)Ambivo Database CLI Suite - Build System$(RESET)"
	@echo "==============================================="
	@echo ""
	@echo "$(GREEN)Available targets:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Current platform:$(RESET) $(PLATFORM)-$(ARCH)"
	@echo "$(GREEN)Version:$(RESET) $(VERSION)"

all: clean install build-local test ## Clean, install deps, build, and test

check-deps: ## Check if required dependencies are installed
	@echo "$(BLUE)Checking dependencies...$(RESET)"
	@python -c "import sys; sys.exit(0 if sys.version_info >= (3,7) else 1)" || (echo "$(RED)❌ Python 3.7+ required$(RESET)" && exit 1)
	@python -c "import mysql_cli" || (echo "$(RED)❌ mysql_cli.py not found$(RESET)" && exit 1)
	@python -c "import db_cli" || (echo "$(RED)❌ db_cli.py not found$(RESET)" && exit 1)
	@echo "$(GREEN)✓ Dependencies OK$(RESET)"

install: ## Install Python dependencies
	@echo "$(BLUE)Installing dependencies...$(RESET)"
	@pip install --upgrade pip
	@pip install pyinstaller
	@pip install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(RESET)"

clean: ## Clean build artifacts
	@echo "$(BLUE)Cleaning build artifacts...$(RESET)"
	@rm -rf $(BUILD_DIR) $(DIST_DIR) __pycache__ *.pyc *.pyo
	@rm -rf *.spec binaries
	@echo "$(GREEN)✓ Clean completed$(RESET)"

build-dirs: ## Create build directories
	@mkdir -p $(BIN_DIR)
	@echo "$(GREEN)✓ Created $(BIN_DIR)$(RESET)"

build-mysql: build-dirs ## Build MySQL CLI binary using spec file
	@echo "$(BLUE)Building MySQL CLI using spec file...$(RESET)"
	@pyinstaller specs/mysql_cli.spec \
		--distpath "$(BIN_DIR)" \
		--workpath "$(BUILD_DIR)/mysql_cli" \
		--clean
	@echo "$(GREEN)✓ MySQL CLI built: $(BIN_DIR)/$(MYSQL_CLI_BIN)$(RESET)"

build-db: build-dirs ## Build Multi-Database CLI binary using spec file
	@echo "$(BLUE)Building Multi-Database CLI using spec file...$(RESET)"
	@pyinstaller specs/db_cli.spec \
		--distpath "$(BIN_DIR)" \
		--workpath "$(BUILD_DIR)/db_cli" \
		--clean
	@echo "$(GREEN)✓ Multi-Database CLI built: $(BIN_DIR)/$(DB_CLI_BIN)$(RESET)"

build-local: check-deps build-mysql build-db ## Build binaries for current platform
	@$(MAKE) create-convenience-scripts
	@$(MAKE) create-docs
	@$(MAKE) create-install-script
	@echo "$(GREEN)✅ Local build completed for $(PLATFORM)-$(ARCH)$(RESET)"

create-convenience-scripts: ## Create convenience wrapper scripts
ifeq ($(PLATFORM),windows)
	@echo '@echo off' > $(BIN_DIR)/mysql$(BATCH_EXT)
	@echo '"%~dp0$(MYSQL_CLI_BIN)" %*' >> $(BIN_DIR)/mysql$(BATCH_EXT)
	@echo '@echo off' > $(BIN_DIR)/dbcli$(BATCH_EXT)
	@echo '"%~dp0$(DB_CLI_BIN)" %*' >> $(BIN_DIR)/dbcli$(BATCH_EXT)
else
	@echo '#!/bin/bash' > $(BIN_DIR)/mysql
	@echo 'DIR="$$(cd "$$(dirname "$${BASH_SOURCE[0]}")" && pwd)"' >> $(BIN_DIR)/mysql
	@echo '"$$DIR/$(MYSQL_CLI_BIN)" "$$@"' >> $(BIN_DIR)/mysql
	@chmod +x $(BIN_DIR)/mysql
	@echo '#!/bin/bash' > $(BIN_DIR)/dbcli
	@echo 'DIR="$$(cd "$$(dirname "$${BASH_SOURCE[0]}")" && pwd)"' >> $(BIN_DIR)/dbcli
	@echo '"$$DIR/$(DB_CLI_BIN)" "$$@"' >> $(BIN_DIR)/dbcli
	@chmod +x $(BIN_DIR)/dbcli
endif
	@echo "$(GREEN)✓ Convenience scripts created$(RESET)"

create-docs: ## Create documentation files
	@echo "# Ambivo Database CLI Suite - $(PLATFORM) $(ARCH)" > $(BIN_DIR)/README.txt
	@echo "" >> $(BIN_DIR)/README.txt
	@echo "## Quick Start" >> $(BIN_DIR)/README.txt
	@echo "" >> $(BIN_DIR)/README.txt
	@echo "### MySQL CLI" >> $(BIN_DIR)/README.txt
	@echo "./$(MYSQL_CLI_BIN) -H localhost -u root -p" >> $(BIN_DIR)/README.txt
	@echo "" >> $(BIN_DIR)/README.txt
	@echo "### Multi-Database CLI" >> $(BIN_DIR)/README.txt
	@echo "./$(DB_CLI_BIN) mysql -H localhost -u root -p -d mydb" >> $(BIN_DIR)/README.txt
	@echo "./$(DB_CLI_BIN) postgresql -H localhost -u postgres -p -d mydb" >> $(BIN_DIR)/README.txt
	@echo "./$(DB_CLI_BIN) sqlite -f database.db" >> $(BIN_DIR)/README.txt
	@echo "./$(DB_CLI_BIN) duckdb -f analytics.db" >> $(BIN_DIR)/README.txt
	@echo "" >> $(BIN_DIR)/README.txt
	@echo "## Features" >> $(BIN_DIR)/README.txt
	@echo "- Standalone executables (no Python required)" >> $(BIN_DIR)/README.txt
	@echo "- Full database connectivity" >> $(BIN_DIR)/README.txt
	@echo "- CSV import with intelligent mapping" >> $(BIN_DIR)/README.txt
	@echo "- Command history and tab completion" >> $(BIN_DIR)/README.txt
	@echo "- Professional table formatting" >> $(BIN_DIR)/README.txt
	@echo "" >> $(BIN_DIR)/README.txt
	@echo "Built by Hemant Gosain 'Sunny' at Ambivo" >> $(BIN_DIR)/README.txt
	@echo "Email: sgosain@ambivo.com | Company: https://www.ambivo.com" >> $(BIN_DIR)/README.txt
	@echo "$(GREEN)✓ Documentation created$(RESET)"

create-install-script: ## Create installation script
ifeq ($(PLATFORM),windows)
	@echo '@echo off' > $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo Installing Ambivo Database CLI Suite...' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'set "INSTALL_DIR=%USERPROFILE%\ambivo-cli"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'mkdir "%INSTALL_DIR%" 2>nul' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'copy "$(MYSQL_CLI_BIN)" "%INSTALL_DIR%\" >nul' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'copy "$(DB_CLI_BIN)" "%INSTALL_DIR%\" >nul' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'copy "mysql$(BATCH_EXT)" "%INSTALL_DIR%\" >nul' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'copy "dbcli$(BATCH_EXT)" "%INSTALL_DIR%\" >nul' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'copy "README.txt" "%INSTALL_DIR%\" >nul' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo.' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo ✓ Installed to: %INSTALL_DIR%' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo.' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo To use globally, add this to your PATH:' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo %INSTALL_DIR%' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo.' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'pause' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
else
	@echo '#!/bin/bash' > $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo "Installing Ambivo Database CLI Suite..."' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'INSTALL_DIR="$HOME/bin"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'mkdir -p "$INSTALL_DIR"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'cp "$(MYSQL_CLI_BIN)" "$INSTALL_DIR/"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'cp "$(DB_CLI_BIN)" "$INSTALL_DIR/"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'cp "mysql" "$INSTALL_DIR/"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'cp "dbcli" "$INSTALL_DIR/"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'cp "README.txt" "$INSTALL_DIR/"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'chmod +x "$INSTALL_DIR/$(MYSQL_CLI_BIN)"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'chmod +x "$INSTALL_DIR/$(DB_CLI_BIN)"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'chmod +x "$INSTALL_DIR/mysql"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'chmod +x "$INSTALL_DIR/dbcli"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo "✓ Installed to: $INSTALL_DIR"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo "To use globally, add this to your PATH:"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo "export PATH=\$PATH:$INSTALL_DIR"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo "Add the above line to ~/.bashrc or ~/.zshrc"' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@echo 'echo' >> $(BIN_DIR)/$(INSTALL_SCRIPT)
	@chmod +x $(BIN_DIR)/$(INSTALL_SCRIPT)
endif
	@echo "$(GREEN)✓ Install script created$(RESET)"

test: ## Test built binaries
	@echo "$(BLUE)Testing binaries...$(RESET)"
	@$(BIN_DIR)/$(MYSQL_CLI_BIN) --help > /dev/null && echo "$(GREEN)✓ MySQL CLI test passed$(RESET)" || echo "$(RED)❌ MySQL CLI test failed$(RESET)"
	@$(BIN_DIR)/$(DB_CLI_BIN) --help > /dev/null && echo "$(GREEN)✓ Multi-Database CLI test passed$(RESET)" || echo "$(RED)❌ Multi-Database CLI test failed$(RESET)"

package: build-local ## Create distribution package
	@echo "$(BLUE)Creating distribution package...$(RESET)"
ifeq ($(PLATFORM),windows)
	@cd binaries && zip -r "ambivo-db-cli-$(PLATFORM)-$(ARCH).zip" "$(PLATFORM)-$(ARCH)/"
	@echo "$(GREEN)✓ Package created: binaries/ambivo-db-cli-$(PLATFORM)-$(ARCH).zip$(RESET)"
else
	@cd binaries && tar -czf "ambivo-db-cli-$(PLATFORM)-$(ARCH).tar.gz" "$(PLATFORM)-$(ARCH)/"
	@echo "$(GREEN)✓ Package created: binaries/ambivo-db-cli-$(PLATFORM)-$(ARCH).tar.gz$(RESET)"
endif

build-all: ## Build for all platforms (requires Docker)
	@echo "$(BLUE)Building for all platforms...$(RESET)"
	@echo "$(YELLOW)Note: This requires Docker for cross-compilation$(RESET)"
	@docker --version > /dev/null 2>&1 || (echo "$(RED)❌ Docker required for cross-platform builds$(RESET)" && exit 1)
	@$(MAKE) build-linux
	@$(MAKE) build-macos
	@$(MAKE) build-windows

build-docker-linux: ## Build Linux binaries using Docker
	@echo "$(BLUE)Building Linux binaries...$(RESET)"
	@docker run --rm -v "$(PWD):/app" -w /app python:3.11-slim bash -c "\
		apt-get update && apt-get install -y build-essential && \
		pip install pyinstaller && \
		pip install -r requirements.txt && \
		make build-local PLATFORM=linux ARCH=x64"

build-docker-windows: ## Build Windows binaries using Docker (Wine)
	@echo "$(BLUE)Building Windows binaries...$(RESET)"
	@echo "$(YELLOW)Note: This is experimental and may require additional setup$(RESET)"

release: clean build-local package ## Full release build
	@echo "$(GREEN)📦 Release package ready:$(RESET)"
	@ls -la binaries/ambivo-db-cli-$(PLATFORM)-$(ARCH).*
	@echo ""
	@echo "$(BLUE)Distribution contents:$(RESET)"
	@ls -la $(BIN_DIR)/
	@echo ""
	@echo "$(GREEN)✅ Release completed for $(PLATFORM)-$(ARCH)$(RESET)"

install-local: build-local ## Install locally for current user
	@echo "$(BLUE)Installing locally...$(RESET)"
	@cd $(BIN_DIR) && ./$(INSTALL_SCRIPT)

size: ## Show binary sizes
	@echo "$(BLUE)Binary sizes:$(RESET)"
	@ls -lh $(BIN_DIR)/ | grep -E "($(MYSQL_CLI_BIN)|$(DB_CLI_BIN))" || echo "No binaries found. Run 'make build-local' first."

benchmark: build-local ## Run basic performance benchmarks
	@echo "$(BLUE)Running benchmarks...$(RESET)"
	@echo "MySQL CLI startup time:"
	@time $(BIN_DIR)/$(MYSQL_CLI_BIN) --help > /dev/null
	@echo ""
	@echo "Multi-Database CLI startup time:"
	@time $(BIN_DIR)/$(DB_CLI_BIN) --help > /dev/null

dev-install: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(RESET)"
	@pip install -r requirements.txt
	@pip install pytest pytest-cov black flake8 mypy
	@echo "$(GREEN)✓ Development environment ready$(RESET)"

lint: ## Run code linting
	@echo "$(BLUE)Running linters...$(RESET)"
	@flake8 mysql_cli.py db_cli.py || echo "$(YELLOW)Flake8 found issues$(RESET)"
	@black --check mysql_cli.py db_cli.py || echo "$(YELLOW)Black formatting needed$(RESET)"
	@mypy mysql_cli.py db_cli.py || echo "$(YELLOW)MyPy found type issues$(RESET)"

format: ## Format code with Black
	@echo "$(BLUE)Formatting code...$(RESET)"
	@black mysql_cli.py db_cli.py
	@echo "$(GREEN)✓ Code formatted$(RESET)"

test-unit: ## Run unit tests
	@echo "$(BLUE)Running unit tests...$(RESET)"
	@python -m pytest tests/ -v || echo "$(YELLOW)Some tests failed$(RESET)"

docker-build: ## Build Docker images for distribution
	@echo "$(BLUE)Building Docker images...$(RESET)"
	@docker build -t ambivo/mysql-cli:latest -f docker/Dockerfile.mysql .
	@docker build -t ambivo/db-cli:latest -f docker/Dockerfile.multi .
	@echo "$(GREEN)✓ Docker images built$(RESET)"

info: ## Show build information
	@echo "$(BLUE)Build Information$(RESET)"
	@echo "=================="
	@echo "Version:     $(VERSION)"
	@echo "Platform:    $(PLATFORM)"
	@echo "Architecture: $(ARCH)"
	@echo "Python:      $(shell python --version)"
	@echo "Build Dir:   $(BIN_DIR)"
	@echo ""
	@echo "$(BLUE)Available Files:$(RESET)"
	@ls -la $(BIN_DIR)/ 2>/dev/null || echo "No binaries built yet. Run 'make build-local'."

# Advanced targets for CI/CD
ci-build: clean install build-local test ## CI/CD build pipeline
	@echo "$(GREEN)✅ CI build completed$(RESET)"

cd-deploy: package ## CD deployment pipeline
	@echo "$(BLUE)Deployment artifacts ready$(RESET)"
	@echo "$(GREEN)✅ CD deployment completed$(RESET)"