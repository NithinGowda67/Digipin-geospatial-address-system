"""
Real-world example: Simple delivery tracking system using DIGIPIN
"""

import sys
import io

# Fix Windows console encoding for unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from digipin import encode, decode, get_bounds, is_valid
from datetime import datetime

class DeliveryLocation:
    """Represents a delivery location with DIGIPIN code."""

    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.code = encode(lat, lon)

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_address_summary(self):
        """Get a summary of the location."""
        min_lat, max_lat, min_lon, max_lon = get_bounds(self.code)
        area = (max_lat - min_lat) * (max_lon - min_lon) * 111000 * 111000  # rough m²

        return {
            'name': self.name,
            'code': self.code,
            'coordinates': (self.lat, self.lon),
            'precision_area': f"{area:.2f} m²"
        }


class DeliveryTrip:
    """Represents a delivery trip with multiple stops."""

    def __init__(self, trip_id):
        self.trip_id = trip_id
        self.stops = []
        self.created_at = datetime.now()

    def add_stop(self, name, lat, lon):
        """Add a delivery stop."""
        location = DeliveryLocation(name, lat, lon)
        self.stops.append(location)
        return location.code

    def get_route(self):
        """Get the delivery route."""
        return [stop.code for stop in self.stops]

    def verify_location(self, code):
        """Verify if a code is in the delivery route."""
        return code in self.get_route()

    def print_route(self):
        """Print the delivery route."""
        print(f"\nDelivery Trip #{self.trip_id}")
        print(f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"Total Stops: {len(self.stops)}")
        print("\nRoute:")
        for i, stop in enumerate(self.stops, 1):
            print(f"  {i}. {stop.name:20} → {stop.code}")


# Example Usage
print("=" * 70)
print("DIGIPIN Delivery Tracking System")
print("=" * 70)

# Create a delivery trip
trip = DeliveryTrip("DL2025-001")

# Add delivery stops
print("\n📦 Adding delivery stops...")
trip.add_stop("Warehouse (New Delhi)", 28.6139, 77.2090)
trip.add_stop("Customer A (Gurgaon)", 28.4595, 77.0266)
trip.add_stop("Customer B (Noida)", 28.5355, 77.3910)
trip.add_stop("Customer C (Faridabad)", 28.4089, 77.3178)
trip.add_stop("Return Depot (Delhi)", 28.6692, 77.4538)

# Print the route
trip.print_route()

# Verify a delivery
print("\n" + "=" * 70)
print("Delivery Verification")
print("=" * 70)

# Driver scans a DIGIPIN code
scanned_code = "39J49LL8T4"  # Example warehouse code

if trip.verify_location(scanned_code):
    lat, lon = decode(scanned_code)
    print(f"✓ Code {scanned_code} verified!")
    print(f"  Location: ({lat:.6f}, {lon:.6f})")
    print(f"  Status: Valid delivery location")
else:
    print(f"✗ Code {scanned_code} not in route!")

# Show detailed info for a stop
print("\n" + "=" * 70)
print("Location Details")
print("=" * 70)

location = trip.stops[0]
details = location.get_address_summary()

print(f"\nLocation: {details['name']}")
print(f"DIGIPIN Code: {details['code']}")
print(f"Coordinates: {details['coordinates']}")
print(f"Precision Area: {details['precision_area']}")

# Calculate distance (rough estimate)
print("\n" + "=" * 70)
print("Distance Calculation")
print("=" * 70)


def calculate_distance(lat1, lon1, lat2, lon2):
    """Simple distance calculation (Euclidean approximation)."""
    # This is a rough approximation; use haversine for accurate results
    dlat = (lat2 - lat1) * 111000  # meters
    dlon = (lon2 - lon1) * 111000 * 0.78  # adjusted for latitude
    return (dlat**2 + dlon**2) ** 0.5


print("\nDistances between stops:")
for i in range(len(trip.stops) - 1):
    stop1 = trip.stops[i]
    stop2 = trip.stops[i + 1]

    distance = calculate_distance(stop1.lat, stop1.lon, stop2.lat, stop2.lon)

    print(f"  {stop1.code} → {stop2.code}: {distance/1000:.2f} km")

# Generate shareable codes
print("\n" + "=" * 70)
print("Shareable Delivery Codes")
print("=" * 70)

print("\nSend these codes to customers:")
for i, stop in enumerate(trip.stops[1:4], 1):  # Skip warehouse and depot
    print(f"  Customer {chr(64+i)}: Your delivery code is {stop.code}")
    print(f"  Share this link: https://maps.example.com/{stop.code}")

# Summary
print("\n" + "=" * 70)
print("Benefits of Using DIGIPIN")
print("=" * 70)

print("""
✓ Compact: Only 10 characters (easy to remember and share)
✓ Accurate: ~2 meter precision for exact delivery locations
✓ Offline: Works without internet connection
✓ Validated: Built-in checksum prevents typos
✓ Standardized: Same code format for all of India
✓ Shareable: Easy to communicate via SMS, email, or QR code
""")
