# DIGIPIN Monorepo Makefile
# Unified commands for Python and JavaScript development

.PHONY: help install test lint clean build publish \
        python-install python-test python-lint python-build python-publish \
        js-install js-test js-lint js-build js-publish \
        all-install all-test all-lint all-clean

# Default target
.DEFAULT_GOAL := help

# Colors for terminal output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ General

help: ## Display this help message
	@echo "$(BLUE)DIGIPIN Monorepo - Available Commands$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make $(GREEN)<target>$(NC)\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Installation

install: all-install ## Install all dependencies (Python + JavaScript)

python-install: ## Install Python dependencies
	@echo "$(BLUE)Installing Python dependencies...$(NC)"
	cd python && pip install -e ".[dev]"
	@echo "$(GREEN)✓ Python dependencies installed$(NC)"

js-install: ## Install JavaScript dependencies
	@echo "$(BLUE)Installing JavaScript dependencies...$(NC)"
	cd javascript && npm install
	@echo "$(GREEN)✓ JavaScript dependencies installed$(NC)"

all-install: python-install js-install ## Install all dependencies

##@ Testing

test: all-test ## Run all tests (Python + JavaScript)

python-test: ## Run Python tests
	@echo "$(BLUE)Running Python tests...$(NC)"
	cd python && pytest tests/ -v
	@echo "$(GREEN)✓ Python tests complete$(NC)"

python-test-cov: ## Run Python tests with coverage
	@echo "$(BLUE)Running Python tests with coverage...$(NC)"
	cd python && pytest tests/ -v --cov=src/digipin --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Coverage report: python/htmlcov/index.html$(NC)"

js-test: ## Run JavaScript tests
	@echo "$(BLUE)Running JavaScript tests...$(NC)"
	cd javascript && npm test
	@echo "$(GREEN)✓ JavaScript tests complete$(NC)"

all-test: python-test js-test ## Run all tests

test-vectors: ## Validate shared test vectors against both implementations
	@echo "$(BLUE)Validating shared test vectors...$(NC)"
	@echo "$(YELLOW)Note: Test vector validation requires custom scripts$(NC)"
	@echo "See tests/data/test_vectors.json for test cases"

##@ Code Quality

lint: all-lint ## Run all linters (Python + JavaScript)

python-lint: ## Run Python linters (black, flake8, mypy)
	@echo "$(BLUE)Running Python linters...$(NC)"
	cd python && black --check src/digipin tests/
	cd python && flake8 src/digipin tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
	cd python && mypy src/digipin --ignore-missing-imports
	@echo "$(GREEN)✓ Python linting complete$(NC)"

python-format: ## Format Python code with black
	@echo "$(BLUE)Formatting Python code...$(NC)"
	cd python && black src/digipin tests/
	@echo "$(GREEN)✓ Python code formatted$(NC)"

js-lint: ## Run JavaScript linter
	@echo "$(BLUE)Checking JavaScript syntax...$(NC)"
	cd javascript && node -c digipin.js
	cd javascript && node -c test.js
	cd javascript && node -c example.js
	@echo "$(GREEN)✓ JavaScript syntax valid$(NC)"

all-lint: python-lint js-lint ## Run all linters

##@ Building

build: all-build ## Build all packages (Python + JavaScript)

python-build: ## Build Python package
	@echo "$(BLUE)Building Python package...$(NC)"
	cd python && pip install --upgrade build && python -m build
	@echo "$(GREEN)✓ Python package built: python/dist/$(NC)"

js-build: ## Verify JavaScript package
	@echo "$(BLUE)Verifying JavaScript package...$(NC)"
	cd javascript && npm pack --dry-run
	@echo "$(GREEN)✓ JavaScript package verified$(NC)"

all-build: python-build js-build ## Build all packages

##@ Publishing

