"""
Geospatial Polyfill Example for DIGIPIN

This script demonstrates how to convert a Polygon (e.g., a delivery zone)
into a list of DIGIPIN codes. This is crucial for geofencing and logistics.

Requirements:
    pip install digipinpy[geo]
"""

try:
    from digipin import polyfill, decode
    from shapely.geometry import Polygon
except ImportError:
    print("Error: This example requires geospatial dependencies.")
    print("Run: pip install digipinpy[geo]")
    exit(1)


def run_demo():
    print("--- DIGIPIN Polyfill Demo ---\n")

    # 1. Define a polygon (e.g., Connaught Place, New Delhi)
    # List of (Lat, Lon) tuples
    delivery_zone_coords = [
        (28.6328, 77.2197),  # Top
        (28.6289, 77.2155),  # Bottom Left
        (28.6289, 77.2239),  # Bottom Right
        (28.6328, 77.2197),  # Closing the loop
    ]

    print(f"Defining Delivery Zone (Triangle): {len(delivery_zone_coords)} points")
    print(f"Coordinates: {delivery_zone_coords}\n")

    # 2. Convert Polygon to DIGIPIN codes
    # Precision 8 = ~60m resolution (Building level)
    print("Calculating coverage at Precision 8 (~60m)...")
    codes = polyfill(delivery_zone_coords, precision=8)

    print(f"Result: {len(codes)} DIGIPIN codes cover this area.")
    if codes:
        print("Sample Codes:", codes[:5], "..." if len(codes) > 5 else "")
    else:
        print("No codes found (polygon may be outside India's bounds)")
        return

    # 3. Verification (Check centers)
    print("\nVerifying first 3 codes:")
    poly_shape = Polygon([(lon, lat) for lat, lon in delivery_zone_coords])

    from shapely.geometry import Point

    for code in codes[:3]:
        lat, lon = decode(code)
        # Note: Shapely uses (x, y) = (lon, lat)
        is_inside = poly_shape.contains(Point(lon, lat))
        status = "[INSIDE]" if is_inside else "[OUTSIDE]"
        print(f"  {code} -> ({lat:.5f}, {lon:.5f}) -> {status}")

    # 4. Use case example: Check if address is in delivery zone
    print("\n--- Use Case: Address Validation ---")
    test_address = (28.6310, 77.2200)  # Should be inside
    from digipin import encode

    test_code = encode(test_address[0], test_address[1], precision=8)
    print(f"Test Address: {test_address} -> {test_code}")

    if test_code in codes:
        print("[YES] Address IS in delivery zone!")
    else:
        print("[NO] Address is NOT in delivery zone")


if __name__ == "__main__":
    run_demo()
