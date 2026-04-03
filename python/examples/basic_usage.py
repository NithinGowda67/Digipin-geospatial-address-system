"""
DIGIPIN Basic Usage Examples
"""

from digipin import encode, decode, is_valid, batch_encode, get_parent, is_within

# Example 1: Basic encoding
lat, lon = 28.622788, 77.213033
code = encode(lat, lon)
print(f"Dak Bhawan, New Delhi: {code}")  # Output: 39J49LL8T4

# Example 2: Decoding
decoded_lat, decoded_lon = decode('39J49LL8T4')
print(f"Decoded: {decoded_lat:.6f}, {decoded_lon:.6f}")

# Example 3: Validation
print(f"Valid: {is_valid('39J49LL8T4')}")  # True

# Example 4: Batch encoding
cities = [(28.622788, 77.213033), (12.9716, 77.5946), (19.0760, 72.8777)]
codes = batch_encode(cities)
print(f"City codes: {codes}")

# Example 5: Hierarchical operations
parent = get_parent('39J49LL8T4', 4)
print(f"City-level code: {parent}")  # 39J4

print(f"Within region: {is_within('39J49LL8T4', '39')}")  # True
