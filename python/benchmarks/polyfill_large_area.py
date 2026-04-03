"""
Performance benchmark showing where quadtree excels: large areas at high precision.

Run with: python benchmarks/polyfill_large_area.py

Requires: pip install digipinpy[geo]
"""

import time
from typing import List, Tuple

try:
    from shapely.geometry import Polygon
    from digipin import polyfill
except ImportError:
    print("Error: This benchmark requires geospatial dependencies.")
    print("Run: pip install digipinpy[geo]")
    exit(1)


def benchmark_polyfill(
    polygon_coords: List[Tuple[float, float]],
    precision: int,
    algorithm: str,
    name: str,
) -> Tuple[int, float]:
    """Benchmark a polyfill operation."""
    start = time.time()
    codes = polyfill(polygon_coords, precision=precision, algorithm=algorithm)
    elapsed = time.time() - start

    print(f"  {name:15} {len(codes):8} codes in {elapsed:10.4f}s")
    return len(codes), elapsed


def main():
    print("=" * 80)
    print("DIGIPIN Polyfill: Where Quadtree Optimization Shines")
    print("=" * 80)
    print("\nQuadtree excels with:")
    print("  1. Large geographic areas (100s of km²)")
    print("  2. High precision levels (9-10)")
    print("  3. Sparse polygons (where most cells are skipped)")
    print()

    # Very Large Zone: ~1000 km² (state-level)
    print("\n1. Very Large Zone (~1000 km²) - Entire Delhi NCR Region")
    print("-" * 80)
    huge_zone = [
        (28.9000, 76.9000),
        (28.9000, 77.4000),
        (28.4000, 77.4000),
        (28.4000, 76.9000),
        (28.9000, 76.9000),
    ]

    print("\nAt Precision 7 (~250m cells):")
    _, time_grid = benchmark_polyfill(huge_zone, 7, "grid", "Grid Scan")
    _, time_quad = benchmark_polyfill(huge_zone, 7, "quadtree", "Quadtree")
    speedup = time_grid / time_quad if time_quad > 0 else 1.0
    print(f"  Speedup: {speedup:.2f}x")

    print("\nAt Precision 8 (~60m cells):")
    _, time_grid = benchmark_polyfill(huge_zone, 8, "grid", "Grid Scan")
    _, time_quad = benchmark_polyfill(huge_zone, 8, "quadtree", "Quadtree")
    speedup = time_grid / time_quad if time_quad > 0 else 1.0
    print(f"  Speedup: {speedup:.2f}x")

    # High Precision on Medium Zone
    print("\n\n2. High Precision (~15m) on City Zone (~25 km²)")
    print("-" * 80)
    city_zone = [
        (12.9800, 77.5900),
        (12.9800, 77.6100),
        (12.9600, 77.6100),
        (12.9600, 77.5900),
        (12.9800, 77.5900),
    ]

    print("\nAt Precision 9 (~15m cells):")
    _, time_grid = benchmark_polyfill(city_zone, 9, "grid", "Grid Scan")
    _, time_quad = benchmark_polyfill(city_zone, 9, "quadtree", "Quadtree")
    speedup = time_grid / time_quad if time_quad > 0 else 1.0
    print(f"  Speedup: {speedup:.2f}x")

    # Sparse polygon (thin corridor)
    print("\n\n3. Sparse Polygon: Thin Corridor (Highway corridor)")
    print("-" * 80)
    corridor = [
        (28.7000, 77.1000),
        (28.7010, 77.1000),
        (28.5010, 77.3000),
        (28.5000, 77.3000),
        (28.7000, 77.1000),
    ]

    print("\nAt Precision 8 (~60m cells):")
    _, time_grid = benchmark_polyfill(corridor, 8, "grid", "Grid Scan")
    _, time_quad = benchmark_polyfill(corridor, 8, "quadtree", "Quadtree")
    speedup = time_grid / time_quad if time_quad > 0 else 1.0
    print(f"  Speedup: {speedup:.2f}x")

    print("\n" + "=" * 80)
    print("Key Findings:")
    print("  - Grid scan is faster for small/medium areas (< 10 km²) at precision 6-8")
    print("  - Quadtree becomes faster when:")
    print("    * Area > 100 km² at precision 7+")
    print("    * Precision >= 9 (even for smaller areas)")
    print("    * Polygon is sparse (thin shapes with large bounding boxes)")
    print("  - For typical use cases (delivery zones at precision 7-8), both are fast")
    print("=" * 80)


if __name__ == "__main__":
    main()
