# Geospatial Polyfill

Convert geographic polygons (delivery zones, city boundaries, restricted areas) into sets of DIGIPIN codes for efficient geofencing and spatial queries.

## Installation

```bash
pip install digipinpy[geo]
```

**Requirements:** shapely>=2.0.0

## What is Polyfill?

**Polyfill** converts a polygon (defined by its boundary coordinates) into a set of DIGIPIN codes that cover the entire area. This is essential for:

- ✅ **Geofencing** - Fast O(1) lookup to check if a location is inside an area
- ✅ **Service Area Definition** - Define delivery zones, coverage areas
- ✅ **Spatial Filtering** - Filter database records by geographic region
- ✅ **Risk Assessment** - Identify locations in flood zones, restricted areas
- ✅ **Logistics Optimization** - Route planning within defined zones

## Quick Start

```python
from digipin import polyfill, encode

# Define delivery zone as polygon (lat, lon coordinates)
delivery_zone = [
    (28.6328, 77.2197),  # Top vertex
    (28.6289, 77.2155),  # Bottom-left
    (28.6289, 77.2239),  # Bottom-right
]

# Convert polygon to DIGIPIN codes (precision 8 = ~60m cells)
zone_codes = polyfill(delivery_zone, precision=8)

print(f"Zone covered by {len(zone_codes)} codes")
# Output: Zone covered by 53 codes

# Fast O(1) address validation
customer_code = encode(28.6310, 77.2200, precision=8)
if customer_code in zone_codes:
    print("✓ Address IS in delivery zone!")
else:
    print("✗ Address NOT in delivery zone")
```

## Function Reference

### `polyfill(polygon, precision=7)`

Convert a polygon to DIGIPIN codes.

**Parameters:**
- `polygon`: Shapely Polygon object OR list of (lat, lon) tuples
- `precision`: DIGIPIN level (1-10). Default: 7

**Returns:** List of DIGIPIN codes as strings

**Example with coordinate list:**
```python
from digipin import polyfill

# List of (latitude, longitude) coordinates
polygon_coords = [
    (28.6328, 77.2197),
    (28.6289, 77.2155),
    (28.6289, 77.2239),
    (28.6328, 77.2197),  # Close the polygon
]

codes = polyfill(polygon_coords, precision=7)
```

**Example with Shapely Polygon:**
```python
from shapely.geometry import Polygon
from digipin import polyfill

# Create Shapely polygon (note: Shapely uses lon, lat order)
polygon = Polygon([
    (77.2197, 28.6328),  # (lon, lat)
    (77.2155, 28.6289),
    (77.2239, 28.6289),
])

codes = polyfill(polygon, precision=7)
```

### `get_polygon_boundary(codes)`

Calculate the bounding box of a list of DIGIPIN codes.

**Parameters:**
- `codes`: List of DIGIPIN code strings

**Returns:** Tuple of (min_lat, max_lat, min_lon, max_lon)

**Example:**
```python
from digipin import get_polygon_boundary

codes = ['39J49LL8T4', '39J49LL8T9', '39J49LL8TC']
min_lat, max_lat, min_lon, max_lon = get_polygon_boundary(codes)

print(f"Bounding box:")
print(f"  Latitude:  {min_lat:.6f} to {max_lat:.6f}")
print(f"  Longitude: {min_lon:.6f} to {max_lon:.6f}")
```

## Precision Selection

Choose precision based on your use case:

| Precision | Cell Size | Use Case |
|-----------|-----------|----------|
| **5** | ~1-4 km | City-wide zones, districts |
| **6** | ~250m-1km | Neighborhood delivery zones |
| **7** | ~60-250m | Street-level service areas |
| **8** | ~15-60m | Building-level geofencing |
| **9-10** | ~4-15m | Precise restricted areas |

**⚠️ Warning:** High precision (9-10) on large polygons generates massive lists!

