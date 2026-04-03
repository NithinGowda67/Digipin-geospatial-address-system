"""
Data Science Workflow with DIGIPIN-Pandas

Demonstrates the pandas integration for efficient batch processing
of DIGIPIN encoding, decoding, and neighbor discovery operations.

Install with: pip install digipinpy[pandas]

SECURITY NOTE:
This is a demonstration script for local development only.
DO NOT use in production environments where stdout is logged,
as it prints location data that may be considered sensitive.
"""
import sys
import time
import pandas as pd
import numpy as np

# Ensure we can import the local packages
sys.path.append('.')

import digipin.pandas_ext  # Registers the 'digipin' accessor
from digipin import encode


def generate_random_data(n=10000):
    print(f"Generating {n} random coordinates in India...")
    # Rough India bounds
    lats = np.random.uniform(8.0, 37.0, n)
    lons = np.random.uniform(68.0, 97.0, n)
    return pd.DataFrame({'lat': lats, 'lon': lons})


def benchmark():
    df = generate_random_data(n=100_000)

    print("\n--- Benchmark: Encoding 100,000 rows ---")

    # Method 1: The Old Way (Standard .apply)
    start = time.time()
    _ = df.apply(lambda row: encode(row['lat'], row['lon']), axis=1)
    end = time.time()
    print(f"1. Standard .apply():   {end - start:.4f} seconds")

    # Method 2: The New Way (Digipin Accessor)
    start = time.time()
    df['digipin'] = df.digipin.encode('lat', 'lon')
    end = time.time()
    print(f"2. df.digipin.encode(): {end - start:.4f} seconds")

    print("\n--- Benchmark: Decoding 100,000 rows ---")
    start = time.time()
    coords = df.digipin.decode('digipin')
    end = time.time()
    print(f"1. df.digipin.decode(): {end - start:.4f} seconds")

    # Verify results (Note: This prints coordinates for demo purposes only)
    print(f"\nVerification: {coords.iloc[0]['latitude']:.6f}, {coords.iloc[0]['longitude']:.6f}")


def analysis_demo():
    print("\n--- Real World Analysis Demo ---")
    df = pd.DataFrame({
        'location': ['Dak Bhawan', 'Mumbai GPO', 'Bengaluru GPO'],
        'lat': [28.622788, 19.0760, 12.9716],
        'lon': [77.213033, 72.8777, 77.5946]
    })

    # 1. Encode
    df['code'] = df.digipin.encode('lat', 'lon')

    # 2. Get Hierarchy (Region Level 2)
    df['state_region'] = df.digipin.get_parent('code', level=2)

    # 3. Find Neighbors (for coverage analysis)
    df['coverage_cells'] = df.digipin.neighbors('code')

    print(df[['location', 'code', 'state_region', 'coverage_cells']])


if __name__ == "__main__":
    try:
        benchmark()
        analysis_demo()
    except ImportError as e:
        print(f"Error: {e}")
        print("\nMissing dependency. Run `pip install pandas` to test this example.")
