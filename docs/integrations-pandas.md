# Pandas Integration

DIGIPIN-Py provides a custom Pandas accessor for seamless DataFrame operations.

## Installation

```bash
pip install digipinpy[pandas]
```

**Requirements:** pandas>=1.3.0, numpy>=1.21.0

## Quick Start

```python
import pandas as pd
import digipin.pandas_ext  # Enables the .digipin accessor

df = pd.DataFrame({
    'location': ['Dak Bhawan', 'India Gate', 'Red Fort'],
    'lat': [28.622788, 28.612912, 28.656159],
    'lon': [77.213033, 77.229510, 77.240963]
})

# Encode coordinates to DIGIPIN codes
df['digipin_code'] = df.digipin.encode('lat', 'lon')

# Decode back to coordinates
df[['decoded_lat', 'decoded_lon']] = df.digipin.decode('digipin_code')

print(df)
```

## Available Methods

### `.digipin.encode(lat_col, lon_col, precision=10)`

Encode latitude/longitude columns to DIGIPIN codes.

```python
# Basic encoding
df['code'] = df.digipin.encode('latitude', 'longitude')

# With custom precision
df['district'] = df.digipin.encode('latitude', 'longitude', precision=5)
```

### `.digipin.decode(code_col)`

Decode DIGIPIN codes to coordinates.

```python
# Returns DataFrame with 'lat' and 'lon' columns
coords = df.digipin.decode('digipin_code')
df[['lat', 'lon']] = coords
```

### `.digipin.is_valid(code_col)`

Validate DIGIPIN codes.

```python
# Returns Series of booleans
df['is_valid'] = df.digipin.is_valid('digipin_code')

# Filter invalid codes
invalid_rows = df[~df['is_valid']]
```

### `.digipin.get_parent(code_col, level)`

Get parent codes at specified level.

```python
# Get district-level codes (level 5)
df['district'] = df.digipin.get_parent('digipin_code', level=5)

# Get immediate parent (level 9)
df['parent'] = df.digipin.get_parent('digipin_code', level=9)
```

### `.digipin.get_neighbors(code_col, direction='all')`

Get neighboring cells.

```python
# Get all 8 neighbors
df['neighbors'] = df.digipin.get_neighbors('digipin_code')

# Get only cardinal neighbors (N, S, E, W)
df['cardinal'] = df.digipin.get_neighbors('digipin_code', direction='cardinal')
```

## Real-World Examples

### Delivery Route Analysis

```python
import pandas as pd
import digipin.pandas_ext

# Load delivery data
deliveries = pd.DataFrame({
    'order_id': [1, 2, 3, 4, 5],
    'customer_lat': [28.6228, 28.6250, 28.6200, 28.6240, 28.6210],
    'customer_lon': [77.2130, 77.2150, 77.2100, 77.2140, 77.2120],
    'delivery_time_mins': [25, 30, 20, 35, 22]
})

# Encode to DIGIPIN (precision 7 = street level)
deliveries['location_code'] = deliveries.digipin.encode(
    'customer_lat', 'customer_lon', precision=7
)

# Get district codes for grouping
deliveries['district'] = deliveries.digipin.get_parent('location_code', level=5)

# Analyze delivery times by district
district_stats = deliveries.groupby('district').agg({
    'delivery_time_mins': ['mean', 'min', 'max', 'count']
}).round(2)

print("Delivery performance by district:")
print(district_stats)
```

### Customer Clustering

```python
import pandas as pd
import digipin.pandas_ext

# Customer database
customers = pd.read_csv('customers.csv')  # Has 'latitude', 'longitude' columns

# Encode to DIGIPIN
customers['digipin'] = customers.digipin.encode('latitude', 'longitude', precision=6)

# Count customers per region
region_counts = customers['digipin'].value_counts()

# Identify high-density areas (>100 customers)
high_density = region_counts[region_counts > 100]

print(f"Found {len(high_density)} high-density regions")
print("\nTop 5 regions:")
print(high_density.head())

# Get customers in top region
top_region = high_density.index[0]
top_customers = customers[customers['digipin'] == top_region]
```

### Spatial Join Simulation

```python
import pandas as pd
import digipin.pandas_ext

# Stores
stores = pd.DataFrame({
    'store_name': ['Store A', 'Store B', 'Store C'],
    'lat': [28.6228, 28.6250, 28.6200],
    'lon': [77.2130, 77.2150, 77.2100]
})
stores['code'] = stores.digipin.encode('lat', 'lon', precision=6)

# Customers
customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4],
    'lat': [28.6229, 28.6251, 28.6201, 28.6300],
    'lon': [77.2131, 77.2151, 77.2101, 77.2200]
})
customers['code'] = customers.digipin.encode('lat', 'lon', precision=6)

# Join on DIGIPIN code
merged = customers.merge(
    stores[['code', 'store_name']],
    on='code',
    how='left'
)

print("Customer-Store matches:")
print(merged[['customer_id', 'store_name']])
```

