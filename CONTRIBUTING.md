# Contributing to DIGIPIN

Thank you for contributing to India's official geocoding standard implementation!

## Quick Start

```bash
git clone https://github.com/DEADSERPENT/digipin.git
cd digipin

# Using Makefile (recommended)
make install    # Install all dependencies
make test       # Run all tests
make lint       # Lint all code
make help       # See all commands

# Or manually
cd python && pip install -e ".[dev]"    # Python
cd javascript && npm install            # JavaScript
```

## Workflow

1. **Fork & Branch** from `main`
2. **Make Changes** following standards below
3. **Add Tests** for new features
4. **Run** `make verify` (tests + linting)
5. **Submit PR** with clear description

## Standards

**Python:** PEP 8, type hints, docstrings, `make python-lint`
**JavaScript:** ES6+, TypeScript definitions, `make js-lint`

## Testing

```bash
make test              # All tests
make python-test-cov   # Python with coverage
make js-test           # JavaScript tests
```

**Critical:** Changes must maintain 100% compliance with `docs/technical_spec.md`

## Pull Requests

- Clear, descriptive title
- Keep focused (one feature/fix)
- All CI checks must pass
- Maintainer approval required (auto-requested)

**Questions?** [Issues](https://github.com/DEADSERPENT/digipin/issues) • [Discussions](https://github.com/DEADSERPENT/digipin/discussions)

**Maintainers:** SAMARTHA H V, MR SHIVAKUMAR
