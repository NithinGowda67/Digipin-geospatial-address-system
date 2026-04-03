# Changelog - JavaScript (digipinjs-lib)

All notable changes to the JavaScript implementation will be documented in this file.

## [1.2.0] - 2025-12-15

### Current Status

**Production-Ready JavaScript Library** implementing India's DIGIPIN national geocoding standard.

#### Features

- ✅ **Core Functions**: `encode()`, `decode()`, `isValid()`
- ✅ **Batch Operations**: `batchEncode()`, `batchDecode()`
- ✅ **Hierarchical Operations**: `getParent()`, `isWithin()`, `getBounds()`
- ✅ **TypeScript Support**: Full type definitions in `digipin.d.ts`
- ✅ **Zero Dependencies**: Pure JavaScript implementation
- ✅ **Cross-Platform**: Node.js ≥10.0.0, browsers (ES5+)
- ✅ **Small Bundle**: ~5KB minified

#### Performance

- Encoding: ~100K ops/sec (Node.js)
- Decoding: ~120K ops/sec (Node.js)
- Suitable for production use in web and mobile applications

#### Installation

```bash
npm install digipinjs-lib
```

#### Usage

```javascript
const digipin = require('digipinjs-lib');

// Encode coordinates
const code = digipin.encode(28.622788, 77.213033);
console.log(code); // '39J49LL8T4'

// Decode code
const coords = digipin.decode('39J49LL8T4');
console.log(coords); // { latitude: 28.622788, longitude: 77.213033 }

// Validate
console.log(digipin.isValid('39J49LL8T4')); // true
```

### Notes

- **Version**: 1.2.0 (stable)
- **Node.js**: ≥10.0.0
- **Bundle Size**: ~5KB minified
- **License**: MIT

---

## [1.1.0] - 2025-12-10

### Added

- TypeScript type definitions (`digipin.d.ts`)
- Batch operations: `batchEncode()`, `batchDecode()`
- Hierarchical functions: `getParent()`, `isWithin()`
- Enhanced error handling with descriptive messages

### Changed

- Improved performance for batch operations
- Updated documentation with TypeScript examples

---

## [1.0.0] - 2025-12-05

### Added

- Initial release of JavaScript implementation
- Core functions: `encode()`, `decode()`, `isValid()`
- Bounding box calculation: `getBounds()`
- Comprehensive test suite
- README with examples
- MIT License

---

## Roadmap (Future Versions)

### Planned for v1.3.0
- Neighbor discovery functions (matching Python implementation)
- React components library (`react-digipin`)
- Vue components library (`vue-digipin`)

### Planned for v2.0.0
- ESM module support
- Tree-shaking optimization
- Browser bundle with UMD format
- CDN distribution
- WebAssembly backend for performance

### Under Consideration
- Angular module
- MapLibre/Leaflet integration
- Client-side visualization helpers
- Form validation components

---

## Comparison: JavaScript vs Python

| Feature | JavaScript (v1.2.0) | Python (v1.8.0) |
|---------|---------------------|-----------------|
| Core Functions | ✅ | ✅ |
| Batch Operations | ✅ | ✅ |
| Neighbor Discovery | ❌ (planned v1.3) | ✅ |
| Polygon Polyfill | ❌ (future) | ✅ |
| Framework Integration | ❌ (planned) | ✅ (Django, FastAPI, Pandas) |
| Visualization | ❌ (planned) | ✅ (Folium maps) |
| Performance Backend | ❌ | ✅ (Cython 10-15x) |
| TypeScript Support | ✅ | ✅ |
| Bundle Size | ~5KB | N/A |
| Performance | ~100K ops/sec | ~50K (Python), ~500-750K (Cython) |

---

## Contributing

We welcome contributions to the JavaScript library!

**Priority Areas:**
1. Neighbor discovery implementation
2. React/Vue component libraries
3. Browser bundle optimization
4. WebAssembly backend

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## Support

**Maintained by:** SAMARTHA H V • MR SHIVAKUMAR
📧 samarthsmg14@gmail.com • hmrshivu@gmail.com

[npm](https://www.npmjs.com/package/digipinjs-lib) • [GitHub](https://github.com/DEADSERPENT/digipin) • [Issues](https://github.com/DEADSERPENT/digipin/issues)

---

**Government of India | Department of Posts | National Addressing Initiative**
