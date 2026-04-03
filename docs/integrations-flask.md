# Flask Integration Guide

DIGIPIN-Py provides comprehensive Flask integration with custom SQLAlchemy types, request validation decorators, and a pre-built REST API blueprint.

## Installation

```bash
pip install digipinpy[flask]
```

This installs:
- `Flask` - Web framework
- `Flask-SQLAlchemy` - ORM integration
- Core DIGIPIN library

## Quick Start

### 1. Basic Flask App with Database

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from digipin.flask_ext import DigipinType

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'
db = SQLAlchemy(app)

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(DigipinType, nullable=False)
    name = db.Column(db.String(100))

# Create tables
with app.app_context():
    db.create_all()
```

### 2. Using the Pre-built API Blueprint

```python
from flask import Flask
from digipin.flask_ext import create_digipin_blueprint

app = Flask(__name__)

# Register DIGIPIN endpoints
digipin_bp = create_digipin_blueprint(url_prefix='/api/digipin')
app.register_blueprint(digipin_bp)

# Now these endpoints are available:
# POST /api/digipin/encode
# GET  /api/digipin/decode/<code>
# GET  /api/digipin/neighbors/<code>
# GET  /api/digipin/disk/<code>
# POST /api/digipin/validate
# GET  /api/digipin/health
```

## Features

### DigipinType (SQLAlchemy Field)

Custom SQLAlchemy type that:
- Auto-validates DIGIPIN format on insert/update
- Normalizes to uppercase
- Stores as VARCHAR(10)

```python
from digipin.flask_ext import DigipinType

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(DigipinType, nullable=False)
    name = db.Column(db.String(100))

# Insert with validation
loc = Location(code='39J49LL8T4', name='Dak Bhawan')
db.session.add(loc)
db.session.commit()  # Auto-validates and normalizes

# Query by region prefix
delhi_locations = Location.query.filter(
    Location.code.like('39%')
).all()
```

**Error Handling:**
```python
# Invalid code raises ValueError
try:
    bad_loc = Location(code='INVALID123')
    db.session.add(bad_loc)
    db.session.commit()
except ValueError as e:
    print(f"Validation failed: {e}")
```

### Request Validation Decorators

#### `@validate_digipin_request(*fields)`

Validates DIGIPIN codes in request JSON:

```python
from flask import Flask, request
from digipin.flask_ext import validate_digipin_request
from digipin import decode

app = Flask(__name__)

@app.route('/api/location', methods=['POST'])
@validate_digipin_request('code')
def get_location():
    data = request.get_json()
    # 'code' is guaranteed to be valid and uppercase
    lat, lon = decode(data['code'])
    return {'lat': lat, 'lon': lon}
```

**Features:**
- Validates format (characters and length)
- Auto-normalizes to uppercase
- Returns 400 with detailed error on failure

**Error Response Example:**
```json
{
  "error": "Invalid DIGIPIN code in field 'code': INVALID123",
  "valid_alphabet": "23456789CFJKLMPT",
  "valid_length": "1-10 characters"
}
```

#### `@validate_coordinates_request(lat_field, lon_field)`

Validates coordinates in request JSON:

```python
from digipin.flask_ext import validate_coordinates_request
from digipin import encode

@app.route('/api/encode', methods=['POST'])
@validate_coordinates_request('latitude', 'longitude')
def encode_location():
    data = request.get_json()
    # Coordinates are guaranteed valid
    code = encode(data['latitude'], data['longitude'])
    return {'code': code}
```

**Features:**
- Validates numeric type
- Validates India bounding box (2.5-38.5°N, 63.5-99.5°E)
- Converts to float automatically
- Returns 400 with range info on failure

## Pre-built API Blueprint

### Endpoints

#### POST `/encode`
Encode coordinates to DIGIPIN.

**Request:**
```json
{
  "lat": 28.622788,
  "lon": 77.213033,
  "precision": 10
}
```

**Response:**
```json
{
  "code": "39J49LL8T4",
  "precision": 10
}
```

#### GET `/decode/<code>`
Decode DIGIPIN to coordinates.

**Request:**
```
GET /decode/39J49LL8T4?include_bounds=true
```

**Response:**
```json
{
  "code": "39J49LL8T4",
  "lat": 28.622788,
  "lon": 77.213033,
  "bounds": {
    "min_lat": 28.622,
    "max_lat": 28.623,
    "min_lon": 77.212,
    "max_lon": 77.213
  }
}
```

#### GET `/neighbors/<code>`
Get neighboring cells.

**Request:**
```
GET /neighbors/39J49LL8T4?direction=cardinal
```

**Response:**
```json
{
  "center": "39J49LL8T4",
  "neighbors": ["39J49LL8T9", "39J49LL8T3", "..."],
  "count": 4
}
```

#### GET `/disk/<code>`
Get all cells within radius.

**Request:**
```
GET /disk/39J49LL8T4?radius=2
```

**Response:**
```json
{
  "center": "39J49LL8T4",
  "radius": 2,
  "cells": ["39J49LL8T4", "39J49LL8T5", "..."],
  "count": 25
}
```

#### POST `/validate`
Validate DIGIPIN code.

**Request:**
```json
{
  "code": "39J49LL8T4"
}
```

**Response:**
```json
{
  "code": "39J49LL8T4",
  "valid": true
}
```

#### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "digipin-api"
}
```

