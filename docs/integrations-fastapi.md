# FastAPI Integration

DIGIPIN-Py provides a pre-built FastAPI router with automatic API documentation and Pydantic validation.

## Installation

```bash
pip install digipinpy[fastapi]
```

**Requirements:** fastapi>=0.68.0, pydantic>=1.8.0, uvicorn>=0.15.0

## Quick Start

### Minimal Application

```python
from fastapi import FastAPI
from digipin.fastapi_ext import router as digipin_router

app = FastAPI(title="DIGIPIN API")

# Mount the pre-built router
app.include_router(digipin_router, prefix="/api/v1", tags=["digipin"])

# Run with: uvicorn app:app --reload
```

**That's it!** You now have a complete DIGIPIN API with:
- ✅ Encode endpoint
- ✅ Decode endpoint
- ✅ Neighbors endpoint
- ✅ Automatic validation
- ✅ Interactive docs at `/docs`

### Access the API

```bash
# Start server
uvicorn app:app --reload

# Visit interactive docs
# http://127.0.0.1:8000/docs
```

## Available Endpoints

### POST `/encode` - Encode Coordinates

Convert latitude/longitude to DIGIPIN code.

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

**Python Client:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/encode",
    json={"lat": 28.622788, "lon": 77.213033, "precision": 10}
)
print(response.json())
# {'code': '39J49LL8T4', 'precision': 10}
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/encode" \
  -H "Content-Type: application/json" \
  -d '{"lat": 28.622788, "lon": 77.213033, "precision": 10}'
```

### GET `/decode/{code}` - Decode DIGIPIN

Convert DIGIPIN code to coordinates.

**Request:**
```
GET /api/v1/decode/39J49LL8T4?include_bounds=true
```

**Response:**
```json
{
  "code": "39J49LL8T4",
  "lat": 28.622788,
  "lon": 77.213033,
  "bounds": {
    "min_lat": 28.622750,
    "max_lat": 28.622825,
    "min_lon": 77.213000,
    "max_lon": 77.213075
  }
}
```

**Python Client:**
```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/decode/39J49LL8T4",
    params={"include_bounds": True}
)
print(response.json())
```

**cURL:**
```bash
curl "http://localhost:8000/api/v1/decode/39J49LL8T4?include_bounds=true"
```

### GET `/neighbors/{code}` - Get Neighbors

Find neighboring cells.

**Request:**
```
GET /api/v1/neighbors/39J49LL8T4?direction=all
```

**Response:**
```json
{
  "code": "39J49LL8T4",
  "neighbors": [
    "39J49LL8T9",
    "39J49LL8TC",
    "39J49LL8TL",
    "39J49LL8T3",
    "39J49LL8T6",
    "39J49LL8T2",
    "39J49LL8T5",
    "39J49LL8T8"
  ],
  "count": 8
}
```

**Direction Options:**
- `all` - All 8 neighbors (default)
- `cardinal` - Only N, S, E, W (4 neighbors)
- `north`, `south`, `east`, `west` - Single direction

**Python Client:**
```python
import requests

# All neighbors
response = requests.get(
    "http://localhost:8000/api/v1/neighbors/39J49LL8T4"
)

# Only cardinal directions
response = requests.get(
    "http://localhost:8000/api/v1/neighbors/39J49LL8T4",
    params={"direction": "cardinal"}
)
```

## Pydantic Models

The router uses these validated models:

### EncodeRequest

```python
from pydantic import BaseModel, Field

class EncodeRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")
    precision: int = Field(10, ge=1, le=10, description="Precision level")
```

### EncodeResponse

```python
class EncodeResponse(BaseModel):
    code: str = Field(..., description="DIGIPIN code")
    precision: int = Field(..., description="Precision level used")
```

### DecodeResponse

```python
class BoundsModel(BaseModel):
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float

class DecodeResponse(BaseModel):
    code: str
    lat: float
    lon: float
    bounds: Optional[BoundsModel] = None
```

### NeighborsResponse

```python
class NeighborsResponse(BaseModel):
    code: str
    neighbors: List[str]
    count: int
```

## Custom Application

### Adding Authentication

```python
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from digipin.fastapi_ext import router as digipin_router

API_KEY = "your-secret-api-key"
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

