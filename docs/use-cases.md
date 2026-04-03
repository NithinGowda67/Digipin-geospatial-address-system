# DIGIPIN Use Cases

Real-world applications and implementation examples for DIGIPIN-Py.

## 🚚 Logistics & Delivery

### Delivery Zone Optimization

Define and manage delivery zones using DIGIPIN codes:

```python
from digipin import encode, get_disk, is_within

# Define delivery hub
hub_lat, hub_lon = 28.622788, 77.213033
hub_code = encode(hub_lat, hub_lon, precision=7)

# Calculate delivery zone (radius 5 = ~2km coverage)
delivery_zone = get_disk(hub_code, radius=5)

print(f"Delivery zone covers {len(delivery_zone)} cells")
# ~49 cells, each ~250m×250m

# Check if customer address is in delivery zone
customer_code = encode(28.625000, 77.215000, precision=7)
can_deliver = customer_code in delivery_zone

if can_deliver:
    print("✓ Delivery available")
else:
    print("✗ Outside delivery range")
```

### Route Optimization

```python
from digipin import encode, batch_encode

# Delivery addresses
addresses = [
    ("Customer A", 28.622788, 77.213033),
    ("Customer B", 28.625000, 77.215000),
    ("Customer C", 28.620000, 77.210000),
]

# Encode all addresses
delivery_data = []
for name, lat, lon in addresses:
    code = encode(lat, lon, precision=7)
    delivery_data.append({
        'customer': name,
        'code': code,
        'lat': lat,
        'lon': lon
    })

# Sort by DIGIPIN code for efficient routing
# (codes close in value = geographically close)
delivery_data.sort(key=lambda x: x['code'])

print("Optimized delivery sequence:")
for i, delivery in enumerate(delivery_data, 1):
    print(f"{i}. {delivery['customer']} - {delivery['code']}")
```

## 🚨 Emergency Services

### Incident Response Area

```python
from digipin import encode, get_ring, get_disk

# Emergency incident location
incident_lat, incident_lon = 19.076090, 72.877426
incident_code = encode(incident_lat, incident_lon, precision=8)

# Immediate response area (direct neighbors)
immediate_area = get_disk(incident_code, radius=1)

# Extended search area (within ~500m)
extended_area = get_ring(incident_code, distance=2)

print(f"Immediate response: {len(immediate_area)} cells")
print(f"Extended search: {len(extended_area)} cells")

# Alert all units in these zones
alert_zones = immediate_area + extended_area
```

### Hospital Coverage Analysis

```python
from digipin import encode, get_disk, get_parent

hospitals = [
    ("Apollo Hospital", 28.545074, 77.201936),
    ("AIIMS Delhi", 28.567373, 77.208924),
    ("Max Hospital", 28.543574, 77.274612),
]

# Calculate coverage for each hospital (5km radius)
coverage_map = {}
for name, lat, lon in hospitals:
    hospital_code = encode(lat, lon, precision=6)
    coverage = get_disk(hospital_code, radius=5)
    coverage_map[name] = coverage

# Find areas covered by multiple hospitals
all_codes = set()
for codes in coverage_map.values():
    all_codes.update(codes)

for code in all_codes:
    covering_hospitals = [
        name for name, codes in coverage_map.items()
        if code in codes
    ]
    if len(covering_hospitals) > 1:
        print(f"{code}: covered by {', '.join(covering_hospitals)}")
```

## 🏙️ Urban Planning

### Population Density Analysis

```python
import pandas as pd
from digipin import encode

# Load census data
population_data = pd.DataFrame({
    'locality': ['Area A', 'Area B', 'Area C'],
    'lat': [28.6229, 28.6250, 28.6200],
    'lon': [77.2130, 77.2150, 77.2100],
    'population': [50000, 75000, 30000]
})

# Encode to district-level codes (level 5)
population_data['district_code'] = population_data.apply(
    lambda row: encode(row['lat'], row['lon'], precision=5),
    axis=1
)

# Aggregate by district
district_stats = population_data.groupby('district_code').agg({
    'population': 'sum',
    'locality': 'count'
}).rename(columns={'locality': 'num_areas'})

print(district_stats)
```

### Zoning and Land Use

```python
from digipin import encode, get_parent, is_within

# Define zones
residential_zone = '39J49L'  # ~1km grid
commercial_zone = '39J49M'
industrial_zone = '39J48'

# Check building permit application
building_lat, building_lon = 28.622788, 77.213033
building_code = encode(building_lat, building_lon, precision=6)

# Verify zoning
if is_within(building_code, residential_zone):
    print("Residential zone - housing permitted")
elif is_within(building_code, commercial_zone):
    print("Commercial zone - business permitted")
elif is_within(building_code, industrial_zone):
    print("Industrial zone - factory permitted")
else:
    print("Unzoned area - special approval required")
```

