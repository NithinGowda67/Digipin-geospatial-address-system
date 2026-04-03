"""
Advanced usage examples for digipin-py
"""

import sys
import io

# Fix Windows console encoding for unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from digipin import (
    encode,
    decode,
    get_bounds,
    batch_encode,
    batch_decode,
    is_valid,
    get_precision_info,
)

# Example 1: Bounding Box
print("=" * 60)
print("Example 1: Bounding Box")
print("=" * 60)

code = "39J49LL8T4"  # Dak Bhawan, New Delhi
lat, lon = decode(code)
min_lat, max_lat, min_lon, max_lon = get_bounds(code)

print(f"DIGIPIN Code: {code}")
print(f"Center Point: ({lat:.6f}, {lon:.6f})")
print(f"Bounding Box:")
print(f"  Latitude:  {min_lat:.6f} to {max_lat:.6f}")
print(f"  Longitude: {min_lon:.6f} to {max_lon:.6f}")
print(f"  Width:  {(max_lon - min_lon) * 111000:.2f} meters")
print(f"  Height: {(max_lat - min_lat) * 111000:.2f} meters")
print()

# Example 2: Batch Operations
print("=" * 60)
print("Example 2: Batch Encoding and Decoding")
print("=" * 60)

coordinates = [
    (28.6139, 77.2090),  # New Delhi
    (19.0760, 72.8777),  # Mumbai
    (12.9716, 77.5946),  # Bengaluru
]

# Batch encode
codes = batch_encode(coordinates)
print("Batch Encoding:")
for (lat, lon), code in zip(coordinates, codes):
    print(f"  ({lat}, {lon}) → {code}")

print()

# Batch decode
decoded = batch_decode(codes)
print("Batch Decoding:")
for code, (lat, lon) in zip(codes, decoded):
    print(f"  {code} → ({lat:.4f}, {lon:.4f})")

print()

# Example 3: Validation
print("=" * 60)
print("Example 3: Validation")
print("=" * 60)

test_codes = [
    ("39J49LL8T4", "Valid DIGIPIN"),
    ("INVALID", "Too short"),
    ("RG9GB8KL@@", "Invalid characters"),
    ("12345", "Too short"),
    ("39J49LL8T4XXX", "Too long"),
]

for code, description in test_codes:
    valid = is_valid(code)
    status = "✓ Valid" if valid else "✗ Invalid"
    print(f"{status:12} {code:15} ({description})")
    if valid:
        try:
            lat, lon = decode(code)
            print(f"            → Decodes to: ({lat:.6f}, {lon:.6f})")
        except:
            pass

print()

# Example 4: Different Precision Levels
print("=" * 60)
print("Example 4: Different Precision Levels")
print("=" * 60)

lat, lon = 28.6139, 77.2090

for k in [3, 4, 5]:
    code = encode(lat, lon, precision=k)
    info = get_precision_info(k)

    print(f"\nPrecision Level k={k}:")
    print(f"  Code: {code}")
    print(f"  Length: {info['code_length']} characters")
    print(f"  Resolution: ~{info['approx_distance_m']:.2f} meters")
    print(f"  Description: {info['description']}")

print()

# Example 5: Variable Precision Encoding
print("=" * 60)
print("Example 5: Variable Precision Encoding")
print("=" * 60)

lat, lon = 28.6139, 77.2090

print(f"Original coordinates: ({lat}, {lon})")
print("\nDifferent precision levels:")

for precision_level in [5, 7, 10]:
    code = encode(lat, lon, precision=precision_level)
    info = get_precision_info(precision_level)

    print(f"\nPrecision {precision_level}:")
    print(f"  Code: {code}")
    print(f"  Description: {info['description']}")
    print(f"  Resolution: ~{info['approx_distance_m']:.2f} meters")

    # Full 10-character codes can be decoded
    if precision_level == 10:
        decoded_lat, decoded_lon = decode(code)
        print(f"  Decoded: ({decoded_lat:.6f}, {decoded_lon:.6f})")

print("\nUse Case: Share a 5-character code for approximate location")
print("to protect exact address privacy, or use full 10 characters")
print("for precise delivery locations.")
