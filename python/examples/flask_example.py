"""
Flask Integration Example

Demonstrates how to use DIGIPIN with Flask and Flask-SQLAlchemy.
Shows both the custom DigipinType for database models and the pre-built API blueprint.

Run this example:
    pip install digipinpy[flask]
    python examples/flask_example.py

Then visit:
    http://localhost:5000/api/digipin/health
    http://localhost:5000/warehouses
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from digipin.flask_ext import DigipinType, create_digipin_blueprint, validate_coordinates_request
from digipin import encode, decode, get_neighbors

# -------------------------------------------------------------------------
# App Setup
# -------------------------------------------------------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# -------------------------------------------------------------------------
# Database Models
# -------------------------------------------------------------------------


class Warehouse(db.Model):
    """
    Warehouse model using DigipinType for location storage.

    The DigipinType automatically:
    - Validates DIGIPIN format on insert/update
    - Normalizes to uppercase
    - Stores as VARCHAR(10)
    """
    __tablename__ = 'warehouses'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(DigipinType, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, default=1000)

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        lat, lon = decode(self.code)
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'capacity': self.capacity,
            'coordinates': {'lat': lat, 'lon': lon}
        }


# -------------------------------------------------------------------------
# Register Pre-built DIGIPIN API Blueprint
# -------------------------------------------------------------------------

# This adds all standard DIGIPIN endpoints:
# POST /api/digipin/encode
# GET  /api/digipin/decode/<code>
# GET  /api/digipin/neighbors/<code>
# GET  /api/digipin/disk/<code>
# POST /api/digipin/validate
# GET  /api/digipin/health

digipin_bp = create_digipin_blueprint(url_prefix='/api/digipin')
app.register_blueprint(digipin_bp)


# -------------------------------------------------------------------------
# Custom Application Endpoints
# -------------------------------------------------------------------------


@app.route('/warehouses', methods=['GET'])
def list_warehouses():
    """
    Get all warehouses.

    Example: GET /warehouses
    """
    warehouses = Warehouse.query.all()
    return jsonify([w.to_dict() for w in warehouses])


@app.route('/warehouses', methods=['POST'])
@validate_coordinates_request('lat', 'lon')
def create_warehouse():
    """
    Create a new warehouse.

    Example: POST /warehouses
    Body: {"name": "Delhi Hub", "lat": 28.622788, "lon": 77.213033, "capacity": 5000}
    """
    data = request.get_json()

    # Encode coordinates to DIGIPIN
    code = encode(data['lat'], data['lon'])

    # Check if warehouse already exists at this location
    existing = Warehouse.query.filter_by(code=code).first()
    if existing:
        return jsonify({'error': 'Warehouse already exists at this location'}), 409

    # Create new warehouse
    warehouse = Warehouse(
        code=code,
        name=data['name'],
        capacity=data.get('capacity', 1000)
    )

    db.session.add(warehouse)
    db.session.commit()

    return jsonify(warehouse.to_dict()), 201


@app.route('/warehouses/<int:warehouse_id>', methods=['GET'])
def get_warehouse(warehouse_id):
    """
    Get warehouse by ID.

    Example: GET /warehouses/1
    """
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    return jsonify(warehouse.to_dict())


@app.route('/warehouses/<int:warehouse_id>', methods=['DELETE'])
def delete_warehouse(warehouse_id):
    """
    Delete warehouse by ID.

    Example: DELETE /warehouses/1
    """
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    db.session.delete(warehouse)
    db.session.commit()
    return '', 204


@app.route('/warehouses/nearby', methods=['POST'])
@validate_coordinates_request('lat', 'lon')
def find_nearby_warehouses():
    """
    Find warehouses near a given location.

    Uses DIGIPIN neighbor discovery to find warehouses in adjacent grid cells.

    Example: POST /warehouses/nearby
    Body: {"lat": 28.6, "lon": 77.2, "radius": 2}
    """
    data = request.get_json()
    radius = int(data.get('radius', 1))

    # Encode customer location
    customer_code = encode(data['lat'], data['lon'], precision=8)

    # Get search area (customer cell + neighbors)
    from digipin import get_disk
    search_area = get_disk(customer_code, radius=radius)

    # Query warehouses in this area
    # We use prefix matching since warehouses are stored at precision 10
    # but we're searching at precision 8
    nearby = []
    for code_prefix in search_area:
        warehouses = Warehouse.query.filter(
            Warehouse.code.like(f'{code_prefix}%')
        ).all()
        nearby.extend(warehouses)

    # Remove duplicates and convert to dict
    unique_warehouses = {w.id: w for w in nearby}.values()

    return jsonify({
        'search_center': customer_code,
        'radius': radius,
        'search_area_size': len(search_area),
        'warehouses_found': len(unique_warehouses),
        'warehouses': [w.to_dict() for w in unique_warehouses]
    })


@app.route('/warehouses/region/<region_code>', methods=['GET'])
def warehouses_in_region(region_code):
    """
    Get all warehouses in a specific region (by DIGIPIN prefix).

    Example: GET /warehouses/region/39J4
    Returns all warehouses in the 39J4 region.
    """
    warehouses = Warehouse.query.filter(
        Warehouse.code.like(f'{region_code.upper()}%')
    ).all()

    return jsonify({
        'region': region_code.upper(),
        'count': len(warehouses),
        'warehouses': [w.to_dict() for w in warehouses]
    })


@app.route('/')
def index():
    """API documentation."""
    return jsonify({
        'name': 'DIGIPIN Flask Example',
        'description': 'Warehouse management system with DIGIPIN geocoding',
        'endpoints': {
            'warehouses': {
                'GET /warehouses': 'List all warehouses',
                'POST /warehouses': 'Create warehouse (requires lat, lon, name)',
                'GET /warehouses/<id>': 'Get warehouse by ID',
                'DELETE /warehouses/<id>': 'Delete warehouse',
                'POST /warehouses/nearby': 'Find nearby warehouses (requires lat, lon, optional radius)',
                'GET /warehouses/region/<code>': 'Get warehouses in region'
            },
            'digipin': {
                'POST /api/digipin/encode': 'Encode coordinates to DIGIPIN',
                'GET /api/digipin/decode/<code>': 'Decode DIGIPIN to coordinates',
                'GET /api/digipin/neighbors/<code>': 'Get neighboring cells',
                'GET /api/digipin/disk/<code>': 'Get cells within radius',
                'POST /api/digipin/validate': 'Validate DIGIPIN code',
                'GET /api/digipin/health': 'Health check'
            }
        },
        'examples': {
            'create_warehouse': 'POST /warehouses with {"name": "Delhi Hub", "lat": 28.622788, "lon": 77.213033}',
            'find_nearby': 'POST /warehouses/nearby with {"lat": 28.6, "lon": 77.2, "radius": 2}',
            'region_query': 'GET /warehouses/region/39J4'
        }
    })


# -------------------------------------------------------------------------
# Database Initialization
# -------------------------------------------------------------------------


def init_db():
    """Initialize database with sample data."""
    with app.app_context():
        db.create_all()

        # Check if we already have data
        if Warehouse.query.count() == 0:
            # Add sample warehouses
            sample_warehouses = [
                {'name': 'Dak Bhawan Hub', 'lat': 28.622788, 'lon': 77.213033, 'capacity': 5000},
                {'name': 'Connaught Place', 'lat': 28.631447, 'lon': 77.219186, 'capacity': 3000},
                {'name': 'Karol Bagh', 'lat': 28.651421, 'lon': 77.190391, 'capacity': 2500},
                {'name': 'South Extension', 'lat': 28.571826, 'lon': 77.223114, 'capacity': 3500},
            ]

            for data in sample_warehouses:
                code = encode(data['lat'], data['lon'])
                warehouse = Warehouse(
                    code=code,
                    name=data['name'],
                    capacity=data['capacity']
                )
                db.session.add(warehouse)

            db.session.commit()
            print(f"✓ Initialized database with {len(sample_warehouses)} warehouses")


# -------------------------------------------------------------------------
# Run Server
# -------------------------------------------------------------------------


if __name__ == '__main__':
    init_db()

    print("\n" + "="*60)
    print("DIGIPIN Flask Example Server")
    print("="*60)
    print("\nEndpoints available:")
    print("  - http://localhost:5000/                    (API docs)")
    print("  - http://localhost:5000/warehouses          (List warehouses)")
    print("  - http://localhost:5000/api/digipin/health  (Health check)")
    print("\nSample queries:")
    print("  curl http://localhost:5000/warehouses")
    print("  curl http://localhost:5000/api/digipin/decode/39J49LL8T4")
    print("  curl -X POST http://localhost:5000/warehouses/nearby \\")
    print("       -H 'Content-Type: application/json' \\")
    print("       -d '{\"lat\": 28.6, \"lon\": 77.2, \"radius\": 2}'")
    print("\n" + "="*60 + "\n")

    # Security: Use environment variable to control debug mode
    # Never use debug=True in production (enables code execution via browser)
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    app.run(debug=debug_mode, port=5000)