## 📊 Data Analysis & Business Intelligence

### Customer Distribution Analysis

```python
import pandas as pd
import digipin.pandas_ext

# Load customer data
customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'lat': [28.622788, 28.625000, 19.076090, 28.620000, 19.080000],
    'lon': [77.213033, 77.215000, 72.877426, 77.210000, 72.880000]
})

# Encode to DIGIPIN
customers['digipin'] = customers.digipin.encode('lat', 'lon', precision=5)

# Get city/district code
customers['district'] = customers.digipin.get_parent('digipin', level=3)

# Analyze distribution
distribution = customers.groupby('district').size()
print("Customers by region:")
print(distribution)

# Identify high-density areas
high_density = customers['digipin'].value_counts()
print("\nHigh-density areas:")
print(high_density.head())
```

### Sales Heat Map

```python
from digipin import encode, get_parent

sales_data = [
    (28.622788, 77.213033, 15000),  # lat, lon, revenue
    (28.625000, 77.215000, 22000),
    (28.620000, 77.210000, 18000),
]

# Aggregate by region (precision 5 = ~1km)
revenue_by_region = {}
for lat, lon, revenue in sales_data:
    code = encode(lat, lon, precision=5)
    revenue_by_region[code] = revenue_by_region.get(code, 0) + revenue

# Find top-performing regions
sorted_regions = sorted(
    revenue_by_region.items(),
    key=lambda x: x[1],
    reverse=True
)

print("Top revenue regions:")
for code, revenue in sorted_regions[:5]:
    print(f"{code}: ₹{revenue:,}")
```

## 🗺️ Geofencing & Location Services

### Service Area Definition

```python
from digipin import polyfill, encode

# Define service boundary as polygon
service_boundary = [
    (28.6328, 77.2197),  # North
    (28.6289, 77.2155),  # West
    (28.6289, 77.2239),  # East
    (28.6328, 77.2197),  # Close polygon
]

# Convert to DIGIPIN codes (precision 7 = ~250m)
service_codes = polyfill(service_boundary, precision=7)

print(f"Service area: {len(service_codes)} cells")

# Fast O(1) lookup for customer address
customer_code = encode(28.6310, 77.2200, precision=7)
if customer_code in service_codes:
    print("✓ Customer in service area")
else:
    print("✗ Customer outside service area")
```

### Geo-Triggered Notifications

```python
from digipin import encode, get_neighbors

# Store location
store_lat, store_lon = 28.622788, 77.213033
store_code = encode(store_lat, store_lon, precision=8)

# Define notification zone (store + neighbors)
notification_zone = get_neighbors(store_code) + [store_code]

# Customer real-time location
customer_code = encode(28.622900, 77.213200, precision=8)

if customer_code in notification_zone:
    send_notification("You're near our store! Visit for 20% off!")
```

## 🏪 Retail & E-Commerce

### Store Locator

```python
from digipin import encode, batch_encode

stores = [
    ("Store A", 28.622788, 77.213033),
    ("Store B", 28.625000, 77.215000),
    ("Store C", 19.076090, 72.877426),
]

# Encode store locations
store_lookup = {}
for name, lat, lon in stores:
    code = encode(lat, lon, precision=6)
    store_lookup[code] = (name, lat, lon)

# Find nearest store
customer_lat, customer_lon = 28.623000, 77.213500
customer_code = encode(customer_lat, customer_lon, precision=6)

# Check if customer code matches any store zone
if customer_code in store_lookup:
    store_name, _, _ = store_lookup[customer_code]
    print(f"Nearest store: {store_name}")
else:
    print("No store in immediate area")
```

### Inventory Distribution

```python
from digipin import encode, get_parent

# Warehouse locations with inventory
warehouses = [
    ("Warehouse North", 28.622788, 77.213033, 1000),  # units
    ("Warehouse South", 19.076090, 72.877426, 1500),
]

# Encode warehouse zones
warehouse_zones = {}
for name, lat, lon, inventory in warehouses:
    zone_code = encode(lat, lon, precision=4)  # Large region
    warehouse_zones[zone_code] = {
        'name': name,
        'inventory': inventory
    }

# Route order to nearest warehouse
order_lat, order_lon = 28.625000, 77.215000
order_code = encode(order_lat, order_lon, precision=4)

if order_code in warehouse_zones:
    warehouse = warehouse_zones[order_code]
    print(f"Fulfill from: {warehouse['name']}")
    print(f"Available: {warehouse['inventory']} units")
```