app = FastAPI(title="Secure DIGIPIN API")

# Mount with authentication
app.include_router(
    digipin_router,
    prefix="/api/v1",
    tags=["digipin"],
    dependencies=[Depends(verify_api_key)]
)
```

**Usage:**
```python
import requests

headers = {"X-API-Key": "your-secret-api-key"}
response = requests.post(
    "http://localhost:8000/api/v1/encode",
    headers=headers,
    json={"lat": 28.622788, "lon": 77.213033}
)
```

### Adding Rate Limiting

```python
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from digipin.fastapi_ext import router as digipin_router

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Rate-Limited DIGIPIN API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Apply rate limit: 100 requests per minute
@app.middleware("http")
async def add_rate_limit(request: Request, call_next):
    limiter.check_rate_limit(key=get_remote_address(request), rate="100/minute")
    return await call_next(request)

app.include_router(digipin_router, prefix="/api/v1")
```

### Adding CORS

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from digipin.fastapi_ext import router as digipin_router

app = FastAPI(title="DIGIPIN API with CORS")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(digipin_router, prefix="/api/v1")
```

## Building Custom Endpoints

### Batch Encoding

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from digipin import batch_encode

app = FastAPI()

class BatchEncodeRequest(BaseModel):
    coordinates: List[tuple[float, float]]
    precision: int = 10

class BatchEncodeResponse(BaseModel):
    codes: List[str]
    count: int

@app.post("/api/batch-encode", response_model=BatchEncodeResponse)
async def batch_encode_endpoint(request: BatchEncodeRequest):
    try:
        codes = batch_encode(request.coordinates, precision=request.precision)
        return BatchEncodeResponse(codes=codes, count=len(codes))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Search Area

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from digipin import get_disk, encode

app = FastAPI()

class SearchAreaRequest(BaseModel):
    lat: float
    lon: float
    radius: int = 3
    precision: int = 7

class SearchAreaResponse(BaseModel):
    center_code: str
    area_codes: List[str]
    total_cells: int

@app.post("/api/search-area", response_model=SearchAreaResponse)
async def search_area_endpoint(request: SearchAreaRequest):
    center = encode(request.lat, request.lon, precision=request.precision)
    area = get_disk(center, radius=request.radius)

    return SearchAreaResponse(
        center_code=center,
        area_codes=area,
        total_cells=len(area)
    )
```

### Geofencing Check

```python
from fastapi import FastAPI
from pydantic import BaseModel
from digipin import encode, is_within

app = FastAPI()

class GeofenceRequest(BaseModel):
    lat: float
    lon: float
    service_area: str  # e.g., "39J49"
    precision: int = 7

class GeofenceResponse(BaseModel):
    customer_code: str
    service_area: str
    is_serviceable: bool

@app.post("/api/check-service-area", response_model=GeofenceResponse)
async def check_service_area(request: GeofenceRequest):
    customer_code = encode(request.lat, request.lon, precision=request.precision)
    serviceable = is_within(customer_code, request.service_area)

    return GeofenceResponse(
        customer_code=customer_code,
        service_area=request.service_area,
        is_serviceable=serviceable
    )
```

## Real-World Applications

### Delivery Service API

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from digipin import encode, get_disk

app = FastAPI(title="Delivery Service API")

# Service areas (in-memory for demo)
SERVICE_AREAS = {
    "north_delhi": "39J49",
    "south_delhi": "39J48",
    "east_delhi": "39J4C",
}

class DeliveryCheckRequest(BaseModel):
    customer_lat: float
    customer_lon: float
    area_name: str

class DeliveryCheckResponse(BaseModel):
    customer_code: str
    area_code: str
    can_deliver: bool
    estimated_time: int  # minutes

@app.post("/api/delivery/check", response_model=DeliveryCheckResponse)
async def check_delivery(request: DeliveryCheckRequest):
    # Encode customer location
    customer_code = encode(
        request.customer_lat,
        request.customer_lon,
        precision=7
    )

    # Get service area code
    area_code = SERVICE_AREAS.get(request.area_name)
    if not area_code:
        raise HTTPException(status_code=404, detail="Service area not found")

    # Check if in service area
    can_deliver = customer_code.startswith(area_code)

    return DeliveryCheckResponse(
        customer_code=customer_code,
        area_code=area_code,
        can_deliver=can_deliver,
        estimated_time=30 if can_deliver else -1
    )
```