publish-check: ## Check packages before publishing
	@echo "$(BLUE)Checking Python package...$(NC)"
	@# REFINEMENT 1: Only install twine if missing (keeps env clean)
	cd python && (python -m pip show twine > /dev/null 2>&1 || pip install twine) && twine check dist/*
	@echo "$(BLUE)Checking JavaScript package...$(NC)"
	cd javascript && npm pack --dry-run
	@echo "$(GREEN)✓ Packages ready for publishing$(NC)"

python-publish: ## Publish Python package to PyPI
	@echo "$(RED)Publishing to PyPI...$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		cd python && twine upload dist/*; \
		echo "$(GREEN)✓ Published to PyPI$(NC)"; \
	else \
		echo "$(YELLOW)Cancelled$(NC)"; \
	fi

python-publish-test: ## Publish Python package to Test PyPI
	@echo "$(BLUE)Publishing to Test PyPI...$(NC)"
	cd python && twine upload --repository testpypi dist/*
	@echo "$(GREEN)✓ Published to Test PyPI$(NC)"

js-publish: ## Publish JavaScript package to NPM
	@echo "$(RED)Publishing to NPM...$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		cd javascript && npm publish --access public; \
		echo "$(GREEN)✓ Published to NPM$(NC)"; \
	else \
		echo "$(YELLOW)Cancelled$(NC)"; \
	fi

##@ Cleanup

clean: all-clean ## Clean all build artifacts

python-clean: ## Clean Python build artifacts
	@echo "$(BLUE)Cleaning Python artifacts...$(NC)"
	@# REFINEMENT 3: Robust cleanup (works on all shells, suppresses errors)
	cd python && rm -rf build/ dist/ src/*.egg-info .pytest_cache htmlcov/ .coverage 2>/dev/null || true
	find python -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Python artifacts cleaned$(NC)"

js-clean: ## Clean JavaScript build artifacts
	@echo "$(BLUE)Cleaning JavaScript artifacts...$(NC)"
	@# REFINEMENT 3: Robust cleanup (works on WSL/Linux/macOS, suppresses errors)
	cd javascript && rm -rf *.tgz 2>/dev/null || true
	cd javascript && rm -rf node_modules/ 2>/dev/null || true
	@echo "$(GREEN)✓ JavaScript artifacts cleaned$(NC)"

all-clean: python-clean js-clean ## Clean all artifacts

##@ Development

dev-python: ## Start Python development environment
	@echo "$(BLUE)Starting Python development...$(NC)"
	cd python && pip install -e ".[dev]"
	@echo "$(GREEN)✓ Python dev environment ready$(NC)"
	@echo "Try: cd python && pytest tests/ -v"

dev-js: ## Start JavaScript development environment
	@echo "$(BLUE)Starting JavaScript development...$(NC)"
	cd javascript && npm install
	@echo "$(GREEN)✓ JavaScript dev environment ready$(NC)"
	@echo "Try: cd javascript && npm test"

examples: ## Run all examples
	@echo "$(BLUE)Running Python examples...$(NC)"
	cd python/examples && python basic_usage.py
	@echo ""
	@echo "$(BLUE)Running JavaScript examples...$(NC)"
	cd javascript && node example.js

benchmark: ## Run Python benchmarks
	@echo "$(BLUE)Running Python benchmarks...$(NC)"
	cd python/benchmarks && python polyfill_comparison.py

##@ Git & CI

git-status: ## Show git status
	@git status

git-diff: ## Show git diff
	@git diff

commit: ## Interactive commit (guides through best practices)
	@echo "$(BLUE)Preparing commit...$(NC)"
	@echo "$(YELLOW)Modified files:$(NC)"
	@git status --short
	@echo ""
	@read -p "Commit message: " msg; \
	git add -A && git commit -m "$$msg"
	@echo "$(GREEN)✓ Committed$(NC)"

push: ## Push to remote
	@echo "$(BLUE)Pushing to remote...$(NC)"
	git push origin main
	@echo "$(GREEN)✓ Pushed to remote$(NC)"

ci-local: all-test all-lint ## Run CI checks locally (tests + lint)
	@echo "$(GREEN)✓ All CI checks passed locally$(NC)"

##@ Documentation

docs: ## Open documentation
	@echo "$(BLUE)Opening documentation...$(NC)"
	@if command -v xdg-open > /dev/null; then \
		xdg-open README.md; \
	elif command -v open > /dev/null; then \
		open README.md; \
	elif command -v start > /dev/null; then \
		start README.md; \
	else \
		echo "$(YELLOW)Please open README.md manually$(NC)"; \
	fi

docs-build: ## Build documentation (if applicable)
	@echo "$(YELLOW)Documentation is in Markdown format$(NC)"
	@echo "See: README.md, python/README.md, javascript/README.md"

##@ Quick Actions

quick-test: ## Quick test (fast subset)
	@echo "$(BLUE)Running quick tests...$(NC)"
	cd python && pytest tests/test_encoder.py tests/test_decoder.py -v
	cd javascript && npm test
	@echo "$(GREEN)✓ Quick tests complete$(NC)"

verify: ci-local ## Verify everything before commit
	@echo "$(GREEN)✓ Ready to commit$(NC)"

info: ## Display repository information
	@echo "$(BLUE)DIGIPIN Repository Information$(NC)"
	@echo ""
	@echo "$(GREEN)Repository:$(NC) github.com/DEADSERPENT/digipin"
	@echo "$(GREEN)Structure:$(NC)  Monorepo (Python + JavaScript)"
	@echo ""
	@echo "$(YELLOW)Python Package:$(NC)"
	@echo "  Name:     digipinpy"
	@echo "  Location: python/"
	@echo "  PyPI:     pypi.org/project/digipinpy"
	@echo ""
	@echo "$(YELLOW)JavaScript Package:$(NC)"
	@echo "  Name:     digipinjs-lib"
	@echo "  Location: javascript/"
	@echo "  NPM:      npmjs.com/package/digipinjs-lib"
	@echo ""
	@echo "Run 'make help' for all available commands"
