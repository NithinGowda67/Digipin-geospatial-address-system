# Build & Release Guide

This guide explains how to build, test, and release DIGIPIN-Py to PyPI.

## Prerequisites

```bash
pip install --upgrade pip setuptools wheel build twine
```

## Local Development Build

### 1. Install in Development Mode

```bash
# Install with all development dependencies
pip install -e ".[dev]"

# Or with specific extras
pip install -e ".[test]"      # Testing only
pip install -e ".[pandas]"    # Pandas integration
pip install -e ".[performance]"  # With Cython optimization (10-15x faster)
```

### 1a. Build with Cython Optimization (Recommended for Production)

For **10-15x performance improvement**, compile the Cython extension:

```bash
# Install Cython and build tools
pip install cython

# Build the C extension
python setup.py build_ext --inplace

# Install in development mode
pip install -e ".[dev]"

# Verify Cython backend is active
python -c "import digipin; print(digipin.get_backend_info())"
# Should show: {'backend': 'cython', 'performance': '10-15x', ...}
```

**Note:** Requires a C compiler:
- **Linux**: `gcc` (usually pre-installed)
- **macOS**: Xcode Command Line Tools (`xcode-select --install`)
- **Windows**: Microsoft Visual C++ 14.0+ ([Download](https://visualstudio.microsoft.com/visual-cpp-build-tools/))

See [Performance Optimization Guide](performance-optimization.md) for details.

### 2. Verify Installation

```python
import digipin
print(digipin.__version__)  # Should print: 1.1.0

# Test basic functionality
from digipin import encode, decode
code = encode(28.622788, 77.213033)
print(code)  # Should print: 39J49LL8T4
```

## Testing

### Run All Tests

```bash
# Basic test run
pytest tests/ -v

# With coverage report
pytest tests/ --cov=src/digipin --cov-report=term --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

### Code Quality Checks

```bash
# Format code with Black
black src/digipin tests/

# Check code style with flake8
flake8 src/digipin tests/ --max-line-length=88

# Type checking with mypy
mypy src/digipin --ignore-missing-imports
```

## Building the Package

### 1. Clean Previous Builds

```bash
# Windows
rmdir /s /q build dist src\digipinpy.egg-info

# Unix/macOS/Linux
rm -rf build/ dist/ src/digipinpy.egg-info/
```

### 2. Build Distribution Files

#### Option A: Pure Python Build (Universal Wheel)

```bash
python -m build
```

This creates:
- `dist/digipinpy-1.7.0-py3-none-any.whl` (pure Python wheel - works everywhere)
- `dist/digipinpy-1.7.0.tar.gz` (source distribution)

#### Option B: Build with Cython Extension (Platform-Specific Wheel)

For maximum performance, build platform-specific wheels with Cython:

```bash
# Install Cython
pip install cython

# Build wheel with C extension
python setup.py bdist_wheel

# This creates a platform-specific wheel like:
# - dist/digipinpy-1.8.0-cp311-cp311-linux_x86_64.whl (Linux)
# - dist/digipinpy-1.8.0-cp311-cp311-macosx_10_9_x86_64.whl (macOS)
# - dist/digipinpy-1.8.0-cp311-cp311-win_amd64.whl (Windows)
```

**When to use which:**
- **Pure Python**: For maximum compatibility across platforms
- **Cython wheel**: For production deployments needing 10-15x performance

### 3. Verify Package Contents

```bash
# Check package metadata
twine check dist/*

# List contents of wheel
python -m zipfile -l dist/digipinpy-1.8.0-py3-none-any.whl

# List contents of source distribution
tar -tzf dist/digipinpy-1.8.0.tar.gz  # Unix/macOS
```

Expected structure in wheel:
```
digipin/
├── __init__.py
├── encoder.py
├── decoder.py
├── neighbors.py
├── utils.py
├── cli.py
├── pandas_ext.py
└── py.typed
```

## Testing the Build

### Test Installation from Built Package

```bash
# Create a clean virtual environment
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# Install from the built wheel
pip install dist/digipinpy-1.8.0-py3-none-any.whl

# Test import and functionality
python -c "from digipin import encode; print(encode(28.622788, 77.213033))"

# Cleanup
deactivate
rm -rf test_env  # Windows: rmdir /s /q test_env
```

## Publishing to PyPI

### Test on PyPI Test Server (Recommended First)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ digipinpy
```

### Publish to Production PyPI

**Prerequisites:**
1. Create account on [PyPI](https://pypi.org/account/register/)
2. Create API token at https://pypi.org/manage/account/token/
3. Configure `.pypirc` (or use `TWINE_USERNAME` and `TWINE_PASSWORD` env vars)

```bash
# Option 1: Using API token
twine upload dist/* -u __token__ -p pypi-YOUR-API-TOKEN

# Option 2: Using .pypirc configuration
twine upload dist/*
```

### Verify Published Package

```bash
# Check package page
open https://pypi.org/project/digipinpy/

# Test installation
pip install digipinpy

# Verify version
python -c "import digipin; print(digipin.__version__)"
```

## Release Checklist

Before creating a new release:

- [ ] Update version in `src/digipin/__init__.py`
- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md` with release notes
- [ ] Run all tests: `pytest tests/ -v`
- [ ] Run code quality checks: `black`, `flake8`, `mypy`
- [ ] Build pure Python package: `python -m build`
- [ ] Build Cython wheels (optional): `python setup.py bdist_wheel`
- [ ] Check the build: `twine check dist/*`
- [ ] Test installation locally (both Python and Cython)
- [ ] Run performance benchmark: `python benchmarks/cython_performance.py`
- [ ] Commit all changes
- [ ] Create Git tag: `git tag -a v1.8.0 -m "Release v1.8.0"`
- [ ] Push tag: `git push origin v1.8.0`
- [ ] Upload to PyPI: `twine upload dist/*`
- [ ] Create GitHub Release with changelog
- [ ] Verify installation: `pip install digipinpy --upgrade`

## Automated Release via GitHub Actions

The repository includes GitHub Actions workflows for automated publishing:

1. **Create a GitHub Release**: Go to Releases → Draft a new release
2. **Create a tag**: Use semantic versioning (e.g., `v1.1.0`)
3. **Add release notes**: Copy from `CHANGELOG.md`
4. **Publish release**: GitHub Actions will automatically build and publish to PyPI

**Prerequisites for automation:**
- Add `PYPI_API_TOKEN` to GitHub repository secrets
- Ensure workflows are enabled in repository settings

## Troubleshooting

### Build Fails

```bash
# Ensure build tools are updated
pip install --upgrade pip setuptools wheel build

# Check pyproject.toml syntax
python -c "import tomli; tomli.load(open('pyproject.toml', 'rb'))"
```

### Tests Fail

```bash
# Run with verbose output
pytest tests/ -vv --tb=long

# Run specific test
pytest tests/test_encoder.py::test_encode_dak_bhawan -vv
```

### Import Errors After Install

```bash
# Check installed package structure
pip show -f digipinpy

# Reinstall in development mode
pip install -e . --force-reinstall --no-deps
```

### PyPI Upload Fails

```bash
# Check package name availability
pip search digipinpy

# Verify credentials
twine upload --repository testpypi dist/* --verbose
```

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.1.0)
  - **MAJOR**: Breaking changes
  - **MINOR**: New features (backward compatible)
  - **PATCH**: Bug fixes (backward compatible)

## Support

For build or release issues:
- Email: samarthsmg14@gmail.com, hmrshivu@gmail.com
- Issues: https://github.com/DEADSERPENT/digipin/issues

---

**Happy Building!** 🚀
