# Getting Started with DIGIPIN-Py

This guide will help you get up and running with DIGIPIN-Py in minutes.

## Installation

### Basic Installation

Install the core package with zero dependencies:

```bash
pip install digipinpy
```

**Requirements:** Python 3.8+ (Python 3.7 supported but not tested in CI)

### Optional Dependencies

Install additional integrations based on your needs:

```bash
# For data science workflows with Pandas
pip install digipinpy[pandas]

# For Django web applications
pip install digipinpy[django]

# For FastAPI microservices
pip install digipinpy[fastapi]

# For geospatial operations (polyfill)
pip install digipinpy[geo]

# Install everything
pip install digipinpy[pandas,django,fastapi,geo]

# For development (testing, linting, type checking)
pip install digipinpy[dev]
```

## Your First DIGIPIN Code

### Encoding Coordinates

Convert latitude/longitude coordinates to a DIGIPIN code:

```python
from digipin import encode

# Encode coordinates (Dak Bhawan, New Delhi)
code = encode(28.622788, 77.213033)
print(code)  # Output: '39J49LL8T4'
```

### Decoding DIGIPIN Codes

Convert a DIGIPIN code back to coordinates:

```python
from digipin import decode

# Decode DIGIPIN code
lat, lon = decode('39J49LL8T4')
print(f"Latitude: {lat:.6f}")   # 28.622788
print(f"Longitude: {lon:.6f}")  # 77.213033
```

### Round-Trip Verification

```python
from digipin import encode, decode

# Original coordinates
original_lat, original_lon = 28.622788, 77.213033

# Encode
code = encode(original_lat, original_lon)

# Decode
decoded_lat, decoded_lon = decode(code)

# Verify (coordinates match at precision level)
print(f"Match: {abs(original_lat - decoded_lat) < 0.0001}")  # True
```

## Working with Precision Levels

DIGIPIN codes can have different precision levels (1-10):

| Level | Approx. Size | Use Case |
|-------|--------------|----------|
| 1-2   | ~1000km      | Country/state level |
| 3-4   | ~60-250km    | District/city level |
| 5-6   | ~4-15km      | Neighborhood level |
| 7-8   | ~250m-1km    | Street/building level |
| 9-10  | ~15m-60m     | Precise location |

### Variable Precision Encoding

```python
from digipin import encode

lat, lon = 28.622788, 77.213033

# Different precision levels
level_3 = encode(lat, lon, precision=3)   # '39J' (~16km)
level_5 = encode(lat, lon, precision=5)   # '39J49' (~1km)
level_7 = encode(lat, lon, precision=7)   # '39J49LL' (~250m)
level_10 = encode(lat, lon, precision=10) # '39J49LL8T4' (~3.8m)

print(f"Region:   {level_3}")
print(f"District: {level_5}")
print(f"Street:   {level_7}")
print(f"Precise:  {level_10}")
```

## Batch Operations

Process multiple locations efficiently:

```python
from digipin import batch_encode, batch_decode

# Encode multiple locations
locations = [
    (28.622788, 77.213033),  # New Delhi
    (19.076090, 72.877426),  # Mumbai
    (13.082680, 80.270721),  # Chennai
]

codes = batch_encode(locations)
print(codes)  # ['39J49LL8T4', '2MK8MP3K63', '2C4LKPTM5T']

# Decode multiple codes
coordinates = batch_decode(codes)
for (lat, lon), city in zip(coordinates, ['Delhi', 'Mumbai', 'Chennai']):
    print(f"{city}: {lat:.4f}, {lon:.4f}")
```

## Proximity Search

### Finding Neighbors

Get the 8 cells immediately surrounding a location:

```python
from digipin import get_neighbors

code = '39J49LL8T4'
neighbors = get_neighbors(code)

print(f"Found {len(neighbors)} neighbors")
# Output: ['39J49LL8T9', '39J49LL8TC', '39J49LL8TL', ...]
```

### Ring Search

Get cells at a specific distance:

```python
from digipin import get_ring

# Get cells at distance 2 from center
ring = get_ring('39J49LL8T4', distance=2)
print(f"Ring size: {len(ring)} cells")
```

### Disk Search

Get all cells within a radius (useful for area searches):

