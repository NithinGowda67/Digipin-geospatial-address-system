# Changelog - Python (digipinpy)

All notable changes to the Python implementation will be documented in this file.

## [1.8.0] - 2025-12-15

### Added – Optional Cython Performance Backend

- Optional **Cython-optimized core** for encoding, decoding, and bounds calculation  
- **10–15x performance improvement** over pure Python for critical operations  
- Automatic backend selection with transparent fallback to pure Python  
- No API changes required for users  
- Backend status available via `get_backend_info()`  

### Performance

- Encoding: ~40K → ~400–600K ops/sec  
- Decoding: ~50K → ~500–750K ops/sec  
- Batch operations: 10–15x faster  

### Build & Tooling

- Cython-aware `setup.py` with platform-specific optimizations  
- Cross-platform support (Linux, macOS, Windows)  
- Benchmark suite for Python vs Cython performance  
- Detailed performance and build documentation  

## [1.6.1] - 2025-12-12

### Changed
- Set quadtree as default polyfill algorithm (was grid scan)
- Algorithm automatically selected based on polygon characteristics

---

## [1.6.0] - 2025-12-12

### Added - Optimized Quadtree Polyfill Algorithm

- Quadtree polyfill implementation (up to 10x faster for sparse polygons)
- Algorithm selection parameter: `polyfill(..., algorithm="quadtree")`
- 15 new comprehensive tests for polyfill
- Performance benchmark scripts
- Technical documentation in `docs/polyfill_optimization.md`

See root CHANGELOG.md for complete details.

---

## [1.5.0] - 2025-12-11

### Added - CSV Batch Processing & Interactive Visualization

- CLI batch processing: `digipin convert` for CSV/Excel files
- Interactive map visualization with Folium
- `plot_pins()`, `plot_coverage()`, `plot_neighbors()` functions
- 46 new comprehensive tests (18 CLI + 28 visualization)

See root CHANGELOG.md for complete details.

---

## [1.4.2] - 2025-12-11

### Added
- New README file with landing page and documentation links

---

## [1.4.1] - 2025-12-10

### Fixed
- PyPI license badge (added MIT classifier)
- Codecov integration

### Added
- Codecov coverage reporting

---

## [1.4.0] - 2025-12-09

### Added - Geospatial Polyfill

- `polyfill()` function for polygon-to-codes conversion
- `get_polygon_boundary()` for bounding box calculation
- Shapely integration for geospatial operations

See root CHANGELOG.md for complete details.

---

## [1.3.0] - 2025-12-09

### Added - FastAPI Integration

- Pre-built FastAPI router with Pydantic models
- REST API endpoints: `/encode`, `/decode/{code}`, `/neighbors/{code}`
- Auto-generated Swagger UI documentation
- 41 comprehensive tests

See root CHANGELOG.md for complete details.

---

## [1.2.0] - 2025-12-09

### Added - Django & Pandas Integrations

- `DigipinField` for Django models
- DataFrame accessor: `df.digipin.encode()`, `df.digipin.decode()`
- 64 new comprehensive tests (31 Django + 33 Pandas)

See root CHANGELOG.md for complete details.

---

## [1.1.0] - 2025-01-28

### Added - Neighbor Discovery

- `get_neighbors()`, `get_ring()`, `get_disk()` functions
- Proximity search capabilities
- 28 comprehensive tests

See root CHANGELOG.md for complete details.

---

## [1.0.1] - 2025-11-26

### Fixed
- Documentation typos
- Example code corrections
- CLI JSON output formatting

---

## [1.0.0] - 2025-11-25

### Added
- Initial release
- Core encoding/decoding
- Batch operations
- CLI interface
- 31 comprehensive tests
