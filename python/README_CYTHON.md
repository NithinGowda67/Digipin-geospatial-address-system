# Cython Performance Backend

## Quick Start

### Build the Cython extension

```bash
cd python

# Install Cython
pip install cython

# Compile the C extension
python setup.py build_ext --inplace

# Install the package
pip install -e .
```

### Verify it's working

```python
import digipin

# Check which backend is active
backend = digipin.get_backend_info()
print(backend)
# Expected output:
# {
#   'backend': 'cython',
#   'performance': '10-15x',
#   'description': 'Cython-optimized (C-compiled) implementation'
# }
```

## Performance Comparison

Run the benchmark:

```bash
python benchmarks/cython_performance.py
```

**Expected Results:**

| Operation | Pure Python | Cython | Speedup |
|-----------|-------------|--------|---------|
| Encoding  | ~40K ops/sec | ~400-600K ops/sec | 10-15x |
| Decoding  | ~50K ops/sec | ~500-750K ops/sec | 10-15x |

## What Gets Optimized?

The Cython backend optimizes the **core spiral encoding/decoding algorithms**:

✅ **Optimized Functions:**
- `encode()` - 10-15x faster
- `decode()` - 10-15x faster
- `get_bounds()` - 10-15x faster
- `batch_encode()` - 10-15x faster
- `batch_decode()` - 10-15x faster

⚠️ **Not Optimized** (still pure Python):
- `get_neighbors()` - Already fast enough
- `polyfill()` - Depends on shapely
- String operations (`get_parent`, `is_within`) - Already fast

## How It Works

### 1. Static C Typing

**Python (dynamic):**
```python
def encode(lat, lon, precision=10):
    min_lat = 2.5
    max_lat = 38.5
    # ... Python objects with runtime type checking
```

**Cython (static):**
```cython
cpdef str encode_fast(double lat, double lon, int precision=10):
    cdef double min_lat = 2.5
    cdef double max_lat = 38.5
    # ... C variables with no runtime overhead
```

### 2. Direct Memory Access

- **Python**: Array access involves Python objects and bounds checking
- **Cython**: Direct C array access with compile-time optimization

### 3. Eliminated Python Overhead

- **Python**: Function calls, object allocation, reference counting
- **Cython**: Compiled to native C code executed by CPU

## Troubleshooting

### Extension not loading?

```bash
# Check if .so (Linux/Mac) or .pyd (Windows) was created
ls src/digipin/core_fast*.so   # Linux/macOS
dir src\digipin\core_fast*.pyd # Windows

# If missing, rebuild:
python setup.py clean --all
python setup.py build_ext --inplace
```

### Compiler errors?

**Windows:** Install [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

**Linux:** Install Python dev headers
```bash
sudo apt-get install python3-dev
```

**macOS:** Install Xcode Command Line Tools
```bash
xcode-select --install
```

## Files

- `src/digipin/core_fast.pyx` - Cython source code
- `setup.py` - Build configuration
- `benchmarks/cython_performance.py` - Performance tests

## Documentation

See the full guide: [docs/performance-optimization.md](../../docs/performance-optimization.md)

## Future Work

- [ ] Rust backend (20-30x speedup) - Planned for v2.0
- [ ] GPU acceleration for batch operations
- [ ] SIMD optimizations

---

**Questions?** Open an issue: https://github.com/DEADSERPENT/digipin/issues
