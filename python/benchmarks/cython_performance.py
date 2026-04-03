"""
Performance Benchmark: Cython vs Pure Python

Compares the performance of Cython-optimized vs pure Python implementations.

Expected Results:
- Encoding: 10-15x speedup (40K → 400-600K ops/sec)
- Decoding: 10-15x speedup (50K → 500-750K ops/sec)
- Batch operations: Similar or better speedup

Usage:
    # Make sure Cython extension is compiled first:
    pip install cython
    cd python
    python setup.py build_ext --inplace

    # Run benchmark:
    python benchmarks/cython_performance.py
"""

import time
import statistics
from typing import Callable, List, Tuple

# Test data: Representative locations across India
TEST_COORDINATES = [
    (28.622788, 77.213033),  # Delhi - Dak Bhawan
    (12.9716, 77.5946),      # Bengaluru
    (19.0760, 72.8777),      # Mumbai
    (13.0827, 80.2707),      # Chennai
    (22.5726, 88.3639),      # Kolkata
    (26.9124, 75.7873),      # Jaipur
    (23.0225, 72.5714),      # Ahmedabad
    (17.3850, 78.4867),      # Hyderabad
    (11.0168, 76.9558),      # Coimbatore
    (15.3173, 75.7139),      # Hubli
]

TEST_CODES = [
    "39J49LL8T4",  # Delhi
    "58C4K9FF72",  # Bengaluru
    "48F4F8LM9C",  # Mumbai
    "5P7JK2J6F8",  # Chennai
    "3TT9T89F5M",  # Kolkata
    "3FK7CJ44P5",  # Jaipur
    "48369K3349",  # Ahmedabad
    "58238L7KLL",  # Hyderabad
    "68F5849MPM",  # Coimbatore
    "588K83T895",  # Hubli
]


def benchmark_function(
    func: Callable,
    args: List,
    iterations: int = 10000,
    warmup: int = 100
) -> dict:
    """
    Benchmark a function with multiple iterations.

    Args:
        func: Function to benchmark
        args: List of argument tuples
        iterations: Number of iterations
        warmup: Number of warmup runs

    Returns:
        Dictionary with timing statistics
    """
    # Warmup
    for _ in range(warmup):
        for arg_set in args:
            if isinstance(arg_set, tuple):
                func(*arg_set)
            else:
                func(arg_set)

    # Actual benchmark
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        for arg_set in args:
            if isinstance(arg_set, tuple):
                func(*arg_set)
            else:
                func(arg_set)
        end = time.perf_counter()
        times.append(end - start)

    # Calculate statistics
    total_ops = iterations * len(args)
    mean_time = statistics.mean(times)
    ops_per_sec = total_ops / sum(times)

    return {
        "mean_time_sec": mean_time,
        "total_ops": total_ops,
        "ops_per_sec": ops_per_sec,
        "min_time": min(times),
        "max_time": max(times),
    }