```python
from digipin import polyfill

large_polygon = [...]  # City boundary

# ✗ BAD - May generate millions of codes
codes = polyfill(large_polygon, precision=10)

# ✓ GOOD - Use appropriate precision
codes = polyfill(large_polygon, precision=6)  # ~250m cells
```

## Real-World Examples

### 1. Delivery Zone Definition

```python
from digipin import polyfill, encode

# Define delivery zone (restaurant coverage area)
restaurant_zone = [
    (28.6328, 77.2197),
    (28.6289, 77.2155),
    (28.6289, 77.2239),
]

# Convert to codes (precision 7 = ~250m, good for delivery)
delivery_codes = polyfill(restaurant_zone, precision=7)

print(f"Delivery zone: {len(delivery_codes)} cells")

# Check customer address
def can_deliver(customer_lat, customer_lon):
    customer_code = encode(customer_lat, customer_lon, precision=7)
    return customer_code in delivery_codes

# Usage
if can_deliver(28.6310, 77.2200):
    print("Delivery available!")
    print("Estimated time: 30 minutes")
```

### 2. Flood Risk Assessment

```python
from digipin import polyfill, encode

# Historical flood zone boundary
flood_zone = [
    (28.5500, 77.1000),
    (28.5500, 77.1500),
    (28.5700, 77.1500),
    (28.5700, 77.1000),
]

# Convert to codes (precision 8 = ~60m)
flood_risk_codes = polyfill(flood_zone, precision=8)

# Check if property is in flood zone
def check_flood_risk(property_lat, property_lon):
    property_code = encode(property_lat, property_lon, precision=8)
    if property_code in flood_risk_codes:
        return "HIGH RISK - Flood zone"
    else:
        return "Low risk"

# Usage
risk = check_flood_risk(28.5600, 77.1200)
print(risk)
```

### 3. Restricted Airspace

```python
from digipin import polyfill, encode

# Airport restricted zone
no_fly_zone = [
    (28.5562, 77.0850),
    (28.5562, 77.1200),
    (28.5700, 77.1200),
    (28.5700, 77.0850),
]

# High precision for safety (precision 9 = ~15m)
restricted_codes = polyfill(no_fly_zone, precision=9)

def is_flight_allowed(drone_lat, drone_lon):
    """Check if drone can fly at location"""
    drone_code = encode(drone_lat, drone_lon, precision=9)
    return drone_code not in restricted_codes

# Usage
if is_flight_allowed(28.5600, 77.1000):
    print("✓ Flight authorized")
else:
    print("✗ RESTRICTED AIRSPACE")
```

### 4. Service Coverage Map

```python
from digipin import polyfill, encode
from shapely.geometry import Point, Polygon
import json

# Mobile network tower coverage
tower_location = (28.6228, 77.2130)
coverage_radius_km = 2.0

# Create circular polygon (approximate)
import math

def create_circle_polygon(center_lat, center_lon, radius_km, num_points=32):
    """Create circular polygon around a point"""
    coords = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        # Approximate: 1 degree lat ≈ 111km, 1 degree lon ≈ 111km * cos(lat)
        delta_lat = (radius_km / 111) * math.cos(angle)
        delta_lon = (radius_km / (111 * math.cos(math.radians(center_lat)))) * math.sin(angle)
        coords.append((center_lat + delta_lat, center_lon + delta_lon))
    return coords

# Generate coverage polygon
coverage_polygon = create_circle_polygon(
    tower_location[0],
    tower_location[1],
    coverage_radius_km
)

# Convert to DIGIPIN codes
coverage_codes = polyfill(coverage_polygon, precision=7)

print(f"Tower covers {len(coverage_codes)} cells")

# Save to file for later use
with open('coverage_map.json', 'w') as f:
    json.dump(coverage_codes, f)
```

### 5. Multi-Zone Logistics