```python
from digipin import get_disk

# Get all cells within radius 3
search_area = get_disk('39J49LL8T4', radius=3)
print(f"Search area: {len(search_area)} cells")

# Radius 0 = just the center
# Radius 1 = center + 8 neighbors (9 total)
# Radius 2 = 5×5 grid (25 total)
# Radius 3 = 7×7 grid (49 total)
```

## Validation

Check if a string is a valid DIGIPIN code:

```python
from digipin import is_valid

# Valid codes
print(is_valid('39J49LL8T4'))   # True
print(is_valid('39J49'))        # True (partial code)

# Invalid codes
print(is_valid('INVALID'))      # False
print(is_valid('39J49LL8T0'))   # False (contains '0')
print(is_valid(''))             # False
```

## Hierarchical Operations

### Get Parent Code

```python
from digipin import get_parent

code = '39J49LL8T4'

# Get parent at level 5 (district)
district = get_parent(code, level=5)
print(district)  # '39J49'

# Get immediate parent (level 9)
parent = get_parent(code, level=9)
print(parent)  # '39J49LL8T'
```

### Check Containment

```python
from digipin import is_within

building = '39J49LL8T4'
district = '39J49'

# Check if building is within district
print(is_within(building, district))  # True

# Reverse check
print(is_within(district, building))  # False
```

## Getting Cell Bounds

Get the geographic boundaries of a DIGIPIN cell:

```python
from digipin import get_bounds

code = '39J49LL8T4'
min_lat, max_lat, min_lon, max_lon = get_bounds(code)

print(f"Latitude:  {min_lat:.6f} to {max_lat:.6f}")
print(f"Longitude: {min_lon:.6f} to {max_lon:.6f}")

# Calculate cell dimensions
lat_span = max_lat - min_lat
lon_span = max_lon - min_lon
print(f"Cell size: ~{lat_span*111:.1f}m × {lon_span*111:.1f}m")
```

## Next Steps

Now that you understand the basics, explore:

- **[Use Cases](use-cases.md)** - Real-world application examples
- **[API Reference](../DOCUMENTATION.md)** - Complete function documentation
- **[Integrations](integrations-pandas.md)** - Pandas, Django, FastAPI guides
- **[Geospatial Polyfill](geospatial-polyfill.md)** - Polygon-to-codes conversion

## Common Patterns

### Location Search

```python
from digipin import encode, get_disk

# User's location
user_lat, user_lon = 28.622788, 77.213033
user_code = encode(user_lat, user_lon, precision=7)

# Search area (within ~1km)
search_codes = get_disk(user_code, radius=2)

# Query database for locations in these codes
# SELECT * FROM locations WHERE digipin_code IN (search_codes)
```

### Geofencing

```python
from digipin import encode, is_within

# Define service area
service_area = '39J49'  # District code

# Check if customer is in service area
customer_location = encode(28.622788, 77.213033, precision=5)
in_service_area = is_within(customer_location, service_area)

if in_service_area:
    print("Delivery available!")
```

### Distance Approximation

```python
from digipin import get_parent

code1 = '39J49LL8T4'
code2 = '39J49LL8T9'

# Find common ancestor level
for level in range(10, 0, -1):
    parent1 = get_parent(code1, level=level)
    parent2 = get_parent(code2, level=level)

    if parent1 == parent2:
        print(f"Same region at level {level}")
        break
```

## Troubleshooting

### "ValueError: Coordinates outside India bounds"

DIGIPIN only covers India's territory:
- Latitude: 2.5°N to 38.5°N
- Longitude: 63.5°E to 99.5°E

Check your coordinate order (latitude first, then longitude).

### "ValueError: Invalid DIGIPIN code"

Valid codes only contain these characters: `23456789CFJKLMPT`

Common issues:
- Contains '0', '1', 'A', 'B', 'D', 'E', etc.
- Empty string
- Too short (< 1) or too long (> 10)

### Performance Tips

1. **Use batch operations** for multiple locations
2. **Cache frequently used codes** in your application
3. **Use appropriate precision** - don't use level 10 when level 7 is sufficient
4. **Pre-compute search areas** for static locations

## Support

- **Issues:** https://github.com/DEADSERPENT/digipin/issues
- **Discussions:** https://github.com/DEADSERPENT/digipin/discussions
- **Email:** samarthsmg14@gmail.com, hmrshivu@gmail.com
