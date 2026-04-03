"""
Neighbor Discovery Examples
============================

This example demonstrates the new neighbor discovery features in digipinpy v1.1.0.
These features enable proximity-based queries essential for location-based services.

Use Cases:
- Delivery routing: "Find warehouses near this address"
- Emergency services: "Which ambulances can reach this location?"
- Restaurant search: "What's within 100m of me?"
- Real estate: "Show properties in this neighborhood"
"""

from digipin import (
    encode,
    decode,
    get_neighbors,
    get_ring,
    get_disk,
    get_surrounding_cells,
    expand_search_area,
)


def example_1_basic_neighbors():
    """Example 1: Get immediate neighbors of a location."""
    print("=" * 60)
    print("Example 1: Basic Neighbor Discovery")
    print("=" * 60)

    # Your current location (Dak Bhawan, New Delhi)
    my_location = encode(28.622788, 77.213033)
    print(f"My location: {my_location}")

    # Get all 8 surrounding cells
    neighbors = get_neighbors(my_location)
    print(f"\nFound {len(neighbors)} neighboring cells:")
    for i, neighbor in enumerate(neighbors, 1):
        lat, lon = decode(neighbor)
        print(f"  {i}. {neighbor} -> ({lat:.6f}, {lon:.6f})")

    # Get only cardinal directions (N, S, E, W)
    cardinal = get_neighbors(my_location, direction='cardinal')
    print(f"\nCardinal neighbors (N, S, E, W): {len(cardinal)} cells")
    for direction, neighbor in zip(['N', 'E', 'S', 'W'], cardinal[:4]):
        print(f"  {direction}: {neighbor}")

    # Get a specific direction
    north = get_neighbors(my_location, direction='north')
    if north:
        print(f"\nNorth neighbor: {north[0]}")


def example_2_delivery_routing():
    """Example 2: Delivery zone expansion from warehouse."""
    print("\n" + "=" * 60)
    print("Example 2: Delivery Zone Expansion")
    print("=" * 60)

    # Warehouse location in Delhi
    warehouse_lat, warehouse_lon = 28.6, 77.2
    warehouse_code = encode(warehouse_lat, warehouse_lon, precision=8)
    print(f"Warehouse: {warehouse_code}")
    print(f"Location: ({warehouse_lat}, {warehouse_lon})")

    # Immediate delivery zone (adjacent cells)
    zone_immediate = get_neighbors(warehouse_code)
    print(f"\nImmediate zone: {len(zone_immediate)} cells")

    # Extended delivery zone (3-cell radius)
    # At level 8, cells are ~60m, so radius=3 ≈ 180m coverage
    zone_extended = get_disk(warehouse_code, radius=3)
    print(f"Extended zone (180m radius): {len(zone_extended)} cells")

    # In a real application, you would query your database:
    # nearby_customers = db.query(Order).filter(
    #     Order.delivery_digipin.in_(zone_extended)
    # )


def example_3_emergency_response():
    """Example 3: Emergency resource discovery."""
    print("\n" + "=" * 60)
    print("Example 3: Emergency Response Coverage")
    print("=" * 60)

    # Emergency incident location
    incident_lat, incident_lon = 12.9716, 77.5946  # Bengaluru
    incident_code = encode(incident_lat, incident_lon, precision=8)
    print(f"Incident location: {incident_code}")

    # Tier 1: Immediate response area (closest resources)
    tier1 = get_neighbors(incident_code)
    print(f"\nTier 1 (immediate): {len(tier1)} cells")

    # Tier 2: Extended search if tier 1 has no resources
    tier2 = get_disk(incident_code, radius=5)
    print(f"Tier 2 (300m radius): {len(tier2)} cells")

    # Tier 3: Wide-area search
    tier3 = get_disk(incident_code, radius=10)
    print(f"Tier 3 (600m radius): {len(tier3)} cells")

    # In a real emergency system:
    # ambulances_tier1 = Ambulance.objects.filter(
    #     current_digipin__in=tier1,
    #     status='available'
    # )
    # if not ambulances_tier1:
    #     ambulances_tier2 = Ambulance.objects.filter(...)


def example_4_restaurant_search():
    """Example 4: 'Find nearby' search for restaurants."""
    print("\n" + "=" * 60)
    print("Example 4: Restaurant Search Nearby")
    print("=" * 60)

    # User location in Mumbai
    user_lat, user_lon = 19.0760, 72.8777
    user_code = encode(user_lat, user_lon, precision=10)
    print(f"User location: {user_code}")
    print(f"Coordinates: ({user_lat}, {user_lon})")

    # Search within ~40m radius
    # Level 10 cells are ~3.8m, so radius=10 ≈ 38m
    search_radius = 10
    search_area = get_disk(user_code, radius=search_radius)
    print(f"\nSearch area ({search_radius*3.8:.1f}m radius): {len(search_area)} cells")

    # In a real app:
    # restaurants = Restaurant.objects.filter(
    #     digipin__in=search_area
    # ).order_by('rating')
    #
    # for restaurant in restaurants:
    #     distance = calculate_distance(user_code, restaurant.digipin)
    #     print(f"{restaurant.name} - {distance}m away - ★ {restaurant.rating}")