### Store Locator API

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from digipin import encode, get_disk

app = FastAPI(title="Store Locator API")

# Mock store database
STORES = [
    {"id": 1, "name": "Store A", "code": "39J49LL8T4"},
    {"id": 2, "name": "Store B", "code": "39J49LL8T9"},
    {"id": 3, "name": "Store C", "code": "39J49LL8TC"},
]

class NearbyStoresRequest(BaseModel):
    lat: float
    lon: float
    radius: int = 2

class StoreInfo(BaseModel):
    id: int
    name: str
    code: str

class NearbyStoresResponse(BaseModel):
    customer_code: str
    stores: List[StoreInfo]
    count: int

@app.post("/api/stores/nearby", response_model=NearbyStoresResponse)
async def find_nearby_stores(request: NearbyStoresRequest):
    # Get customer location code
    customer_code = encode(request.lat, request.lon, precision=8)

    # Get search area
    search_codes = get_disk(customer_code, radius=request.radius)

    # Find stores in search area
    nearby = [
        store for store in STORES
        if store["code"] in search_codes
    ]

    return NearbyStoresResponse(
        customer_code=customer_code,
        stores=nearby,
        count=len(nearby)
    )
```

## Testing

### Using TestClient

```python
from fastapi.testclient import TestClient
from your_app import app

client = TestClient(app)

def test_encode_endpoint():
    response = client.post(
        "/api/v1/encode",
        json={"lat": 28.622788, "lon": 77.213033, "precision": 10}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "39J49LL8T4"
    assert data["precision"] == 10

def test_decode_endpoint():
    response = client.get("/api/v1/decode/39J49LL8T4")
    assert response.status_code == 200
    data = response.json()
    assert "lat" in data
    assert "lon" in data

def test_invalid_code():
    response = client.get("/api/v1/decode/INVALID")
    assert response.status_code == 400

def test_neighbors_endpoint():
    response = client.get("/api/v1/neighbors/39J49LL8T4")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 8
    assert len(data["neighbors"]) == 8
```

### Integration Tests

```python
import pytest
from fastapi.testclient import TestClient
from your_app import app

@pytest.fixture
def client():
    return TestClient(app)

def test_encode_decode_roundtrip(client):
    # Encode
    encode_response = client.post(
        "/api/v1/encode",
        json={"lat": 28.622788, "lon": 77.213033, "precision": 10}
    )
    code = encode_response.json()["code"]

    # Decode
    decode_response = client.get(f"/api/v1/decode/{code}")
    decoded = decode_response.json()

    # Verify coordinates match (approximately)
    assert abs(decoded["lat"] - 28.622788) < 0.0001
    assert abs(decoded["lon"] - 77.213033) < 0.0001
```

## Deployment

### Production Configuration

```python
# main.py
from fastapi import FastAPI
from digipin.fastapi_ext import router as digipin_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DIGIPIN API",
    version="1.0.0",
    docs_url="/docs" if DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if DEBUG else None,
)

app.include_router(digipin_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    logger.info("DIGIPIN API started")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("DIGIPIN API shutting down")
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
    restart: unless-stopped
```

### Running with Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with workers
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

## Performance Tips

1. **Use async/await for I/O operations:**
```python
@app.post("/api/custom")
async def custom_endpoint():
    # Use async for database calls, API requests, etc.
    result = await some_async_function()
    return result
```

2. **Enable response caching:**
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```

3. **Use response compression:**
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

## Troubleshooting

### 422 Validation Error

**Problem:** Request fails with 422 status.

**Solution:** Check Pydantic validation:
```json
{
  "detail": [
    {
      "loc": ["body", "lat"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

Ensure all required fields are provided.

### CORS Errors

**Problem:** Frontend can't access API.

**Solution:** Add CORS middleware (see CORS section above).

## See Also

- [Getting Started](getting-started.md) - Basic DIGIPIN concepts
- [API Reference](../DOCUMENTATION.md) - Complete function documentation
- [Use Cases](use-cases.md) - Real-world examples
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - FastAPI official docs