```python
from digipin import polyfill, encode

# Define multiple delivery hubs with zones
hubs = {
    "Hub North": {
        "location": (28.6500, 77.2000),
        "zone": [
            (28.6700, 77.1800),
            (28.6300, 77.1800),
            (28.6300, 77.2200),
            (28.6700, 77.2200),
        ]
    },
    "Hub South": {
        "location": (28.6000, 77.2000),
        "zone": [
            (28.6200, 77.1800),
            (28.5800, 77.1800),
            (28.5800, 77.2200),
            (28.6200, 77.2200),
        ]
    }
}

# Convert all zones to codes
for hub_name, hub_data in hubs.items():
    hub_data["codes"] = polyfill(hub_data["zone"], precision=7)
    print(f"{hub_name}: {len(hub_data['codes'])} cells")

# Route order to correct hub
def assign_hub(customer_lat, customer_lon):
    customer_code = encode(customer_lat, customer_lon, precision=7)

    for hub_name, hub_data in hubs.items():
        if customer_code in hub_data["codes"]:
            return hub_name

    return "No hub available"

# Usage
hub = assign_hub(28.6400, 77.1900)
print(f"Assigned to: {hub}")
```

## Working with Shapely

### Complex Polygons

```python
from shapely.geometry import Polygon
from digipin import polyfill

# Polygon with hole (donut shape)
outer_ring = [
    (77.2000, 28.6000),
    (77.2000, 28.6300),
    (77.2300, 28.6300),
    (77.2300, 28.6000),
]

inner_ring = [  # Hole
    (77.2100, 28.6100),
    (77.2100, 28.6200),
    (77.2200, 28.6200),
    (77.2200, 28.6100),
]

polygon = Polygon(outer_ring, [inner_ring])
codes = polyfill(polygon, precision=7)
```

### Multi-Polygon (Disconnected Regions)

```python
from shapely.geometry import MultiPolygon, Polygon
from digipin import polyfill

# Two separate delivery zones
zone1 = Polygon([
    (77.2000, 28.6000),
    (77.2100, 28.6000),
    (77.2100, 28.6100),
    (77.2000, 28.6100),
])

zone2 = Polygon([
    (77.2200, 28.6200),
    (77.2300, 28.6200),
    (77.2300, 28.6300),
    (77.2200, 28.6300),
])

multi_polygon = MultiPolygon([zone1, zone2])

# Polyfill each polygon separately
all_codes = []
for poly in multi_polygon.geoms:
    codes = polyfill(poly, precision=7)
    all_codes.extend(codes)

print(f"Total coverage: {len(all_codes)} cells")
```

## Performance Optimization

### 1. Pre-compute and Cache

```python
from digipin import polyfill
import json

# Compute once
service_area_polygon = [...]
service_codes = polyfill(service_area_polygon, precision=7)

# Save to file
with open('service_area.json', 'w') as f:
    json.dump(service_codes, f)

# Load for fast lookups
with open('service_area.json', 'r') as f:
    service_codes = set(json.load(f))  # Use set for O(1) lookup

# Fast check
customer_code = "39J49LL8T4"
if customer_code in service_codes:  # O(1) operation
    print("In service area")
```

### 2. Use Appropriate Precision

```python
# ✗ BAD - Overkill for city-wide zone
city_codes = polyfill(city_boundary, precision=10)  # Millions of codes!

# ✓ GOOD - Appropriate for use case
city_codes = polyfill(city_boundary, precision=6)  # Thousands of codes
```

### 3. Database Storage

```python
# PostgreSQL with array column
CREATE TABLE service_areas (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    coverage_codes TEXT[]  -- Store as array
);

# Insert
INSERT INTO service_areas (name, coverage_codes)
VALUES ('North Zone', ARRAY['39J49LL8T4', '39J49LL8T9', ...]);

# Query
SELECT * FROM service_areas
WHERE '39J49LL8T4' = ANY(coverage_codes);
```

### 4. In-Memory Cache