## Real-World Example

See `examples/flask_example.py` for a complete warehouse management system:

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from digipin.flask_ext import (
    DigipinType,
    create_digipin_blueprint,
    validate_coordinates_request
)
from digipin import encode, get_disk

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
db = SQLAlchemy(app)

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(DigipinType, nullable=False, unique=True)
    name = db.Column(db.String(100))
    capacity = db.Column(db.Integer)

# Register DIGIPIN API
digipin_bp = create_digipin_blueprint()
app.register_blueprint(digipin_bp)

@app.route('/warehouses/nearby', methods=['POST'])
@validate_coordinates_request('lat', 'lon')
def find_nearby():
    data = request.get_json()
    customer_code = encode(data['lat'], data['lon'], precision=8)
    search_area = get_disk(customer_code, radius=2)

    # Query warehouses in area
    nearby = []
    for code in search_area:
        warehouses = Warehouse.query.filter(
            Warehouse.code.like(f'{code}%')
        ).all()
        nearby.extend(warehouses)

    return jsonify({
        'warehouses': [w.to_dict() for w in nearby]
    })

if __name__ == '__main__':
    app.run(debug=True)
```

**Run the example:**
```bash
python examples/flask_example.py
```

**Test the API:**
```bash
# Create warehouse
curl -X POST http://localhost:5000/warehouses \
  -H 'Content-Type: application/json' \
  -d '{"name": "Delhi Hub", "lat": 28.6, "lon": 77.2, "capacity": 5000}'

# Find nearby warehouses
curl -X POST http://localhost:5000/warehouses/nearby \
  -H 'Content-Type: application/json' \
  -d '{"lat": 28.6, "lon": 77.2, "radius": 2}'

# Use DIGIPIN endpoints
curl http://localhost:5000/api/digipin/health
curl http://localhost:5000/api/digipin/decode/39J49LL8T4
```

## Best Practices

### 1. Database Indexing

Add indexes for common query patterns:

```python
class Location(db.Model):
    code = db.Column(DigipinType, nullable=False, index=True)
    # For prefix queries (region filtering)
```

### 2. Error Handling

Always handle validation errors:

```python
@app.errorhandler(ValueError)
def handle_validation_error(e):
    return jsonify({'error': str(e)}), 400
```

### 3. API Versioning

Version your custom endpoints:

```python
digipin_bp = create_digipin_blueprint(url_prefix='/api/v1/digipin')
```

### 4. Rate Limiting

Use Flask-Limiter for production:

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/encode', methods=['POST'])
@limiter.limit("100/hour")
@validate_coordinates_request('lat', 'lon')
def encode_endpoint():
    ...
```

## Testing

Use pytest with Flask test client:

```python
import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_encode_endpoint(client):
    response = client.post('/api/digipin/encode', json={
        'lat': 28.6,
        'lon': 77.2
    })
    assert response.status_code == 200
    assert 'code' in response.json
```

See `tests/test_flask_integration.py` for comprehensive test examples.

## Comparison with Django

| Feature | Flask | Django |
|---------|-------|--------|
| **Field Type** | `DigipinType` | `DigipinField` |
| **Auto-validation** | ✓ | ✓ |
| **Uppercase normalization** | ✓ | ✓ |
| **Custom lookups** | Manual (LIKE) | Built-in (`__within`) |
| **Request decorators** | ✓ | Manual validation |
| **Pre-built API** | Blueprint | Router (via FastAPI) |

**Choose Flask if:**
- You want lightweight microservices
- You need flexibility and minimal boilerplate
- You're building REST APIs

**Choose Django if:**
- You need an admin interface
- You want built-in ORM features (migrations, lookups)
- You're building full web applications

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

### Environment Variables

```python
import os

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///default.db'
)
```

## Next Steps

- Explore [FastAPI Integration](integrations-fastapi.md) for async APIs
- Learn about [Pandas Integration](integrations-pandas.md) for data processing
- See [Use Cases](use-cases.md) for real-world examples