def compare_implementations():
    """Compare Cython vs Python implementations."""

    print("=" * 70)
    print("DIGIPIN Performance Benchmark: Cython vs Pure Python")
    print("=" * 70)
    print()

    # Import both backends explicitly
    try:
        from digipin.core_fast import (
            encode_fast,
            decode_fast,
            batch_encode_fast,
            batch_decode_fast,
        )
        cython_available = True
    except ImportError:
        print("⚠ Cython extension not available!")
        print("  Build it first: python setup.py build_ext --inplace")
        print()
        cython_available = False

    from digipin.encoder import encode as encode_py, batch_encode as batch_encode_py
    from digipin.decoder import decode as decode_py, batch_decode as batch_decode_py

    # Check what backend is active
    import digipin
    backend_info = digipin.get_backend_info()
    print(f"Active Backend: {backend_info['backend'].upper()}")
    print(f"Performance: {backend_info['performance']}")
    print(f"Description: {backend_info['description']}")
    print()

    # Benchmark configuration
    iterations = 5000
    print(f"Benchmark Configuration:")
    print(f"  - Test coordinates: {len(TEST_COORDINATES)}")
    print(f"  - Test codes: {len(TEST_CODES)}")
    print(f"  - Iterations: {iterations:,}")
    print(f"  - Total operations per test: {iterations * len(TEST_COORDINATES):,}")
    print()

    # ========================================================================
    # ENCODING BENCHMARK
    # ========================================================================
    print("-" * 70)
    print("ENCODING BENCHMARK")
    print("-" * 70)

    print("Testing Pure Python encode()...", end=" ", flush=True)
    py_encode_stats = benchmark_function(encode_py, TEST_COORDINATES, iterations)
    print(f"✓ {py_encode_stats['ops_per_sec']:,.0f} ops/sec")

    if cython_available:
        print("Testing Cython encode_fast()...", end=" ", flush=True)
        cy_encode_stats = benchmark_function(encode_fast, TEST_COORDINATES, iterations)
        print(f"✓ {cy_encode_stats['ops_per_sec']:,.0f} ops/sec")

        speedup = cy_encode_stats['ops_per_sec'] / py_encode_stats['ops_per_sec']
        print(f"\n📊 Encoding Speedup: {speedup:.1f}x")
        print(f"   Python:  {py_encode_stats['ops_per_sec']:>12,.0f} ops/sec")
        print(f"   Cython:  {cy_encode_stats['ops_per_sec']:>12,.0f} ops/sec")
    else:
        print("\n⚠ Skipping Cython benchmark (extension not built)")

    # ========================================================================
    # DECODING BENCHMARK
    # ========================================================================
    print()
    print("-" * 70)
    print("DECODING BENCHMARK")
    print("-" * 70)

    print("Testing Pure Python decode()...", end=" ", flush=True)
    py_decode_stats = benchmark_function(decode_py, TEST_CODES, iterations)
    print(f"✓ {py_decode_stats['ops_per_sec']:,.0f} ops/sec")

    if cython_available:
        print("Testing Cython decode_fast()...", end=" ", flush=True)
        cy_decode_stats = benchmark_function(decode_fast, TEST_CODES, iterations)
        print(f"✓ {cy_decode_stats['ops_per_sec']:,.0f} ops/sec")

        speedup = cy_decode_stats['ops_per_sec'] / py_decode_stats['ops_per_sec']
        print(f"\n📊 Decoding Speedup: {speedup:.1f}x")
        print(f"   Python:  {py_decode_stats['ops_per_sec']:>12,.0f} ops/sec")
        print(f"   Cython:  {cy_decode_stats['ops_per_sec']:>12,.0f} ops/sec")
    else:
        print("\n⚠ Skipping Cython benchmark (extension not built)")

    # ========================================================================
    # BATCH OPERATIONS BENCHMARK
    # ========================================================================
    print()
    print("-" * 70)
    print("BATCH OPERATIONS BENCHMARK")
    print("-" * 70)

    batch_iterations = iterations // 10  # Fewer iterations for batch

    print("Testing Pure Python batch_encode()...", end=" ", flush=True)
    py_batch_encode_stats = benchmark_function(
        batch_encode_py, [TEST_COORDINATES], batch_iterations
    )
    print(f"✓ {py_batch_encode_stats['ops_per_sec']:,.0f} ops/sec")

    if cython_available:
        print("Testing Cython batch_encode_fast()...", end=" ", flush=True)
        cy_batch_encode_stats = benchmark_function(
            batch_encode_fast, [TEST_COORDINATES], batch_iterations
        )
        print(f"✓ {cy_batch_encode_stats['ops_per_sec']:,.0f} ops/sec")

        speedup = cy_batch_encode_stats['ops_per_sec'] / py_batch_encode_stats['ops_per_sec']
        print(f"\n📊 Batch Encode Speedup: {speedup:.1f}x")
        print(f"   Python:  {py_batch_encode_stats['ops_per_sec']:>12,.0f} ops/sec")
        print(f"   Cython:  {cy_batch_encode_stats['ops_per_sec']:>12,.0f} ops/sec")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if cython_available:
        encode_speedup = cy_encode_stats['ops_per_sec'] / py_encode_stats['ops_per_sec']
        decode_speedup = cy_decode_stats['ops_per_sec'] / py_decode_stats['ops_per_sec']
        avg_speedup = (encode_speedup + decode_speedup) / 2

        print(f"Average Speedup: {avg_speedup:.1f}x")
        print()
        print("Target Achievement:")
        print(f"  ✓ Encoding: {encode_speedup:.1f}x (target: 10-15x)")
        print(f"  ✓ Decoding: {decode_speedup:.1f}x (target: 10-15x)")
        print()

        if avg_speedup >= 10:
            print("🎉 SUCCESS: Cython optimization achieved target performance!")
        elif avg_speedup >= 5:
            print("✓ GOOD: Significant performance improvement achieved")
        else:
            print("⚠ WARNING: Performance below target - check compilation flags")
    else:
        print("Build Cython extension to enable performance comparison:")
        print("  pip install cython")
        print("  cd python")
        print("  python setup.py build_ext --inplace")

    print()


if __name__ == "__main__":
    compare_implementations()