```python
from functools import lru_cache
from digipin import polyfill

@lru_cache(maxsize=100)
def get_cached_zone_codes(zone_id, precision=7):
    """Cache polyfill results"""
    polygon = load_zone_polygon(zone_id)
    return frozenset(polyfill(polygon, precision=precision))

# First call computes
codes1 = get_cached_zone_codes("zone_1")

# Second call uses cache
codes2 = get_cached_zone_codes("zone_1")  # Instant!
```

## Integration with Other Libraries

### With GeoPandas

```python
import geopandas as gpd
from digipin import polyfill

# Load shapefile
gdf = gpd.read_file('city_boundaries.shp')

# Polyfill each polygon
gdf['digipin_codes'] = gdf['geometry'].apply(
    lambda geom: polyfill(geom, precision=6)
)

# Count codes per region
gdf['code_count'] = gdf['digipin_codes'].apply(len)

print(gdf[['name', 'code_count']])
```

### With Folium (Interactive Maps)

```python
import folium
from digipin import polyfill, decode

# Create map
m = folium.Map(location=[28.6229, 77.2130], zoom_start=13)

# Define zone
zone_polygon = [(28.6328, 77.2197), (28.6289, 77.2155), (28.6289, 77.2239)]

# Add polygon to map
folium.Polygon(
    locations=zone_polygon,
    color='blue',
    fill=True,
    popup='Delivery Zone'
).add_to(m)

# Get codes and plot cell centers
codes = polyfill(zone_polygon, precision=8)
for code in codes[:10]:  # Plot first 10
    lat, lon = decode(code)
    folium.CircleMarker(
        location=[lat, lon],
        radius=2,
        color='red',
        fill=True
    ).add_to(m)

m.save('zone_map.html')
```

## Troubleshooting

### ValueError: Polygon outside India bounds

**Problem:** Polygon coordinates are outside India's coverage area.

**Solution:** DIGIPIN only covers:
- Latitude: 2.5°N to 38.5°N
- Longitude: 63.5°E to 99.5°E

Ensure your polygon is within these bounds.

### ImportError: No module named 'shapely'

**Problem:** Shapely not installed.

**Solution:**
```bash
pip install digipinpy[geo]
```

### Memory Error with High Precision

**Problem:** Out of memory when using precision 9-10 on large polygons.

**Solution:** Use lower precision or split polygon into smaller regions.

## Best Practices

### 1. Choose Right Precision

```python
# Delivery zones: precision 6-7
delivery_codes = polyfill(zone, precision=7)  # ~250m cells

# Building-level: precision 8
building_codes = polyfill(zone, precision=8)  # ~60m cells

# Precise safety zones: precision 9
safety_codes = polyfill(zone, precision=9)  # ~15m cells
```

### 2. Validate Polygon Before Polyfill

```python
from shapely.geometry import Polygon
from shapely.validation import explain_validity

polygon = Polygon(coordinates)

if not polygon.is_valid:
    print(f"Invalid polygon: {explain_validity(polygon)}")
    polygon = polygon.buffer(0)  # Fix common issues
```

### 3. Close Your Polygon

```python
# ✓ GOOD - Polygon closed (first == last)
polygon = [
    (28.6328, 77.2197),
    (28.6289, 77.2155),
    (28.6289, 77.2239),
    (28.6328, 77.2197),  # Closes the loop
]

# ✗ BAD - Polygon not closed
polygon = [
    (28.6328, 77.2197),
    (28.6289, 77.2155),
    (28.6289, 77.2239),
    # Missing closing point
]
```

### 4. Use Sets for Fast Lookup

```python
from digipin import polyfill

# Convert list to set
zone_codes = set(polyfill(polygon, precision=7))

# Fast O(1) membership test
if customer_code in zone_codes:  # Instant lookup
    print("In zone")
```

## See Also

- [Getting Started](getting-started.md) - Basic DIGIPIN concepts
- [Use Cases](use-cases.md) - More real-world examples
- [API Reference](../DOCUMENTATION.md) - Complete function documentation
- [Shapely Documentation](https://shapely.readthedocs.io/) - Geometry operations