## 🚗 Transportation & Mobility

### Ride-Hailing Zones

```python
from digipin import encode, get_disk

# High-demand pickup zones
demand_zones = [
    ("Airport", 28.556160, 77.100281),
    ("Railway Station", 28.643041, 77.220482),
    ("Mall", 28.631460, 77.218659),
]

# Create surge pricing zones
surge_zones = set()
for name, lat, lon in demand_zones:
    code = encode(lat, lon, precision=7)
    zone = get_disk(code, radius=2)
    surge_zones.update(zone)

# Check if ride request is in surge zone
ride_request_code = encode(28.556500, 77.100500, precision=7)
if ride_request_code in surge_zones:
    surge_multiplier = 1.5
    print(f"Surge pricing: {surge_multiplier}x")
```

### Parking Availability

```python
from digipin import encode, get_neighbors

# Parking lots with availability
parking_lots = {
    encode(28.622788, 77.213033, precision=8): {
        'name': 'Parking A',
        'available': 25,
        'total': 100
    },
    encode(28.623000, 77.213200, precision=8): {
        'name': 'Parking B',
        'available': 5,
        'total': 50
    }
}

# Find nearby parking
driver_code = encode(28.622900, 77.213100, precision=8)
nearby_codes = get_neighbors(driver_code) + [driver_code]

available_parking = []
for code in nearby_codes:
    if code in parking_lots and parking_lots[code]['available'] > 0:
        available_parking.append(parking_lots[code])

if available_parking:
    best_option = max(available_parking, key=lambda x: x['available'])
    print(f"Recommended: {best_option['name']}")
    print(f"Available: {best_option['available']}/{best_option['total']}")
```

## 🌾 Agriculture & Environment

### Farm Management

```python
from digipin import encode, polyfill

# Farm boundary
farm_boundary = [
    (20.5937, 78.9629),  # Coordinates in central India
    (20.5940, 78.9629),
    (20.5940, 78.9635),
    (20.5937, 78.9635),
]

# Divide farm into management zones
farm_zones = polyfill(farm_boundary, precision=9)  # ~15m grid

print(f"Farm divided into {len(farm_zones)} zones")

# Assign irrigation status
irrigation_zones = {
    zone: {'irrigated': False, 'last_watered': None}
    for zone in farm_zones
}
```

### Environmental Monitoring

```python
from digipin import encode

# Pollution monitoring stations
monitoring_data = [
    (28.622788, 77.213033, 125),  # lat, lon, AQI
    (28.625000, 77.215000, 158),
    (28.620000, 77.210000, 98),
]

# Create pollution map
pollution_map = {}
for lat, lon, aqi in monitoring_data:
    code = encode(lat, lon, precision=6)
    pollution_map[code] = aqi

# Alert if AQI > 150 in any zone
for code, aqi in pollution_map.items():
    if aqi > 150:
        print(f"⚠️ High pollution alert in zone {code}: AQI {aqi}")
```

## Best Practices

### Choosing Precision Level

```python
# Use appropriate precision for your use case
precision_guide = {
    3: "City/district-wide operations",
    5: "Neighborhood/locality services",
    7: "Street-level accuracy (delivery, transport)",
    8: "Building-level precision",
    10: "Exact location (emergency, mapping)"
}
```

### Caching for Performance

```python
from functools import lru_cache
from digipin import encode, get_disk

# Cache frequently accessed zones
@lru_cache(maxsize=1000)
def get_cached_delivery_zone(lat, lon, radius=5):
    code = encode(lat, lon, precision=7)
    return frozenset(get_disk(code, radius=radius))

# Use cached function
zone1 = get_cached_delivery_zone(28.622788, 77.213033)
zone2 = get_cached_delivery_zone(28.622788, 77.213033)  # Cached!
assert zone1 == zone2
```

### Database Indexing

```python
# PostgreSQL example
# CREATE INDEX idx_digipin ON locations (digipin_code);
# CREATE INDEX idx_digipin_prefix ON locations (LEFT(digipin_code, 5));

# Efficient hierarchical queries
# SELECT * FROM locations WHERE digipin_code LIKE '39J49%';  # All in district 39J49
```

## More Examples

See the [integrations](integrations-pandas.md) guides for framework-specific use cases:
- [Pandas Integration](integrations-pandas.md) - Data analysis workflows
- [Django Integration](integrations-django.md) - Web application examples
- [FastAPI Integration](integrations-fastapi.md) - Microservices and APIs
- [Geospatial Polyfill](geospatial-polyfill.md) - Advanced polygon operations