### Time-Series Location Analysis

```python
import pandas as pd
import digipin.pandas_ext

# Vehicle tracking data
tracking = pd.DataFrame({
    'timestamp': pd.date_range('2025-01-01', periods=100, freq='1min'),
    'lat': [28.622 + i*0.0001 for i in range(100)],
    'lon': [77.213 + i*0.0001 for i in range(100)]
})

# Encode locations
tracking['code'] = tracking.digipin.encode('lat', 'lon', precision=8)

# Detect location changes
tracking['location_changed'] = tracking['code'] != tracking['code'].shift()

# Count stops (locations where vehicle stayed for multiple readings)
stops = tracking.groupby((tracking['location_changed']).cumsum()).agg({
    'code': 'first',
    'timestamp': ['first', 'last', 'count']
}).reset_index(drop=True)

stops.columns = ['code', 'arrival', 'departure', 'duration_mins']
print("Vehicle stops:")
print(stops[stops['duration_mins'] > 5])  # Stops longer than 5 minutes
```

### Data Quality Validation

```python
import pandas as pd
import digipin.pandas_ext

# Dataset with potentially invalid coordinates
data = pd.read_csv('locations.csv')

# Encode (invalid coords will return NaN or raise warnings)
try:
    data['digipin'] = data.digipin.encode('lat', 'lon')
except Exception as e:
    print(f"Encoding error: {e}")

# Validate codes
data['is_valid'] = data.digipin.is_valid('digipin')

# Report data quality
total = len(data)
valid = data['is_valid'].sum()
invalid = total - valid

print(f"Data Quality Report:")
print(f"Total records: {total}")
print(f"Valid codes: {valid} ({valid/total*100:.1f}%)")
print(f"Invalid codes: {invalid} ({invalid/total*100:.1f}%)")

# Export invalid records for review
if invalid > 0:
    data[~data['is_valid']].to_csv('invalid_locations.csv', index=False)
```

### Aggregation by Geographic Region

```python
import pandas as pd
import digipin.pandas_ext

# Sales data
sales = pd.DataFrame({
    'date': pd.date_range('2025-01-01', periods=100),
    'lat': [28.622 + random.random()*0.01 for _ in range(100)],
    'lon': [77.213 + random.random()*0.01 for _ in range(100)],
    'amount': [random.randint(100, 1000) for _ in range(100)]
})

# Encode to district level (precision 5)
sales['district'] = sales.digipin.encode('lat', 'lon', precision=5)

# Aggregate by district and date
district_daily = sales.groupby(['district', sales['date'].dt.date]).agg({
    'amount': ['sum', 'mean', 'count']
}).round(2)

print("Daily sales by district:")
print(district_daily.head(10))
```

## Performance Tips

### 1. Batch Processing

The Pandas accessor automatically uses batch operations for efficiency:

```python
# ✓ Efficient - single vectorized operation
df['code'] = df.digipin.encode('lat', 'lon')

# ✗ Slow - row-by-row iteration
df['code'] = df.apply(lambda row: encode(row['lat'], row['lon']), axis=1)
```

### 2. Appropriate Precision

Use only the precision you need:

```python
# For district-level analysis, precision=5 is sufficient
df['district'] = df.digipin.encode('lat', 'lon', precision=5)

# Don't use precision=10 unless you need meter-level accuracy
```

### 3. Caching Parent Codes

```python
# Cache frequently used parent codes
df['district'] = df.digipin.get_parent('precise_code', level=5)

# Reuse for filtering
delhi_data = df[df['district'] == '39J49']
```

## Handling Missing Data

```python
import pandas as pd
import numpy as np
import digipin.pandas_ext

df = pd.DataFrame({
    'lat': [28.622788, np.nan, 28.656159],
    'lon': [77.213033, 77.229510, np.nan]
})

# Missing coordinates will result in NaN codes
df['code'] = df.digipin.encode('lat', 'lon')

# Check for missing codes
missing_count = df['code'].isna().sum()
print(f"Rows with missing codes: {missing_count}")

# Filter complete cases
complete = df.dropna(subset=['code'])
```

## Integration with GeoPandas

```python
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import digipin.pandas_ext

# Create GeoDataFrame
gdf = gpd.GeoDataFrame({
    'name': ['Location A', 'Location B'],
    'lat': [28.622788, 28.612912],
    'lon': [77.213033, 77.229510]
})

# Add geometry
gdf['geometry'] = gdf.apply(lambda row: Point(row['lon'], row['lat']), axis=1)

# Add DIGIPIN codes
gdf['digipin'] = gdf.digipin.encode('lat', 'lon')

# Now you can use both GeoPandas and DIGIPIN features
print(gdf.crs)  # GeoPandas coordinate reference system
print(gdf['digipin'])  # DIGIPIN codes
```

## See Also

- [Getting Started](getting-started.md) - Basic DIGIPIN concepts
- [Use Cases](use-cases.md) - More real-world examples
- [API Reference](../DOCUMENTATION.md) - Complete function documentation
