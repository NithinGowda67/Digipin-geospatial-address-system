<div align="center">

# 🇮🇳 DIGIPIN

**Official open-source implementations of India's national geocoding standard**

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python)](python/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?logo=javascript)](javascript/)
[![DOI](https://zenodo.org/badge/1101294193.svg)](https://doi.org/10.5281/zenodo.17916240)

Transform coordinates into precise, hierarchical digital addresses — no API required.
From country-level to doorstep accuracy in milliseconds.

[Documentation](docs/index.md) • [Contributing](CONTRIBUTING.md) • [Changelog](CHANGELOG.md)

</div>

---

## What is DIGIPIN?

**DIGIPIN** (Digital Postal Index Number) is India's national geocoding system developed by the **Department of Posts, Ministry of Communications, Government of India**. It divides the entire country into a hierarchical grid, assigning a unique code to every ~4m × 4m location.

This repository contains official reference implementations in **Python** and **JavaScript**, both achieving 100% specification compliance with zero dependencies.

---

## 🚀 Implementations

### 🐍 Python

**Package:** `digipinpy`
**Location:** [`/python`](python/)
**PyPI:** [pypi.org/project/digipinpy](https://pypi.org/project/digipinpy/)

```bash
pip install digipinpy
```

**Features:**
- ⚡ ~50,000 encodes/second
- 📦 Zero dependencies (pure Python)
- 🔌 Native Pandas, Django, FastAPI, Flask integrations
- 📊 CLI for batch CSV/Excel processing
- 🗺️ Interactive map visualization

[→ Python Documentation](python/README.md)

---

### 🟨 JavaScript / TypeScript

**Package:** `digipinjs-lib`
**Location:** [`/javascript`](javascript/)
**NPM:** [npmjs.com/package/digipinjs-lib](https://www.npmjs.com/package/digipinjs-lib)

```bash
npm install digipinjs-lib
```

**Features:**
- 🎯 Zero dependencies
- 📘 Full TypeScript definitions
- 🌐 Node.js & Browser compatible
- ⚡ < 5KB gzipped
- ⚛️ React, Vue, Angular ready

[→ JavaScript Documentation](javascript/README.md)

---

## 📖 Documentation

### 📚 General Resources
- [Technical Specification](docs/technical_spec.md) - Official DIGIPIN spec
- [Getting Started](docs/getting-started.md) - Quick start guide
- [Use Cases](docs/use-cases.md) - Real-world applications
- [Geospatial Polyfill](docs/geospatial-polyfill.md) - Polygon conversion

### 🔌 Integration Guides
- [Pandas Integration](docs/integrations-pandas.md) - DataFrame operations
- [Django Integration](docs/integrations-django.md) - ORM field with validation
- [FastAPI Integration](docs/integrations-fastapi.md) - REST API microservices
- [Flask Integration](docs/integrations-flask.md) - Flask + SQLAlchemy

---

## 🎯 Quick Example

### Python
```python
from digipin import encode, decode

# Encode coordinates to DIGIPIN
code = encode(28.622788, 77.213033)  # '39J49LL8T4'

# Decode back to coordinates
lat, lon = decode('39J49LL8T4')
```

### JavaScript
```javascript
import { encode, decode } from 'digipinjs-lib';

// Encode coordinates to DIGIPIN
const code = encode(28.622788, 77.213033);  // '39J49LL8T4'

// Decode back to coordinates
const { lat, lon } = decode('39J49LL8T4');
```

---

## 🗺️ Precision Levels

| Level | Cell Size | Use Case |
|-------|-----------|----------|
| **1-2** | ~1000-250 km | Country/State analytics |
| **3-5** | ~63-4 km | Regional/Urban zones |
| **6-8** | ~1km-60m | Delivery zones/Store locator |
| **9-10** | ~15-4m | Building/Last-mile delivery |

---

## 🌟 Key Features

<table>
<tr>
<td width="50%">

**🎯 Core Capabilities**
- Encode/Decode coordinates
- Variable precision (10 levels)
- Neighbor discovery
- Radius search (disk/ring)
- Hierarchical operations
- Bounding box calculations

</td>
<td width="50%">

**⚡ Performance**
- Zero API dependencies
- Offline operation
- Sub-millisecond encoding
- Optimized algorithms
- Small bundle sizes
- Cross-platform

</td>
</tr>
</table>

---

## 📦 Repository Structure

```
digipin/
├── python/              # Python implementation (digipinpy)
│   ├── src/            # Source code
│   ├── tests/          # Test suite (178+ tests)
│   ├── examples/       # Usage examples
│   ├── benchmarks/     # Performance tests
│   └── README.md       # Python docs
│
├── javascript/         # JavaScript implementation (digipinjs-lib)
│   ├── digipin.js      # Main library
│   ├── test.js         # Test suite (60+ tests)
│   ├── example.js      # Usage examples
│   └── README.md       # JavaScript docs
│
├── tests/data/         # 🆕 Shared test vectors (35+ test cases)
│   ├── test_vectors.json  # Single source of truth
│   └── README.md       # Test vector documentation
│
├── docs/               # Shared documentation
├── images/             # Assets and diagrams
├── .github/workflows/  # CI/CD workflows (Python + JavaScript)
├── Makefile            # 🆕 Unified development commands
└── README.md           # This file
```

---

## 🤝 Contributing

We welcome contributions to both Python and JavaScript implementations!

**Quick setup using Makefile:**

```bash
# Clone the repository
git clone https://github.com/DEADSERPENT/digipin.git
cd digipin

# Install all dependencies
make install

# Run all tests
make test

# Run linters
make lint

# See all available commands
make help
```

**Or manually:**

```bash
# For Python development
cd python
pip install -e ".[dev]"
pytest tests/ -v

# For JavaScript development
cd javascript
npm install
npm test
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📊 Project Status

- ✅ **Production Ready** - Both implementations stable
- ✅ **100% Spec Compliant** - Official DoP specification
- ✅ **Comprehensive Tests** - 178+ tests for Python, 60+ for JavaScript
- ✅ **Type Safe** - Full type hints (Python) and TypeScript definitions (JS)
- ✅ **Multi-Platform** - Windows, macOS, Linux, Browser

---

## 📜 License

**MIT License** — Free for commercial and personal use.

Based on the official DIGIPIN specification published by the **Department of Posts, Ministry of Communications, Government of India** (March 2025).

See [LICENSE](LICENSE) file for details.

---

## 👥 Maintainers

**SAMARTHA H V** • **MR SHIVAKUMAR**

📧 [samarthsmg14@gmail.com](mailto:samarthsmg14@gmail.com) • [hmrshivu@gmail.com](mailto:hmrshivu@gmail.com)

---

## 🔗 Links

- 🐍 **Python (PyPI):** [pypi.org/project/digipinpy](https://pypi.org/project/digipinpy/)
- 🟨 **JavaScript (NPM):** [npmjs.com/package/digipinjs-lib](https://www.npmjs.com/package/digipinjs-lib)
- 📚 **Documentation:** [docs/](docs/)
- 🐛 **Issue Tracker:** [GitHub Issues](https://github.com/DEADSERPENT/digipin/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/DEADSERPENT/digipin/discussions)

---

<div align="center">

**Government of India • Department of Posts • National Addressing Initiative**

</div>
