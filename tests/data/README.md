# Shared Test Vectors

This directory contains **shared test vectors** that ensure consistency between Python and JavaScript implementations of DIGIPIN.

## Purpose

The `test_vectors.json` file serves as the **single source of truth** for test cases. Both implementations must produce identical results for all test cases to guarantee:

✅ **Specification Compliance** - Both implementations follow the same standard
✅ **Cross-Language Consistency** - Encode in Python, decode in JavaScript (or vice versa)
✅ **Regression Prevention** - Changes don't break compatibility
✅ **Quality Assurance** - Comprehensive edge case coverage

---

## Test Vector Structure

```json
{
  "test_cases": {
    "encoding": [...]      // Lat/lon → DIGIPIN code tests
    "decoding": [...]      // DIGIPIN code → lat/lon tests
    "validation": [...]    // Valid/invalid code tests
    "edge_cases": [...]    // Boundary conditions
    "bounding_boxes": [...] // Cell boundary tests
    "neighbors": [...]     // Neighbor discovery tests
    "hierarchical": [...]  // Parent/child relationships
    "round_trip": [...]    // Encode→Decode consistency
  },
  "character_set": {...},   // Valid DIGIPIN characters
  "precision_table": [...]  // Precision level definitions
}
```

---

## Usage

### Python

```python
import json
from digipin import encode, decode, is_valid

# Load test vectors
with open('tests/data/test_vectors.json', 'r') as f:
    vectors = json.load(f)

# Run encoding tests
for test in vectors['test_cases']['encoding']:
    result = encode(test['lat'], test['lon'], test['precision'])
    assert result == test['expected'], f"Failed: {test['name']}"
    print(f"✓ {test['name']}: {result}")

# Run validation tests
for test in vectors['test_cases']['validation']:
    result = is_valid(test['code'])
    assert result == test['expected'], f"Failed: {test['name']}"
    print(f"✓ {test['name']}: {result}")
```

### JavaScript

```javascript
const { encode, decode, isValid } = require('./digipin');
const vectors = require('../tests/data/test_vectors.json');

// Run encoding tests
vectors.test_cases.encoding.forEach(test => {
  const result = encode(test.lat, test.lon, test.precision);
  console.assert(result === test.expected, `Failed: ${test.name}`);
  console.log(`✓ ${test.name}: ${result}`);
});

// Run validation tests
vectors.test_cases.validation.forEach(test => {
  const result = isValid(test.code);
  console.assert(result === test.expected, `Failed: ${test.name}`);
  console.log(`✓ ${test.name}: ${result}`);
});
```

---

## Test Categories

### 1. **Encoding Tests**
Verify coordinate → DIGIPIN code conversion:
- Famous Indian landmarks (Taj Mahal, India Gate, etc.)
- Different precision levels (1-10)
- Edge cases (borders, corners)

### 2. **Decoding Tests**
Verify DIGIPIN code → coordinate conversion:
- Full precision (10 characters)
- Partial codes (5, 1 characters)
- Tolerance checks for precision loss

### 3. **Validation Tests**
Check valid/invalid DIGIPIN codes:
- Valid codes at different lengths
- Invalid characters (0, 1, A, lowercase)
- Edge cases (empty, too long)

### 4. **Edge Cases**
Boundary condition testing:
- Geographic boundaries of India
- Extreme coordinates
- Southernmost, northernmost points

### 5. **Bounding Boxes**
Verify cell boundary calculations:
- Minimum/maximum lat/lon for cells
- Different precision levels
- Tolerance specifications

### 6. **Neighbors**
Test neighbor discovery:
- 8-directional neighbors
- Specific direction tests
- Edge neighbor handling

### 7. **Hierarchical**
Parent/child code relationships:
- Extracting parent codes
- Different hierarchy levels
- Code truncation

### 8. **Round Trip**
Encode → Decode consistency:
- Major Indian cities
- Precision tolerance checks
- Data integrity verification

---

## Adding New Test Cases

When adding new test vectors:

1. **Add to appropriate category** in `test_vectors.json`
2. **Include all required fields:**
   ```json
   {
     "name": "Descriptive test name",
     "description": "What this tests",
     // ... test-specific fields
     "expected": "expected_result"
   }
   ```
3. **Test in BOTH languages** before committing
4. **Update this README** if adding new categories

---

## Validation Script

Run the validation script to verify both implementations against test vectors:

```bash
# Python
cd python
python tests/validate_test_vectors.py

# JavaScript
cd javascript
node tests/validate_test_vectors.js

# Or use Make
make test-vectors
```

---

## Coverage

Current test vector coverage:

| Category | Test Cases | Status |
|----------|------------|--------|
| Encoding | 8 | ✅ |
| Decoding | 3 | ✅ |
| Validation | 9 | ✅ |
| Edge Cases | 5 | ✅ |
| Bounding Boxes | 2 | ✅ |
| Neighbors | 2 | ✅ |
| Hierarchical | 3 | ✅ |
| Round Trip | 3 | ✅ |

**Total:** 35 test vectors

---

## Known Landmarks

Test vectors include these famous Indian locations:

- 🏛️ **Dak Bhawan, New Delhi** - Department of Posts HQ
- 🕌 **India Gate, New Delhi** - War memorial
- 🌊 **Gateway of India, Mumbai** - Iconic monument
- 🕌 **Taj Mahal, Agra** - World Heritage Site
- 🏰 **Mysore Palace** - Historical palace

These serve as real-world validation points and demonstrate practical usage.

---

## Contributing

When contributing test vectors:

1. Ensure test is **meaningful** (tests real scenario or edge case)
2. Provide **clear description** of what's being tested
3. Include **expected results** with appropriate tolerance
4. **Verify accuracy** using official specification
5. Test with **both implementations**

---

## Maintenance

- **Review quarterly** for completeness
- **Update version** when adding test categories
- **Validate** after specification changes
- **Keep synchronized** with both implementations

---

## License

Test vectors are part of the DIGIPIN project and covered by the MIT License.

Based on the official DIGIPIN specification by the Department of Posts, Government of India.

---

## Contact

Issues with test vectors? Please report at:
- 🐛 [GitHub Issues](https://github.com/DEADSERPENT/digipin/issues)
- 💬 [Discussions](https://github.com/DEADSERPENT/digipin/discussions)
