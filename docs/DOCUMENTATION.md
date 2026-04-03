# digipinpy - Complete Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start Guide](#quick-start-guide)
4. [Framework Integrations](#framework-integrations)
   - [Pandas Integration](#pandas-integration)
   - [Django Integration](#django-integration)
   - [FastAPI Integration](#fastapi-integration)
   - [Geospatial Polyfill](#geospatial-polyfill)
5. [Core Concepts](#core-concepts)
6. [API Reference](#api-reference)
7. [Usage Examples](#usage-examples)
8. [Technical Specification](#technical-specification)
9. [Testing & Validation](#testing--validation)
10. [Performance](#performance)
11. [Frequently Asked Questions](#frequently-asked-questions)

---

## Introduction

### What is DIGIPIN?

DIGIPIN (Digital Postal Index Number) is India's official national-level addressing grid system developed by the Department of Posts in collaboration with IIT Hyderabad and NRSC, ISRO. It provides a standardized, geo-coded addressing framework for the entire country.

### What's New in v1.5.0

**CSV Batch Processing & Interactive Visualization** - Non-Programmer Friendly!

Version 1.5.0 adds two game-changing features that make DIGIPIN accessible to everyone:

#### CSV Batch Processing (NEW)
- **`digipin convert` CLI** - Process thousands of addresses from CSV/Excel files
- **Auto-column Detection** - Automatically finds lat/lon columns
- **Excel Support** - Works with .xlsx and .xls files
- **Progress Bars** - Visual feedback with tqdm
- **Data Validation** - Built-in validation with `--validate` flag
- **Custom Precision** - Variable precision levels (1-10)

#### Interactive Visualization (NEW)
- **`plot_pins()`** - Visualize DIGIPIN codes on interactive Folium maps
- **`plot_coverage()`** - Create coverage maps for zones/areas
- **`plot_neighbors()`** - Visualize neighbor relationships
- **Color-Coding** - Beautiful color palettes by precision level
- **Marker Clustering** - Handle 1000+ codes efficiently
- **Export to HTML** - Standalone interactive map files

### What's New in v1.4.0

**Geospatial Polyfill** - Polygon-to-Code Conversion!

Version 1.4.0 adds **Polyfill** functionality for converting geographic polygons into DIGIPIN codes:

#### Polyfill Module (NEW)
- **`polyfill(polygon, precision)`** - Convert polygons to DIGIPIN codes
- **Grid Scan Algorithm** - Efficient polygon coverage calculation
- **Prepared Geometry** - Fast point-in-polygon checks with Shapely
- **Flexible Input** - Accepts Shapely Polygons or coordinate lists
- **Recommended Precision** - 6-8 for city/district zones (~1km to ~60m)

### What's New in v1.3.0

**FastAPI Integration** - Modern Microservices Support!

Version 1.3.0 completes the backend trinity with **FastAPI integration** for high-performance microservices and APIs:

#### FastAPI Integration (NEW)
- **Pydantic Models** - Type-safe data contracts with automatic validation
- **Pre-built APIRouter** - Plug-and-play REST API with 3 endpoints
- **Auto-generated Docs** - Beautiful Swagger UI and ReDoc documentation
- **High Performance** - Async/await support, ~10,000 requests/sec
- **Microservices Ready** - Perfect for serverless, AI/ML backends, IoT

### What's New in v1.2.0

**Framework Integrations** - Pandas & Django support!

Version 1.2.0 brings DIGIPIN to the Python ecosystem with native integrations for the most popular frameworks:

#### Django Integration
- **`DigipinField`** - Custom model field with automatic validation and normalization
- **`__within` lookup** - Hierarchical region queries via SQL LIKE
- **Auto-uppercase** - Codes automatically normalized in the database
- **Migration support** - Clean Django migrations via `deconstruct()`

#### Pandas Integration (NEW)
- **DataFrame accessor** - `df.digipin` namespace for data science workflows
- **Vectorized operations** - Encode/decode thousands of coordinates efficiently
- **Data validation** - Filter invalid codes in your DataFrames
- **Hierarchical grouping** - Aggregate data by regions using `get_parent()`
- **Neighbor discovery** - Find neighbors for every row in a DataFrame

#### Previous: v1.1.0 - Neighbor Discovery
- **`get_neighbors()`** - Find immediately adjacent grid cells
- **`get_disk()`** - Get all cells within a radius
- **`get_ring()`** - Get cells at a specific distance

See the [Framework Integrations](#framework-integrations) section for complete guides.

### Key Features

- **Universal Coverage**: Covers entire India including maritime Exclusive Economic Zone (EEZ)
- **Hierarchical Precision**: 10 levels from regional (~1000 km) to precise (~3.8 m)
- **Neighbor Discovery**: Find adjacent cells and expand search areas (NEW in v1.1.0)
- **Offline Capability**: Works without internet connectivity
- **Directional Properties**: Logical naming pattern enables geographic queries
- **Privacy Respecting**: Represents locations only, stores no personal information
- **Government Standard**: Official specification by Ministry of Communications

### Use Cases

- **Delivery Services**: Precise address identification and proximity-based routing
- **Emergency Response**: Quick location identification and resource discovery
- **Proximity Search**: Find nearby restaurants, stores, or services
- **Banking & KYC**: Enhanced address verification
- **Agriculture**: Farm and land parcel identification
- **Real Estate**: Property location standardization and neighborhood search
- **Tourism**: Hotel and tourist spot addressing
- **Government Services**: Census, voting, welfare schemes
- **Maritime Operations**: Offshore asset identification (oil rigs, platforms)

---

## Installation

### Requirements

- Python 3.7 or higher
- No external dependencies required

### Install from PyPI

```bash
# Core package (zero dependencies)
pip install digipinpy

# With CSV batch processing & Pandas integration
pip install digipinpy[pandas]

# With Django integration
pip install digipinpy[django]

# With FastAPI integration
pip install digipinpy[fastapi]

# With geospatial polyfill
pip install digipinpy[geo]

# With interactive visualization
pip install digipinpy[viz]

# Complete ecosystem (all integrations)
pip install digipinpy[pandas,django,fastapi,geo,viz]
```

### Install from Source

```bash
git clone https://github.com/DEADSERPENT/digipin.git
cd digipinpy
pip install -e .
```

### Development Installation

```bash
pip install digipinpy[dev]
```

Includes: pytest, pytest-cov, black, flake8, mypy

---

## Quick Start Guide

### Basic Encoding

```python
from digipin import encode

# Encode coordinates to DIGIPIN code
code = encode(28.622788, 77.213033)
print(code)  # Output: 39J49LL8T4
```

### Basic Decoding

```python
from digipin import decode

# Decode DIGIPIN code to coordinates
lat, lon = decode('39J49LL8T4')
print(f"Latitude: {lat:.6f}, Longitude: {lon:.6f}")
# Output: Latitude: 28.622788, Longitude: 77.213033
```

### Validation

```python
from digipin import is_valid

# Check if a DIGIPIN code is valid
print(is_valid('39J49LL8T4'))  # True
print(is_valid('INVALID123'))  # False
```

### Neighbor Discovery (NEW in v1.1.0)

```python
from digipin import encode, get_neighbors, get_disk

# Find nearby locations
my_location = encode(28.622788, 77.213033)

# Get all 8 immediate neighbors
neighbors = get_neighbors(my_location)
print(neighbors)  # ['39J49LL8T9', '39J49LL8TC', ...]

# Search within a radius
search_area = get_disk(my_location, radius=5)
print(f"Search area: {len(search_area)} cells")  # ~50 cells
```

---

## Framework Integrations

### Pandas Integration

The Pandas integration provides a DataFrame accessor for efficient geospatial data processing.

#### Installation

```bash
pip install digipinpy[pandas]
```

#### Quick Start

```python
import pandas as pd
import digipin.pandas_ext  # Register the accessor

df = pd.DataFrame({
    'name': ['Location A', 'Location B', 'Location C'],
    'lat': [28.622788, 19.076090, 13.082680],
    'lon': [77.213033, 72.877426, 80.270721]
})

# Encode coordinates to DIGIPIN codes
df['code'] = df.digipin.encode('lat', 'lon')

# Decode back to coordinates
coords = df.digipin.decode('code')
df[['decoded_lat', 'decoded_lon']] = coords

# Validate codes
df['is_valid'] = df.digipin.is_valid('code')

# Get parent regions for grouping
df['region'] = df.digipin.get_parent('code', level=4)

# Get neighbors for proximity searches
df['neighbors'] = df.digipin.neighbors('code')
```

#### API Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `.encode(lat_col, lon_col, precision=10)` | Encode coordinate columns | Series of DIGIPIN codes |
| `.decode(code_col)` | Decode to coordinates | DataFrame with lat/lon columns |
| `.is_valid(code_col)` | Validate codes | Boolean Series |
| `.get_parent(code_col, level)` | Get parent at hierarchy level | Series of parent codes |
| `.neighbors(code_col, direction='all')` | Get neighbors for each row | Series of neighbor lists |

#### Use Cases

**Data Cleaning:**
```python
# Filter to only valid codes
valid_df = df[df.digipin.is_valid('code')]

# Remove duplicates at city level (precision 6)
df['city_code'] = df.digipin.encode('lat', 'lon', precision=6)
df_unique = df.drop_duplicates('city_code')
```

**Regional Analysis:**
```python
# Group by state/region (first 2 characters)
df['state'] = df.digipin.get_parent('code', level=2)
state_stats = df.groupby('state').agg({'value': 'sum'})
```

**Proximity Search:**
```python
# Find nearby locations
df['search_area'] = df.digipin.neighbors('code')
expanded = df.explode('search_area')
# Join with points of interest
nearby = poi_df[poi_df['code'].isin(expanded['search_area'])]
```

### Django Integration

The Django integration provides a custom model field with automatic validation and database lookups.

#### Installation

```bash
pip install digipinpy[django]
```

#### Quick Start

```python
from django.db import models
from digipin.django_ext import DigipinField

class DeliveryLocation(models.Model):
    name = models.CharField(max_length=100)
    digipin = DigipinField()  # Auto-validates & normalizes!

    class Meta:
        indexes = [
            models.Index(fields=['digipin']),
        ]

# Create a location
location = DeliveryLocation.objects.create(
    name="Customer Home",
    digipin="39j49ll8t4"  # Auto-converted to uppercase: 39J49LL8T4
)

# Hierarchical queries with custom lookup
delhi_locations = DeliveryLocation.objects.filter(digipin__within='39')
specific_area = DeliveryLocation.objects.filter(digipin__within='39J49L')
```

#### Field Features

- **Auto-validation**: Invalid DIGIPIN codes raise `ValidationError`
- **Auto-normalization**: Lowercase codes converted to uppercase
- **Strict by default**: Only accepts full 10-character codes
- **Migration support**: Clean `deconstruct()` for Django migrations
- **Database-efficient**: Uses `CharField(max_length=10)` internally

#### Custom Lookups

**`__within` - Hierarchical Region Queries:**

```python
# Find all locations in Delhi region (starts with '39')
Location.objects.filter(digipin__within='39')

# Find in specific neighborhood
Location.objects.filter(digipin__within='39J49L')

# SQL translation: SELECT * FROM location WHERE digipin LIKE '39J49L%'
```

#### Django Admin Integration

```python
from django.contrib import admin
from .models import DeliveryLocation

@admin.register(DeliveryLocation)
class DeliveryLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'digipin', 'created_at']
    search_fields = ['name', 'digipin']
    list_filter = ['created_at']
```

#### Django REST Framework

```python
from rest_framework import serializers, viewsets

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLocation
        fields = ['id', 'name', 'digipin']
    # DigipinField validation happens automatically!

class LocationViewSet(viewsets.ModelViewSet):
    queryset = DeliveryLocation.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        region = self.request.query_params.get('region')
        if region:
            queryset = queryset.filter(digipin__within=region)
        return queryset
```

#### Use Cases

**Warehouse Management:**
```python
class Warehouse(models.Model):
    name = models.CharField(max_length=200)
    location = DigipinField(db_index=True)
    capacity = models.IntegerField()

# Find warehouses in Delhi region
delhi_warehouses = Warehouse.objects.filter(location__within='39')

# Aggregate by region
from django.db.models import Count
from django.db.models.functions import Substr

region_counts = (
    Warehouse.objects
    .annotate(region=Substr('location', 1, 2))
    .values('region')
    .annotate(count=Count('id'))
)
```

**Address Validation:**
```python
from django import forms

class AddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryLocation
        fields = ['name', 'digipin']

    # Validation happens automatically via DigipinField.validate()
```

### FastAPI Integration

The FastAPI integration provides Pydantic models and a pre-built APIRouter for modern microservices.

#### Installation

```bash
pip install digipinpy[fastapi]
```

#### Quick Start

```python
from fastapi import FastAPI
from digipin.fastapi_ext import router as digipin_router

app = FastAPI(
    title="DIGIPIN Microservice",
    description="High-performance geocoding API for India"
)

# Mount the pre-built router
app.include_router(digipin_router, prefix="/api/v1")

# Run with: uvicorn app:app --reload
# Visit: http://127.0.0.1:8000/docs for Swagger UI
```

#### Pydantic Models

| Model | Description | Validation |
|-------|-------------|------------|
| `Coordinate` | Lat/lon input | ge=2.5, le=38.5 for lat; ge=63.5, le=99.5 for lon |
| `DigipinRequest` | DIGIPIN code input | min_length=1, max_length=10, auto-uppercase |
| `EncodeResponse` | Encode endpoint response | code, precision |
| `DecodeResponse` | Decode endpoint response | lat, lon, optional bounds |

#### API Endpoints

**POST /encode** - Encode coordinates to DIGIPIN:
```bash
curl -X POST "http://localhost:8000/api/v1/encode?precision=10" \
  -H "Content-Type: application/json" \
  -d '{"lat": 28.622788, "lon": 77.213033}'

# Response: {"code": "39J49LL8T4", "precision": 10}
```

**GET /decode/{code}** - Decode DIGIPIN to coordinates:
```bash
curl "http://localhost:8000/api/v1/decode/39J49LL8T4?include_bounds=true"

# Response: {
#   "lat": 28.622788,
#   "lon": 77.213033,
#   "bounds": [28.6227, 28.6228, 77.2130, 77.2131]
# }
```

**GET /neighbors/{code}** - Get neighboring cells:
```bash
curl "http://localhost:8000/api/v1/neighbors/39J49LL8T4?direction=all"

# Response: {
#   "center": "39J49LL8T4",
#   "neighbors": ["39J49LL8T9", "39J49LL8TC", ...],
#   "count": 8
# }
```

#### Use Cases

**Microservices Architecture:**
```python
# main.py
from fastapi import FastAPI
from digipin.fastapi_ext import router as digipin_router

app = FastAPI()
app.include_router(digipin_router, prefix="/geocoding")

# Other routers
app.include_router(delivery_router, prefix="/delivery")
app.include_router(warehouse_router, prefix="/warehouse")
```

**AI/ML Backend:**
```python
from fastapi import FastAPI
from digipin.fastapi_ext import router as digipin_router

app = FastAPI()
app.include_router(digipin_router, prefix="/api/v1")

@app.post("/predict-delivery-time")
async def predict(customer_lat: float, customer_lon: float):
    from digipin import encode
    code = encode(customer_lat, customer_lon)
    # Use code for ML model prediction
    return {"delivery_zone": code, "estimated_time": "30 mins"}
```

**Serverless Deployment:**
```python
# Works with AWS Lambda, Google Cloud Functions, Azure Functions
from mangum import Mangum
from fastapi import FastAPI
from digipin.fastapi_ext import router as digipin_router

app = FastAPI()
app.include_router(digipin_router, prefix="/api/v1")

handler = Mangum(app)  # For AWS Lambda
```

### Geospatial Polyfill

The Polyfill module converts geographic polygons into sets of DIGIPIN codes, essential for geofencing and service area definition.

#### Installation

```bash
pip install digipinpy[geo]
```

#### Quick Start

```python
from digipin import polyfill, encode

# Define delivery zone (polygon)
delivery_zone = [
    (28.6328, 77.2197),  # Top
    (28.6289, 77.2155),  # Bottom Left
    (28.6289, 77.2239),  # Bottom Right
]

# Convert to DIGIPIN codes (precision 8 = ~60m)
zone_codes = polyfill(delivery_zone, precision=8)
print(f"Zone covered by {len(zone_codes)} codes")  # 53 codes

# Fast O(1) address validation
customer_code = encode(28.6310, 77.2200, precision=8)
if customer_code in zone_codes:
    print("Address IS in delivery zone!")
```

#### API Functions

| Function | Description | Returns |
|----------|-------------|---------|
| `polyfill(polygon, precision)` | Convert polygon to codes | List[str] |
| `get_polygon_boundary(codes)` | Get bounding box of codes | Tuple (min_lat, max_lat, min_lon, max_lon) |

#### Parameters

**polyfill():**
- `polygon`: Shapely Polygon object OR list of (lat, lon) tuples
- `precision`: Target DIGIPIN level (1-10)
  - Recommended: 6-8 for city/district zones
  - Warning: 9-10 on large areas generates massive lists

#### Algorithm

- **Grid Scan**: Scans polygon bounding box at target precision
- **Prepared Geometry**: Uses Shapely's `prep()` for fast checks
- **Center Point Testing**: Includes cell if center is inside polygon
- **Performance**: ~0.1s for typical delivery zone at precision 8

#### Use Cases

**Delivery Service:**
```python
# Define service area once
service_codes = polyfill(city_boundary, precision=7)

# Store in database
db.service_area.insert({"city": "Delhi", "codes": service_codes})

# Fast O(1) lookup for each order
if customer_code in service_codes:
    accept_order()
```

**Emergency Response:**
```python
# Pre-compute ambulance coverage zones
hospital_coverage = polyfill(response_time_5min_polygon, precision=8)

# Instant dispatch decisions
if incident_code in hospital_coverage:
    dispatch_ambulance(hospital_id)
```

**Flood Risk Assessment:**
```python
# Convert flood zone polygon to codes
flood_zone_codes = polyfill(flood_hazard_polygon, precision=7)

# Check if address is at risk
address_code = encode(property_lat, property_lon, precision=7)
if address_code in flood_zone_codes:
    flag_high_risk()
```

**Restaurant Delivery Zones:**
```python
# Define delivery radius as polygon
from shapely.geometry import Point

restaurant_point = Point(77.2200, 28.6310)
delivery_range = restaurant_point.buffer(0.01)  # ~1km radius

# Convert to codes
delivery_codes = polyfill(delivery_range, precision=8)

# Check order eligibility
if order_code in delivery_codes:
    accept_delivery()
```

#### Performance Tips

1. **Choose Right Precision**: Use 6-8 for zones, not 9-10
2. **Pre-compute Zones**: Calculate once, reuse many times
3. **Cache Results**: Store in database or Redis
4. **Bounded Polygons**: Limit polygon complexity for speed

### CSV Batch Processing

The CSV batch processing feature provides a command-line interface for converting large CSV/Excel files containing coordinates into DIGIPIN codes.

#### Installation

```bash
pip install digipinpy[pandas]
```

#### Quick Start

```bash
# Basic conversion (auto-detect lat/lon columns)
digipin convert addresses.csv

# Explicit columns and custom output
digipin convert warehouses.csv --lat-col latitude --lon-col longitude -o codes.csv

# Custom precision and validation
digipin convert data.csv -p 8 --validate -o output.csv --digipin-col code
```

#### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `input_file` | CSV/Excel file to process | Required |
| `--lat-col` | Latitude column name | Auto-detect |
| `--lon-col` | Longitude column name | Auto-detect |
| `-o, --output` | Output file path | `{input}_with_digipin.csv` |
| `--digipin-col` | DIGIPIN column name | `digipin` |
| `-p, --precision` | Precision level (1-10) | 10 |
| `--validate` | Validate all codes | False |

#### Auto-Detection

The CLI automatically detects latitude/longitude columns by recognizing common names:
- **Latitude**: `lat`, `latitude`, `Lat`, `Latitude`, `LAT`
- **Longitude**: `lon`, `lng`, `longitude`, `Longitude`, `LON`, `LNG`

#### Use Cases

**Logistics: Daily Order Processing**
```bash
# Morning: Convert overnight orders
digipin convert overnight_orders.csv --validate -o ready_to_ship.csv
```

**Real Estate: Property Database**
```bash
# Process entire property database
digipin convert properties.xlsx --lat-col prop_lat --lon-col prop_lon -o geocoded.csv
```

**Government: Address Standardization**
```bash
# Standardize census data
digipin convert census_2025.csv -p 8 -o census_with_digipin.csv
```

#### Performance

- **1,000 rows**: ~2 seconds
- **10,000 rows**: ~20 seconds
- **100,000 rows**: ~3 minutes
- Suitable for production data pipelines

### Interactive Visualization

The visualization module provides interactive Folium maps for exploring DIGIPIN codes and coverage areas.

#### Installation

```bash
pip install digipinpy[viz]
```

#### Quick Start

```python
from digipin import encode
from digipin.viz import plot_pins, plot_coverage, plot_neighbors

# Single location
m = plot_pins('39J49LL8T4')
m.save('map.html')

# Multiple locations with color-coding
codes = ['39J49LL8T4', '39J49LL8T5', '39J49LL8T6']
m = plot_pins(codes, color_by_precision=True, show_bounds=True)
m.save('locations.html')

# Coverage area
from digipin import polyfill
zone_polygon = [(28.63, 77.22), (28.62, 77.21), (28.62, 77.23)]
zone_codes = polyfill(zone_polygon, precision=8)
m = plot_coverage(zone_codes, title="Delivery Zone")
m.save('coverage.html')

# Neighbor visualization
m = plot_neighbors('39J49LL8T4', radius=2)
m.save('neighbors.html')
```

#### API Functions

**plot_pins(codes, ...)**

Visualize DIGIPIN codes on an interactive map.

Parameters:
- `codes`: Single code (str) or list of codes
- `map_object`: Existing Folium map (optional)
- `color_by_precision`: Color-code by precision level (default: True)
- `show_labels`: Show DIGIPIN code popups (default: True)
- `show_bounds`: Draw bounding box rectangles (default: True)
- `zoom`: Map zoom level (auto-calculated if None)
- `tiles`: Map tile provider (default: 'OpenStreetMap')
- `cluster`: Use marker clustering (default: False)
- `max_clusters`: Maximum markers to render (default: 1000)

**plot_coverage(codes, title, ...)**

Create coverage map for delivery zones or service areas.

Parameters:
- `codes`: List of DIGIPIN codes
- `title`: Map title (default: "DIGIPIN Coverage Map")
- `output_file`: Save to HTML file (optional)
- `**kwargs`: Additional arguments for plot_pins()

**plot_neighbors(center_code, ...)**

Visualize a DIGIPIN code and its neighbors.

Parameters:
- `center_code`: Central DIGIPIN code
- `include_neighbors`: Show neighbors (default: True)
- `radius`: Neighbor radius (default: 1)
- `output_file`: Save to HTML file (optional)

#### Features

- **Color Palettes**: 10 precision levels from dark red to turquoise
- **Interactive Popups**: Code details on click
- **Bounding Boxes**: Visual grid cell boundaries
- **Auto-Zoom**: Automatic zoom calculation
- **Marker Clustering**: Handle 1000+ codes efficiently
- **Standalone HTML**: Export to self-contained files

#### Use Cases

**Delivery Planning**
```python
# Visualize warehouse coverage
warehouse = encode(28.622788, 77.213033)
coverage = get_disk(warehouse, radius=10)
m = plot_coverage(coverage, title="Delivery Zone", output_file="zone.html")
```

**Business Intelligence**
```python
# Show customer distribution
customer_codes = [encode(lat, lon) for lat, lon in customer_locations]
m = plot_pins(customer_codes, cluster=True)
m.save('customers.html')
```

**Urban Planning**
```python
# Map service areas
service_area_codes = polyfill(city_boundary, precision=7)
m = plot_coverage(service_area_codes, title="Service Area")
m.save('service_map.html')
```

---

## Core Concepts

### Hierarchical Grid System

DIGIPIN uses a 10-level hierarchical grid subdivision:

| Level | Code Length | Grid Size | Approx. Distance | Use Case |
|-------|-------------|-----------|------------------|----------|
| 1 | 1 char | 9° × 9° | ~1000 km | Regional |
| 2 | 2 chars | 2.25° × 2.25° | ~250 km | State |
| 3 | 3 chars | 33.75' × 33.75' | ~62 km | District |
| 4 | 4 chars | 8.44' × 8.44' | ~15 km | City |
| 5 | 5 chars | 2.11' × 2.11' | ~4 km | Locality |
| 6 | 6 chars | 0.53' × 0.53' | ~1 km | Neighborhood |
| 7 | 7 chars | 0.13' × 0.13' | ~250 m | Block |
| 8 | 8 chars | 0.03' × 0.03' | ~60 m | Building |
| 9 | 9 chars | 0.5" × 0.5" | ~15 m | Property |
| 10 | 10 chars | 0.12" × 0.12" | ~3.8 m | Precise location |

### Spiral Labeling Pattern

DIGIPIN uses an anticlockwise spiral pattern for labeling grid cells:

```
Grid Layout (4×4):
     Col 0   Col 1   Col 2   Col 3
   +-------+-------+-------+-------+
R0 |   F   |   C   |   9   |   8   |  (North)
   +-------+-------+-------+-------+
R1 |   J   |   3   |   2   |   7   |
   +-------+-------+-------+-------+
R2 |   K   |   4   |   5   |   6   |
   +-------+-------+-------+-------+
R3 |   L   |   M   |   P   |   T   |  (South)
   +-------+-------+-------+-------+
  (West)                       (East)
```

- Starts at center: `2`
- Spirals anticlockwise: `2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → C → F → J → K → L → M → P → T`
- Adjacent symbols are geographic neighbors

### Character Alphabet

16 unambiguous symbols:
- **Numbers (8)**: 2, 3, 4, 5, 6, 7, 8, 9
- **Letters (8)**: C, F, J, K, L, M, P, T

**Excluded for clarity**: 0, 1, O, I, G, W, X

### Bounding Box

**Official Coverage Area:**
- **Latitude**: 2.5°N to 38.5°N
- **Longitude**: 63.5°E to 99.5°E
- **Coordinate System**: EPSG:4326 (WGS84 datum, epoch 2005)

**Coverage includes:**
- All land territory of India
- Maritime Exclusive Economic Zone (EEZ)
- Island territories (Andaman & Nicobar, Lakshadweep)
- Offshore assets (oil rigs, platforms)

---

## API Reference

### Core Functions

#### `encode(lat, lon, *, precision=10)`

Encode geographic coordinates to a DIGIPIN code.

**Parameters:**
- `lat` (float): Latitude in degrees North (2.5° to 38.5°)
- `lon` (float): Longitude in degrees East (63.5° to 99.5°)
- `precision` (int, optional): Code length (1-10 characters). Default: 10

**Returns:**
- `str`: DIGIPIN code

**Raises:**
- `ValueError`: If coordinates are outside the bounding box

**Example:**
```python
code = encode(28.622788, 77.213033)  # '39J49LL8T4'
regional = encode(28.622788, 77.213033, precision=4)  # '39J4'
```

---

#### `decode(code)`

Decode a DIGIPIN code to geographic coordinates.

**Parameters:**
- `code` (str): DIGIPIN code (10 characters)

**Returns:**
- `Tuple[float, float]`: (latitude, longitude) of cell center

**Raises:**
- `ValueError`: If code format is invalid

**Example:**
```python
lat, lon = decode('39J49LL8T4')  # (28.622788, 77.213033)
```

---

#### `is_valid(code)`

Validate a DIGIPIN code format.

**Parameters:**
- `code` (str): DIGIPIN code to validate

**Returns:**
- `bool`: True if valid, False otherwise

**Example:**
```python
is_valid('39J49LL8T4')  # True
is_valid('INVALID123')  # False
```

---

### Batch Operations

#### `batch_encode(coordinates, **kwargs)`

Encode multiple coordinate pairs in batch.

**Parameters:**
- `coordinates` (list): List of (lat, lon) tuples
- `**kwargs`: Additional arguments for `encode()`

**Returns:**
- `list`: List of DIGIPIN codes

**Example:**
```python
coords = [
    (28.622788, 77.213033),  # Delhi
    (12.9716, 77.5946),      # Bengaluru
    (19.0760, 72.8777),      # Mumbai
]
codes = batch_encode(coords)
# ['39J49LL8T4', '4P3JK852C9', '4FK5958823']
```

---

#### `batch_decode(codes)`

Decode multiple DIGIPIN codes in batch.

**Parameters:**
- `codes` (list): List of DIGIPIN codes

**Returns:**
- `list`: List of (lat, lon) tuples

**Example:**
```python
codes = ['39J49LL8T4', '4P3JK852C9', '4FK5958823']
coords = batch_decode(codes)
# [(28.622788, 77.213033), (12.9716, 77.5946), (19.0760, 72.8777)]
```

---

### Hierarchical Operations

#### `get_parent(code, level)`

Get parent DIGIPIN code at a higher (coarser) level.

**Parameters:**
- `code` (str): Full DIGIPIN code
- `level` (int): Parent level (1 to len(code)-1)

**Returns:**
- `str`: Parent code (truncated)

**Example:**
```python
code = '39J49LL8T4'
get_parent(code, 1)  # '3' (regional)
get_parent(code, 4)  # '39J4' (city)
get_parent(code, 6)  # '39J49L' (neighborhood)
```

---

#### `is_within(child_code, parent_code)`

Check if a DIGIPIN code is within a larger region.

**Parameters:**
- `child_code` (str): Code to check
- `parent_code` (str): Parent region code

**Returns:**
- `bool`: True if child is within parent region

**Example:**
```python
is_within('39J49LL8T4', '39J49L')  # True (same neighborhood)
is_within('39J49LL8T4', '39')      # True (same state region)
is_within('39J49LL8T4', '48')      # False (different region)
```

---

#### `get_bounds(code)`

Get the bounding box of a grid cell.

**Parameters:**
- `code` (str): DIGIPIN code (1-10 characters)

**Returns:**
- `Tuple[float, float, float, float]`: (min_lat, max_lat, min_lon, max_lon)

**Example:**
```python
min_lat, max_lat, min_lon, max_lon = get_bounds('39J49LL8T4')
# Returns boundaries of the ~3.8m × 3.8m cell
```

---

#### `encode_with_bounds(lat, lon, **kwargs)`

Encode and return code with grid cell boundaries.

**Parameters:**
- `lat` (float): Latitude
- `lon` (float): Longitude
- `**kwargs`: Additional arguments for `encode()`

**Returns:**
- `dict`: Dictionary with 'code', 'lat', 'lon', and 'bounds' keys

**Example:**
```python
result = encode_with_bounds(28.622788, 77.213033)
# {
#     'code': '39J49LL8T4',
#     'lat': 28.622788,
#     'lon': 77.213033,
#     'bounds': (28.622785, 28.622791, 77.213029, 77.213036)
# }
```

---

#### `decode_with_bounds(code)`

Decode and return coordinates with grid cell boundaries.

**Parameters:**
- `code` (str): DIGIPIN code

**Returns:**
- `dict`: Dictionary with 'code', 'lat', 'lon', and 'bounds' keys

**Example:**
```python
result = decode_with_bounds('39J49LL8T4')
# {
#     'code': '39J49LL8T4',
#     'lat': 28.622788,
#     'lon': 77.213033,
#     'bounds': (28.622785, 28.622791, 77.213029, 77.213036)
# }
```

---

### Neighbor Discovery Operations

#### `get_neighbors(code, direction='all')`

Get immediate neighboring grid cells for a DIGIPIN code.

**Parameters:**
- `code` (str): The central DIGIPIN code (1-10 characters)
- `direction` (str, optional): Which neighbors to fetch
  - `'all'`: 8 neighbors (default)
  - `'cardinal'`: 4 neighbors (N, S, E, W)
  - Specific: `'north'`, `'south'`, `'east'`, `'west'`, `'northeast'`, `'northwest'`, `'southeast'`, `'southwest'`

**Returns:**
- `List[str]`: Valid DIGIPIN codes for the neighbors

**Raises:**
- `ValueError`: If code is invalid or direction is not recognized

**Example:**
```python
# Get all 8 surrounding cells
neighbors = get_neighbors('39J49LL8T4')
# ['39J49LL8T9', '39J49LL8TC', '39J49LL8T5', ...]

# Get only cardinal directions
cardinal = get_neighbors('39J49LL8T4', direction='cardinal')
# ['39J49LL8T9', '39J49LL8T3', '39J49LL8T5', '39J49LL8TF']

# Get specific direction
north = get_neighbors('39J49LL8T4', direction='north')
# ['39J49LL8T9']
```

---

#### `get_ring(code, radius)`

Get all grid cells at exactly 'radius' distance from center (hollow ring).

**Parameters:**
- `code` (str): Center DIGIPIN code
- `radius` (int): Distance in cells (must be >= 1)

**Returns:**
- `List[str]`: Unique codes forming the ring at specified radius

**Raises:**
- `ValueError`: If radius < 1 or code is invalid

**Example:**
```python
# Get cells exactly 1 step away (8 immediate neighbors)
ring1 = get_ring('39J49LL8T4', radius=1)  # 8 neighbors

# Get cells exactly 2 steps away
ring2 = get_ring('39J49LL8T4', radius=2)  # Up to 16 cells
```

---

#### `get_disk(code, radius=1)`

Get all grid cells within a specific cell radius (filled disk).

**Parameters:**
- `code` (str): Center DIGIPIN code
- `radius` (int): Number of cell layers to expand (must be >= 0)
  - `0`: Just the center cell
  - `1`: 3×3 grid (center + 8 neighbors)
  - `2`: 5×5 grid (25 cells total)
  - `n`: (2n+1)×(2n+1) grid

**Returns:**
- `List[str]`: Unique codes covering the disk area, including center

**Raises:**
- `ValueError`: If radius < 0 or code is invalid

**Example:**
```python
# Center + 8 immediate neighbors (3×3 grid)
disk1 = get_disk('39J49LL8T4', radius=1)  # 9 cells

# 5×5 grid for wider search area
disk2 = get_disk('39J49LL8T4', radius=2)  # 25 cells

# Delivery search: Find warehouses within ~40m
# (Level 10 cells are ~3.8m, so radius=10 ≈ 38m)
customer_code = encode(lat, lon)
search_area = get_disk(customer_code, radius=10)
nearby_warehouses = db.query(Warehouse).filter(
    Warehouse.digipin.in_(search_area)
)
```

---

#### `get_surrounding_cells(code)`

Alias for `get_neighbors(code, direction='all')`. Returns all 8 immediate neighbors.

**Example:**
```python
neighbors = get_surrounding_cells('39J49LL8T4')  # 8 neighbors
```

---

#### `expand_search_area(code, radius=1)`

Alias for `get_disk(code, radius)`. Returns all cells within radius distance (including center).

**Example:**
```python
search_area = expand_search_area('39J49LL8T4', radius=5)
```

---

### Utility Functions

#### `is_valid_coordinate(lat, lon)`

Check if coordinates are within India's bounding box.

**Parameters:**
- `lat` (float): Latitude
- `lon` (float): Longitude

**Returns:**
- `bool`: True if within bounds

**Example:**
```python
is_valid_coordinate(28.622788, 77.213033)  # True
is_valid_coordinate(0, 0)                   # False
```

---

#### `get_precision_info(level=10)`

Get detailed precision information for a level.

**Parameters:**
- `level` (int): DIGIPIN level (1-10)

**Returns:**
- `dict`: Precision details

**Example:**
```python
info = get_precision_info(10)
# {
#     'level': 10,
#     'code_length': 10,
#     'grid_size_lat_deg': 3.38e-05,
#     'grid_size_lon_deg': 3.38e-05,
#     'approx_distance_m': 3.814,
#     'total_cells': 1099511627776,
#     'description': 'Precise location (~3.8 m)'
# }
```

---

#### `get_grid_size(level)`

Calculate grid cell size at a given level.

**Parameters:**
- `level` (int): DIGIPIN level (1-10)

**Returns:**
- `Tuple[float, float]`: (lat_degrees, lon_degrees) cell size

**Example:**
```python
lat_size, lon_size = get_grid_size(10)  # (3.38e-05, 3.38e-05)
```

---

#### `get_approx_distance(level)`

Get approximate linear distance for grid cell at a level.

**Parameters:**
- `level` (int): DIGIPIN level (1-10)

**Returns:**
- `float`: Approximate cell size in meters

**Example:**
```python
distance = get_approx_distance(10)  # 3.814 meters
```

---

### Constants and Imports

```python
# Core functions
from digipin import encode, decode, is_valid

# Batch operations
from digipin import batch_encode, batch_decode

# Hierarchical operations
from digipin import get_bounds, get_parent, is_within
from digipin import encode_with_bounds, decode_with_bounds

# Neighbor discovery (NEW in v1.1.0)
from digipin import get_neighbors, get_ring, get_disk
from digipin import get_surrounding_cells, expand_search_area

# Utilities
from digipin import is_valid_coordinate, get_precision_info
from digipin import get_grid_size, get_approx_distance

# Framework Integrations (NEW in v1.2.0)
import digipin.pandas_ext  # Enables df.digipin accessor (requires: pip install digipinpy[pandas])
from digipin.django_ext import DigipinField  # Django model field (requires: pip install digipinpy[django])

# Constants
from digipin import (
    LAT_MIN,          # 2.5 (minimum latitude)
    LAT_MAX,          # 38.5 (maximum latitude)
    LON_MIN,          # 63.5 (minimum longitude)
    LON_MAX,          # 99.5 (maximum longitude)
    DIGIPIN_ALPHABET, # '23456789CFJKLMPT' (16 symbols)
    DIGIPIN_LEVELS    # 10 (number of hierarchical levels)
)
```

---

## Usage Examples

### Example 1: Delivery Application

```python
from digipin import encode, decode, get_bounds

# Customer places order
customer_lat, customer_lon = 28.622788, 77.213033

# Generate DIGIPIN for delivery address
delivery_code = encode(customer_lat, customer_lon)
print(f"Delivery DIGIPIN: {delivery_code}")  # 39J49LL8T4

# Delivery agent uses code to navigate
target_lat, target_lon = decode(delivery_code)
print(f"Target location: {target_lat}, {target_lon}")

# Get precise delivery area boundaries
min_lat, max_lat, min_lon, max_lon = get_bounds(delivery_code)
print(f"Delivery zone: {min_lat} to {max_lat}, {min_lon} to {max_lon}")
```

### Example 2: Emergency Services

```python
from digipin import encode, is_within

# Emergency call with location
emergency_lat, emergency_lon = 12.9716, 77.5946
emergency_code = encode(emergency_lat, emergency_lon)

# Dispatch to nearest station in same district (level 3)
district_code = emergency_code[:3]  # '4P3'

# Check if ambulance location is in same district
ambulance_code = '4P3JK9XXXX'
if is_within(ambulance_code, district_code):
    print("Ambulance is in same district - dispatching")
else:
    print("Need to dispatch from different district")
```

### Example 3: Real Estate Listings

```python
from digipin import encode, get_parent

# Property location
property_lat, property_lon = 19.0760, 72.8777
property_code = encode(property_lat, property_lon)

# Create hierarchical listing
print(f"Precise location: {property_code}")              # 4FK5958823
print(f"Building: {get_parent(property_code, 8)}")       # 4FK59588
print(f"Block: {get_parent(property_code, 7)}")          # 4FK5958
print(f"Neighborhood: {get_parent(property_code, 6)}")   # 4FK595
print(f"Locality: {get_parent(property_code, 5)}")       # 4FK59
```

### Example 4: Agricultural Land Mapping

```python
from digipin import batch_encode, get_bounds

# Farm plot corners
corners = [
    (26.9124, 75.7873),  # Northwest
    (26.9124, 75.7883),  # Northeast
    (26.9114, 75.7883),  # Southeast
    (26.9114, 75.7873),  # Southwest
]

# Generate DIGIPIN codes for corners
plot_codes = batch_encode(corners)
print("Farm plot DIGIPIN codes:")
for i, code in enumerate(plot_codes):
    print(f"  Corner {i+1}: {code}")

# Calculate plot area using bounds
min_lat1, max_lat1, min_lon1, max_lon1 = get_bounds(plot_codes[0])
min_lat2, max_lat2, min_lon2, max_lon2 = get_bounds(plot_codes[2])

# Approximate area calculation (simplified)
lat_diff = abs(max_lat1 - min_lat2) * 111000  # meters
lon_diff = abs(max_lon2 - min_lon1) * 111000  # meters
area_sqm = lat_diff * lon_diff
print(f"Approximate plot area: {area_sqm:.2f} sq meters")
```

### Example 5: Tourism & Navigation

```python
from digipin import encode, decode, batch_decode

# Tourist spots
spots = {
    'India Gate': '39J5XXXXXX',
    'Red Fort': '39J6XXXXXX',
    'Qutub Minar': '39JXXXXXXX'
}

# Plan route by decoding all locations
for name, code in spots.items():
    lat, lon = decode(code)
    print(f"{name}: {lat:.6f}, {lon:.6f}")

# Batch decode for route optimization
codes = list(spots.values())
coordinates = batch_decode(codes)
print(f"Route coordinates: {coordinates}")
```

### Example 6: Neighbor Discovery & Proximity Search (NEW in v1.1.0)

```python
from digipin import encode, get_neighbors, get_disk, get_ring

# Find nearby locations
my_location = encode(28.622788, 77.213033)

# Get all 8 immediate neighbors
neighbors = get_neighbors(my_location)
print(f"Immediate neighbors: {len(neighbors)} cells")
# ['39J49LL8T9', '39J49LL8TC', '39J49LL8T5', ...]

# Get only cardinal directions (N, S, E, W)
cardinal = get_neighbors(my_location, direction='cardinal')
print(f"Cardinal neighbors: {len(cardinal)} cells")

# Get specific direction
north = get_neighbors(my_location, direction='north')
print(f"North neighbor: {north[0]}")

# Delivery zone expansion
warehouse_code = encode(28.6, 77.2, precision=8)
delivery_zone = get_disk(warehouse_code, radius=3)
print(f"Delivery zone: {len(delivery_zone)} cells (~180m radius)")

# Database query for nearby restaurants
customer_code = encode(lat, lon)
search_area = get_disk(customer_code, radius=10)  # ~40m radius
nearby_restaurants = db.query(Restaurant).filter(
    Restaurant.digipin.in_(search_area)
)

# Emergency response tiers
incident_code = encode(12.9716, 77.5946, precision=8)
tier1 = get_neighbors(incident_code)              # Immediate
tier2 = get_disk(incident_code, radius=5)         # 300m radius
tier3 = get_disk(incident_code, radius=10)        # 600m radius

# Progressive ring expansion
search_center = encode(28.5, 77.0, precision=7)
for radius in [1, 2, 3, 4, 5]:
    ring = get_ring(search_center, radius=radius)
    print(f"Ring {radius}: {len(ring)} cells (~{radius*250}m)")
```

---

## Technical Specification

### Algorithm Details

#### Encoding Algorithm

1. **Validate Coordinates**: Check if within bounding box (2.5-38.5°N, 63.5-99.5°E)
2. **Initialize Bounds**: Start with full India bounding box
3. **Hierarchical Subdivision** (repeat 10 times):
   - Divide current region into 4×4 grid
   - Calculate which sub-grid contains the point
   - Map grid position to symbol using spiral pattern
   - Append symbol to code
   - Narrow bounds to selected sub-grid
4. **Return Code**: 10-character string

#### Decoding Algorithm

1. **Validate Code**: Check format (10 chars, valid alphabet)
2. **Initialize Bounds**: Start with full India bounding box
3. **Hierarchical Lookup** (for each character):
   - Map character to grid position using spiral pattern
   - Divide current region into 4×4 grid
   - Select sub-grid at position
   - Update bounds to sub-grid
4. **Return Center**: Center point of final grid cell

#### Boundary Assignment Rules

For coordinates coinciding with grid lines:
- **Vertical lines (N-S)**: Assign to eastern (right) cell
- **Horizontal lines (E-W)**: Assign to northern (upper) cell
- **Intersections**: Assign to northeastern (top-right) cell
- **Exceptions**: Top-most (38.5°N) and right-most (99.5°E) boundaries assign to opposite side

#### Neighbor Discovery Algorithm (NEW in v1.1.0)

The neighbor discovery algorithm uses a robust coordinate-based approach:

1. **Decode Center**: Convert DIGIPIN code to lat/lon coordinates
2. **Calculate Grid Size**: Determine cell dimensions at current level
3. **Compute Offsets**: Calculate neighbor coordinates by adding/subtracting grid size
4. **Re-encode**: Convert neighbor coordinates back to DIGIPIN codes
5. **Validate**: Filter out codes that fall outside India's bounding box

This approach automatically handles:
- **Boundary Crossing**: When neighbors span different parent grids
- **Edge Cases**: Cells near India's geographic boundaries
- **Variable Precision**: Works consistently across all 10 hierarchical levels

**Performance Characteristics**:
- `get_neighbors()`: O(8) - constant time for 8 neighbors
- `get_ring(radius)`: O(8R) - linear in radius
- `get_disk(radius)`: O(R²) - quadratic in radius
- Typical execution: ~200μs for immediate neighbors

### Coordinate Reference System

- **Standard**: EPSG:4326
- **Datum**: WGS84 at epoch 2005
- **Units**: Decimal degrees
- **Precision**: Double-precision floating-point

### Grid Properties

- **Subdivision Factor**: 4×4 at each level
- **Total Levels**: 10
- **Total Cells at Level 10**: 4^10 × 4^10 = 1,099,511,627,776 cells
- **Cell Dimensions** (at equator):
  - Level 10: ~3.8m × 3.8m
  - Level 9: ~15m × 15m
  - Level 8: ~60m × 60m
  - Level 6: ~1km × 1km
  - Level 1: ~1000km × 1000km

---

## Testing & Validation

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=digipin --cov-report=html

# Run specific test
pytest tests/test_official_spec.py::TestOfficialSpecification::test_dak_bhawan_official_example -v
```

### Test Coverage

**Comprehensive test suite with 209 tests covering:**

1. **Official Specification Compliance** (29 tests)
   - Dak Bhawan official example (28.622788°N, 77.213033°E → `39J49LL8T4`)
   - Major cities across India
   - Round-trip encoding/decoding accuracy
   - Boundary conditions and edge cases
   - Validation and hierarchical operations
   - Grid system verification

2. **Neighbor Discovery** (29 tests - v1.1.0)
   - Immediate neighbor detection
   - Cardinal vs. all directions
   - Ring and disk expansion
   - Boundary edge cases
   - Multi-level neighbor queries

3. **Pandas Integration** (33 tests - v1.2.0)
   - DataFrame encoding/decoding
   - Column validation
   - Parent code extraction
   - Neighbor discovery
   - Error handling
   - Performance benchmarks

4. **Django Integration** (31 tests - v1.2.0)
   - Model field validation
   - Auto-normalization
   - Database operations
   - Custom lookups (`__within`)
   - Form validation
   - Migration support

5. **FastAPI Integration** (41 tests - v1.3.0)
   - Pydantic model validation
   - Encode/decode endpoints
   - Neighbors endpoint
   - Response schema validation
   - Real-world scenarios
   - Performance benchmarks

6. **Geospatial Polyfill** (tests - v1.4.0)
   - Polygon-to-code conversion
   - Shapely integration
   - Boundary calculations
   - Coverage testing

7. **CSV Batch Processing** (18 tests - NEW in v1.5.0)
   - Auto-column detection
   - Explicit column specification
   - Excel file support
   - Data validation
   - Large dataset handling
   - Error handling

8. **Interactive Visualization** (28 tests - NEW in v1.5.0)
   - Single/multiple code plotting
   - Color-coding by precision
   - Marker clustering
   - Coverage and neighbor maps
   - Polyfill integration
   - Error handling

### Validation Results

- **Total Tests**: 209 (100% passing)
- **Test Success Rate**: 100%
- **Official Example**: ✓ PASS
- **Round-trip Accuracy**: < 5m error
- **Edge Cases**: ✓ ALL PASS
- **Neighbor Discovery**: ✓ ALL PASS (v1.1.0)
- **Pandas Integration**: ✓ ALL PASS (v1.2.0)
- **Django Integration**: ✓ ALL PASS (v1.2.0)
- **FastAPI Integration**: ✓ ALL PASS (v1.3.0)
- **Geospatial Polyfill**: ✓ ALL PASS (v1.4.0)
- **CSV Batch Processing**: ✓ ALL PASS (NEW in v1.5.0)
- **Interactive Visualization**: ✓ ALL PASS (NEW in v1.5.0)
- **Specification Compliance**: 100%

---

## Performance

### Benchmarks

Tested on: Intel i5, Python 3.10

| Operation | Time (avg) | Throughput |
|-----------|------------|------------|
| Single encode | ~25 μs | ~40,000 ops/sec |
| Single decode | ~20 μs | ~50,000 ops/sec |
| Batch encode (100) | ~2.5 ms | ~40,000 ops/sec |
| Batch decode (100) | ~2.0 ms | ~50,000 ops/sec |
| Validation | ~5 μs | ~200,000 ops/sec |
| **Neighbor discovery** (v1.1.0) | ~200 μs | ~5,000 ops/sec |
| **get_disk(radius=1)** | ~300 μs | ~3,300 ops/sec |
| **get_disk(radius=10)** | ~4 ms | ~250 ops/sec |
| **get_ring(radius=5)** | ~1.5 ms | ~670 ops/sec |
| **Pandas encode (1000 rows)** (NEW) | ~5 sec | ~200 rows/sec |
| **Pandas decode (500 rows)** (NEW) | ~3 sec | ~167 rows/sec |
| **Django field validation** (NEW) | ~0.1 ms | ~10,000 ops/sec |

### Memory Usage

- **Library size**: < 50 KB
- **Runtime memory**: < 1 MB
- **Zero dependencies**: No external packages required

### Optimization Tips

1. **Batch Operations**: Use `batch_encode()` / `batch_decode()` for multiple locations
2. **Precision Control**: Use lower precision (level 6-8) when exact precision not needed
3. **Caching**: Cache frequently used codes in your application
4. **Validation**: Pre-validate coordinates before encoding to avoid exceptions

---

## Frequently Asked Questions

### General Questions

**Q: What is the difference between DIGIPIN and PIN code?**
A: PIN code (Postal Index Number) identifies a postal delivery area. DIGIPIN is a geographic grid code that identifies a precise ~3.8m location anywhere in India.

**Q: Does DIGIPIN replace traditional addresses?**
A: No, DIGIPIN complements traditional addresses by providing an additional geographic attribute.

**Q: Can I use DIGIPIN for navigation?**
A: Yes, DIGIPIN codes can be converted to lat/lon coordinates for navigation apps.

**Q: Is DIGIPIN unique for each location?**
A: Yes, each ~3.8m × 3.8m grid cell has a unique 10-character code.

### Technical Questions

**Q: What coordinate system should I use?**
A: Use EPSG:4326 (WGS84). If your coordinates are in a different system, convert them first.

**Q: Why does my decoded coordinate differ slightly from encoded?**
A: Decoding returns the center of the grid cell. Maximum deviation is ~2.7m (half diagonal of 3.8m cell).

**Q: Can I use partial codes?**
A: Yes, shorter codes represent larger areas. Use `precision` parameter when encoding.

**Q: How do I handle coordinates outside India?**
A: The library will raise a `ValueError`. DIGIPIN only covers India's bounding box.

**Q: Is the library thread-safe?**
A: Yes, all functions are pure and stateless, safe for concurrent use.

**Q: How do I find all locations within a certain distance?** (NEW)
A: Use `get_disk()` to get all cells within a radius. For example, `get_disk(code, radius=10)` returns all cells within ~10 grid cells. Calculate the radius based on your precision level (e.g., Level 10 cells are ~3.8m, so radius=10 ≈ 38m).

**Q: What's the difference between get_ring() and get_disk()?** (NEW)
A: `get_ring(code, radius)` returns only cells at exactly the specified distance (hollow ring), while `get_disk(code, radius)` returns all cells within and including that distance (filled disk). Use `get_disk()` for "nearby" searches and `get_ring()` for progressive expansion.

### Integration Questions

**Q: How do I integrate with Django/Flask?**
A: For Django, use the `DigipinField` model field (v1.2.0+). For Flask or other frameworks, import and use functions directly in your views/routes.

**Q: How do I use DIGIPIN with Pandas DataFrames?** (NEW in v1.2.0)
A: Install `digipinpy[pandas]` and import `digipin.pandas_ext`. This registers the `df.digipin` accessor for encoding, decoding, and validation on DataFrame columns.

**Q: How do I use DIGIPIN in Django models?** (NEW in v1.2.0)
A: Install `digipinpy[django]` and use `from digipin.django_ext import DigipinField`. Add it to your model like any CharField. It auto-validates and normalizes codes. Use the `__within` lookup for hierarchical queries.

**Q: Can I use this with GPS devices?**
A: Yes, convert GPS coordinates (lat/lon) to DIGIPIN using `encode()`.

**Q: How do I store DIGIPIN codes in database?**
A: Use Django's `DigipinField` for automatic validation, or store as `VARCHAR(10)` or `CHAR(10)`. Consider indexing for fast lookups.

**Q: Can I display DIGIPIN on maps?**
A: Yes, decode to coordinates and use any mapping library (Folium, Plotly, Google Maps).

**Q: Do the Pandas and Django integrations require additional dependencies?**
A: Yes. Pandas integration requires `pandas>=1.3.0` and `numpy>=1.21.0`. Django integration requires `django>=3.2`. The core package has zero dependencies.

---

## Package Structure

```
digipinpy/
├── digipin/
│   ├── __init__.py         # Public API exports
│   ├── encoder.py          # Coordinate → DIGIPIN encoding
│   ├── decoder.py          # DIGIPIN → Coordinate decoding
│   ├── neighbors.py        # Neighbor discovery (v1.1.0)
│   ├── pandas_ext.py       # Pandas integration (NEW in v1.2.0)
│   ├── django_ext.py       # Django integration (NEW in v1.2.0)
│   ├── utils.py            # Constants, validation, utilities
│   └── cli.py              # Command-line interface
├── tests/
│   ├── __init__.py
│   ├── test_official_spec.py     # Core DIGIPIN tests (29 tests)
│   ├── test_neighbors.py         # Neighbor discovery tests (29 tests)
│   ├── test_pandas_integration.py  # Pandas tests (NEW - 33 tests)
│   └── test_django_integration.py  # Django tests (NEW - 31 tests)
├── examples/
│   ├── basic_usage.py      # Basic examples
│   ├── advanced_usage.py   # Advanced examples
│   ├── delivery_app.py     # Real-world application
│   ├── neighbor_discovery.py  # Neighbor discovery examples
│   ├── pandas_usage.py     # Pandas integration examples (NEW)
│   └── django_example.py   # Django integration examples (NEW)
├── images/                  # Official specification diagrams
├── DOCUMENTATION.md         # This file (complete API reference)
├── README.md               # Quick start guide
├── CHANGELOG.md            # Version history
├── LICENSE                 # MIT License
├── pyproject.toml          # Package configuration
└── DIGIPIN_Technical_Document.md  # Official specification

```

---

## Support & Contributing

### Getting Help

- **GitHub Issues**: https://github.com/DEADSERPENT/digipin/issues
- **Email**: samarthsmg14@gmail.com

### Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest tests/ -v`)
6. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use Black for formatting (`black .`)
- Add type hints where appropriate
- Document all public functions

---

## License

MIT License

Copyright (c) 2025 SAMARTHA H V

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## References

1. Department of Posts, Ministry of Communications, Government of India. "Digital Postal Index Number (DIGIPIN) - Technical Document, Final Version." March 2025.

2. National Geospatial Policy 2022, Department of Science & Technology, Government of India.

3. EPSG:4326 - WGS 84 Coordinate Reference System. https://epsg.io/4326

---

**Last Updated**: December 2025
**Version**: 1.5.0
**Maintained by**: SAMARTHA H V & MR SHIVAKUMAR