def example_5_concentric_rings():
    """Example 5: Concentric ring expansion for progressive search."""
    print("\n" + "=" * 60)
    print("Example 5: Progressive Ring Expansion")
    print("=" * 60)

    # Real estate search - expand until we find enough properties
    search_center = encode(28.5, 77.0, precision=7)  # Block level
    print(f"Search center: {search_center}")

    # Expand in rings
    for radius in [1, 2, 3, 4, 5]:
        ring = get_ring(search_center, radius=radius)
        print(f"\nRing {radius} (~{radius*250}m): {len(ring)} cells")

        # In a real estate app:
        # properties = Property.objects.filter(digipin__in=ring)
        # if len(properties) >= 10:
        #     break  # Found enough properties


def example_6_multi_level_search():
    """Example 6: Hierarchical search using different precision levels."""
    print("\n" + "=" * 60)
    print("Example 6: Multi-Level Hierarchical Search")
    print("=" * 60)

    base_lat, base_lon = 28.6, 77.2

    # Coarse search at neighborhood level (level 6, ~1km cells)
    coarse_code = encode(base_lat, base_lon, precision=6)
    coarse_area = get_disk(coarse_code, radius=2)
    print(f"Coarse search (neighborhood level):")
    print(f"  Code: {coarse_code}")
    print(f"  Coverage: {len(coarse_area)} cells (~5km radius)")

    # Fine search at building level (level 8, ~60m cells)
    fine_code = encode(base_lat, base_lon, precision=8)
    fine_area = get_disk(fine_code, radius=5)
    print(f"\nFine search (building level):")
    print(f"  Code: {fine_code}")
    print(f"  Coverage: {len(fine_area)} cells (~300m radius)")

    # Precise search (level 10, ~3.8m cells)
    precise_code = encode(base_lat, base_lon, precision=10)
    precise_area = get_disk(precise_code, radius=10)
    print(f"\nPrecise search (exact location):")
    print(f"  Code: {precise_code}")
    print(f"  Coverage: {len(precise_area)} cells (~40m radius)")


def example_7_convenience_aliases():
    """Example 7: Using convenience alias functions."""
    print("\n" + "=" * 60)
    print("Example 7: Convenience Functions")
    print("=" * 60)

    code = encode(12.9716, 77.5946)
    print(f"Location: {code}")

    # get_surrounding_cells() is an alias for get_neighbors(direction='all')
    surrounding = get_surrounding_cells(code)
    print(f"\nSurrounding cells: {len(surrounding)}")

    # expand_search_area() is an alias for get_disk()
    expanded = expand_search_area(code, radius=3)
    print(f"Expanded area (radius=3): {len(expanded)} cells")


def example_8_performance_demo():
    """Example 8: Performance characteristics."""
    print("\n" + "=" * 60)
    print("Example 8: Performance Benchmark")
    print("=" * 60)

    import time

    code = encode(28.622788, 77.213033)

    # Benchmark neighbor discovery
    start = time.time()
    iterations = 1000
    for _ in range(iterations):
        get_neighbors(code)
    elapsed = time.time() - start
    per_call = (elapsed / iterations) * 1000  # milliseconds
    print(f"Neighbor discovery: {per_call:.3f}ms per call")
    print(f"  ({iterations} iterations in {elapsed:.3f}s)")

    # Benchmark disk expansion
    start = time.time()
    iterations = 100
    for radius in [1, 5, 10]:
        for _ in range(iterations // 3):
            get_disk(code, radius=radius)
    elapsed = time.time() - start
    print(f"\nDisk expansion: {(elapsed/iterations)*1000:.3f}ms avg per call")
    print(f"  (Mixed radii: 1, 5, 10)")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("DIGIPIN Neighbor Discovery Examples (v1.1.0)")
    print("=" * 60 + "\n")

    example_1_basic_neighbors()
    example_2_delivery_routing()
    example_3_emergency_response()
    example_4_restaurant_search()
    example_5_concentric_rings()
    example_6_multi_level_search()
    example_7_convenience_aliases()
    example_8_performance_demo()

    print("\n" + "=" * 60)
    print("Examples Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("- Integrate neighbor discovery into your application")
    print("- Use get_disk() for radius-based searches")
    print("- Use get_neighbors() for immediate adjacency")
    print("- Combine with database queries for real-world apps")
    print("\nDocumentation: https://github.com/DEADSERPENT/digipin")
    print("=" * 60 + "\n")
