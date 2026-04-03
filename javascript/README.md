<div align="center">

# DIGIPIN-JS

### JavaScript/TypeScript Library for India's National Geocoding Standard

Transform coordinates into precise, hierarchical digital addresses — no API required.
From country-level to doorstep accuracy in milliseconds.

<br>

[![NPM](https://img.shields.io/npm/v/digipinjs-lib?color=CB3837&logo=npm)](https://www.npmjs.com/package/digipinjs-lib)
[![Size](https://img.shields.io/bundlephobia/minzip/digipinjs-lib?label=gzipped)](https://bundlephobia.com/package/digipinjs-lib)
[![TypeScript](https://img.shields.io/badge/types-included-blue?logo=typescript)](digipin.d.ts)
[![Tests](https://img.shields.io/badge/tests-60%2B%20passing-success)](test.js)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[🐍 Python Version](https://github.com/DEADSERPENT/digipin) • [📖 Full Documentation](https://github.com/DEADSERPENT/digipin/tree/main/docs) • [🐛 Issues](https://github.com/DEADSERPENT/digipin/issues)

</div>

---

## What is DIGIPIN?

**DIGIPIN** (Digital Postal Index Number) is India's national geocoding system developed by the **Department of Posts, Ministry of Communications**. It divides the entire country into a hierarchical grid, assigning a unique code to every ~4m × 4m location.

This JavaScript implementation provides offline geocoding with zero dependencies and full TypeScript support.

---

## ⚡ Installation

```bash
# NPM
npm install digipinjs-lib

# Yarn
yarn add digipinjs-lib

# PNPM
pnpm add digipinjs-lib
```

**Browser CDN:**
```html
<script src="https://cdn.jsdelivr.net/npm/digipinjs-lib"></script>
```

---

## 🚀 Quick Start

```javascript
import { encode, decode, getNeighbors, getDisk, getRing } from 'digipinjs-lib';

// Encode coordinates to DIGIPIN
const pin = encode(28.622788, 77.213033);  // '39J49LL8T4'

// Decode back to coordinates
const { lat, lon } = decode('39J49LL8T4');

// Variable precision (1-10 levels)
const cityCode = encode(28.6, 77.2, 5);    // '39J49' (~4km)
const doorCode = encode(28.6, 77.2, 10);   // '39J49LL8T4' (~4m)

// Find 8 immediate neighbors
const neighbors = getNeighbors(pin);

// Get all cells within radius (filled disk)
const area = getDisk(pin, 5);              // 11×11 grid (~300m)

// Get cells at exact distance (hollow ring)
const ring = getRing(pin, 2);              // Cells exactly 2 steps away

// Validate codes
import { isValid } from 'digipinjs-lib';
isValid('39J49LL8T4');  // true
```

---

## ✨ Features

<table>
<tr>
<td align="center" width="33%">

**🎯 Core Operations**
- Encode/Decode
- Validation
- Variable precision (10 levels)
- Bounding boxes
- Parent/child codes

</td>
<td align="center" width="33%">

**🗺️ Geospatial**
- Neighbor discovery
- Radius search (disk)
- Batch operations
- Distance helpers
- 8-directional navigation

</td>
<td align="center" width="33%">

**👨‍💻 Developer Ready**
- TypeScript definitions
- Zero dependencies
- < 5KB gzipped
- Node.js & Browser
- React Native compatible

</td>
</tr>
</table>

---

## 📖 Complete API Reference

### Core Operations

```javascript
// Encoding & Decoding
encode(lat, lon, precision?)           // → '39J49LL8T4'
decode(code)                           // → { lat: 28.6, lon: 77.2 }

// Validation
isValid(code, strict?)                 // → true/false
isValidCoordinate(lat, lon)            // → true/false

// Spatial Queries
getBounds(code)                        // → { minLat, maxLat, minLon, maxLon }
getParent(code, level)                 // → '39J49' (parent at level 5)
```

### Geospatial Functions

```javascript
// Neighbor Discovery
getNeighbors(code, direction?)         // → [...] (8 neighbors or filtered)
// Directions: 'all', 'cardinal', 'north', 'south', 'east', 'west',
//             'northeast', 'northwest', 'southeast', 'southwest'

// Search Areas
getDisk(code, radius?)                 // → [...] (all cells within radius)
getRing(code, radius)                  // → [...] (cells at exact radius)

// Batch Operations
batchEncode(coords, precision?)        // → [...] (encode multiple)
batchDecode(codes)                     // → [...] (decode multiple)
```

---

## 🎯 Real-World Examples

### Store Locator

```javascript
// Find nearby stores
const customerPin = encode(userLat, userLon, 8);
const searchArea = getDisk(customerPin, 5);  // ~300m radius

const nearbyStores = stores.filter(store =>
  searchArea.includes(store.digipin)
);
```

### Delivery Zone Mapping

```javascript
// Define service coverage
const warehousePin = '39J49LL8T4';
const deliveryZone = getDisk(warehousePin, 10);  // ~600m radius

// Check if address is serviceable
const customerPin = encode(customerLat, customerLon, 10);
const canDeliver = deliveryZone.includes(customerPin);
```

### Route Optimization

```javascript
// Group nearby delivery addresses
const addresses = [
  { lat: 28.6, lon: 77.2, id: 1 },
  { lat: 28.61, lon: 77.21, id: 2 }
];

// Encode all addresses
const encoded = batchEncode(
  addresses.map(a => [a.lat, a.lon]),
  8  // street-level precision
);

// Group by region (first 5 characters)
const regions = {};
encoded.forEach((code, i) => {
  const region = code.substring(0, 5);
  if (!regions[region]) regions[region] = [];
  regions[region].push(addresses[i]);
});
```

---

## 📊 Precision Levels

| Level | Cell Size | Resolution | Use Case |
|-------|-----------|-----------|----------|
| **1** | ~1000 km | Country | National analytics |
| **2** | ~250 km | State | Regional planning |
| **3** | ~63 km | Region | District operations |
| **4** | ~16 km | District | City-wide services |
| **5** | ~4 km | City | Urban zones |
| **6** | ~1 km | Neighborhood | Delivery zones |
| **7** | ~250 m | Area | Local services |
| **8** | ~60 m | Street | Store locator |
| **9** | ~15 m | Building | Building-level |
| **10** | ~4 m | Doorstep | Last-mile delivery |

---

## 🌐 Platform Support

| Platform | Support | Version |
|----------|---------|---------|
| **Node.js** | ✅ Full | v10+ |
| **Browsers** | ✅ Full | ES6+ |
| **TypeScript** | ✅ Full | Included |
| **React** | ✅ Compatible | Any |
| **React Native** | ✅ Compatible | Any |
| **Vue.js** | ✅ Compatible | Any |
| **Angular** | ✅ Compatible | Any |

---

## 🔗 DIGIPIN Ecosystem

| Package | Environment | Version | Status |
|---------|------------|---------|--------|
| [digipinpy](https://pypi.org/project/digipinpy/) | Python 3.7+ | v1.7.0 | ✅ Production |
| **digipinjs-lib** | JavaScript/TS | v1.0.0 | ✅ Production |
| digipin-django | Django ORM | Included | ✅ Available |
| digipin-flask | Flask + SQLAlchemy | Included | ✅ Available |
| digipin-fastapi | FastAPI | Included | ✅ Available |
| digipin-pandas | Pandas | Included | ✅ Available |

---

## ✅ Testing

```bash
npm test  # 60+ tests, 100% pass rate
```

**Test Coverage:**
- ✅ Encoding/Decoding accuracy
- ✅ Edge cases (poles, boundaries)
- ✅ Neighbor discovery (8 directions)
- ✅ Search algorithms (disk, ring)
- ✅ Batch operations
- ✅ Validation logic

---

## 📜 License

**MIT License** — Free for commercial and personal use.

Based on the official DIGIPIN specification published by the **Department of Posts, Ministry of Communications, Government of India**.

See [LICENSE](LICENSE) file for details.

---

## 👥 Maintainers

**SAMARTHA H V** • **MR SHIVAKUMAR**

📧 [samarthsmg14@gmail.com](mailto:samarthsmg14@gmail.com) • [hmrshivu@gmail.com](mailto:hmrshivu@gmail.com)

---

## 🔗 Links

- 📦 **NPM Package:** [npmjs.com/package/digipinjs-lib](https://www.npmjs.com/package/digipinjs-lib)
- 🐍 **Python Version:** [pypi.org/project/digipinpy](https://pypi.org/project/digipinpy/)
- 📚 **Full Documentation:** [GitHub Docs](https://github.com/DEADSERPENT/digipin/tree/main/docs)
- 🐛 **Issue Tracker:** [GitHub Issues](https://github.com/DEADSERPENT/digipin/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/DEADSERPENT/digipin/discussions)
- 📖 **Changelog:** [CHANGELOG.md](https://github.com/DEADSERPENT/digipin/blob/main/CHANGELOG.md)

---

Government of India • Department of Posts • National Addressing Initiative

</div>
