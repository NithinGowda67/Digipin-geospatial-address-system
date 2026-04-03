"""
Additional edge case tests for encoder.py, decoder.py, and utils.py.

These tests target specific uncovered lines to increase coverage.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from digipin import encoder, decoder, utils


class TestEncoderEdgeCases:
    """Additional edge cases for encoder.py."""

    def test_encode_precision_boundaries(self):
        """Test encoding at each precision level (1-10)."""
        lat, lon = 28.622788, 77.213033

        for precision in range(1, 11):
            result = encoder.encode(lat, lon, precision=precision)
            assert len(result) == precision
            assert all(c in utils.DIGIPIN_ALPHABET for c in result)

    def test_encode_at_exact_min_bounds(self):
        """Test encoding at exact minimum bounds."""
        # Exact southwest corner
        lat, lon = utils.LAT_MIN, utils.LON_MIN
        result = encoder.encode(lat, lon)
        assert len(result) == 10

    def test_encode_at_exact_max_bounds(self):
        """Test encoding at exact maximum bounds."""
        # Exact northeast corner
        lat, lon = utils.LAT_MAX, utils.LON_MAX
        result = encoder.encode(lat, lon)
        assert len(result) == 10

    def test_encode_with_bounds_structure(self):
        """Test encode_with_bounds returns complete structure."""
        result = encoder.encode_with_bounds(28.622788, 77.213033, precision=8)

        assert "code" in result
        assert "lat" in result
        assert "lon" in result
        assert "bounds" in result

        assert result["lat"] == 28.622788
        assert result["lon"] == 77.213033
        assert len(result["code"]) == 8
        assert len(result["bounds"]) == 4

    def test_encode_float_vs_integer_coords(self):
        """Test that encoding works with integer coordinates."""
        # Integer inputs should work
        result = encoder.encode(28, 77)
        assert isinstance(result, str)
        assert len(result) == 10

    def test_batch_encode_empty_list(self):
        """Test batch encoding with empty list."""
        result = encoder.batch_encode([])
        assert result == []

    def test_batch_encode_single_item(self):
        """Test batch encoding with single coordinate."""
        result = encoder.batch_encode([(28.622788, 77.213033)])
        assert len(result) == 1
        assert result[0] == "39J49LL8T4"

    def test_batch_encode_preserves_order(self):
        """Test that batch encoding preserves input order."""
        coords = [
            (28.622788, 77.213033),  # Delhi
            (12.9716, 77.5946),  # Bangalore
            (19.0760, 72.8777),  # Mumbai
        ]
        result = encoder.batch_encode(coords)

        # First result should correspond to first input
        assert result[0] == "39J49LL8T4"


class TestDecoderEdgeCases:
    """Additional edge cases for decoder.py."""

    def test_decode_case_insensitive(self):
        """Test that decoding is case-insensitive."""
        lat1, lon1 = decoder.decode("39J49LL8T4")
        lat2, lon2 = decoder.decode("39j49ll8t4")
        lat3, lon3 = decoder.decode("39J49ll8T4")  # Mixed case

        assert lat1 == lat2 == lat3
        assert lon1 == lon2 == lon3

    def test_decode_all_precision_levels(self):
        """Test decoding codes at all precision levels."""
        base_code = "39J49LL8T4"

        for level in range(1, 11):
            code = base_code[:level]
            lat, lon = decoder.decode(code)

            # Should return valid coordinates
            assert utils.LAT_MIN <= lat <= utils.LAT_MAX
            assert utils.LON_MIN <= lon <= utils.LON_MAX

    def test_decode_with_bounds_complete(self):
        """Test decode_with_bounds returns all fields."""
        result = decoder.decode_with_bounds("39J49LL8T4")

        # Check structure
        assert "code" in result
        assert "lat" in result
        assert "lon" in result
        assert "bounds" in result

        # Check values
        assert result["code"] == "39J49LL8T4"
        assert isinstance(result["lat"], float)
        assert isinstance(result["lon"], float)
        assert len(result["bounds"]) == 4

    def test_get_bounds_precision_consistency(self):
        """Test that bounds are consistent across precision levels."""
        # Lower precision bounds should contain higher precision bounds
        bounds_6 = decoder.get_bounds("39J49L")
        bounds_7 = decoder.get_bounds("39J49LL")

        min_lat_6, max_lat_6, min_lon_6, max_lon_6 = bounds_6
        min_lat_7, max_lat_7, min_lon_7, max_lon_7 = bounds_7

        # Level 7 bounds should be within level 6 bounds
        assert min_lat_6 <= min_lat_7
        assert max_lat_7 <= max_lat_6
        assert min_lon_6 <= min_lon_7
        assert max_lon_7 <= max_lon_6

    def test_get_parent_edge_cases(self):
        """Test get_parent with various inputs."""
        code = "39J49LL8T4"

        # Parent level 1
        assert decoder.get_parent(code, 1) == "3"

        # Parent level 5
        assert decoder.get_parent(code, 5) == "39J49"

        # Parent level 9
        assert decoder.get_parent(code, 9) == "39J49LL8T"

    def test_is_within_longer_parent(self):
        """Test is_within with same or longer parent."""
        code = "39J49LL8T4"
        # Child should be within shorter parent
        assert decoder.is_within(code, "39J49") is True

    def test_is_within_longer_child(self):
        """Test is_within when child is longer than parent."""
        parent = "39J"
        child = "39J49LL8T4"
        assert decoder.is_within(child, parent) is True

        # Reverse should be false
        assert decoder.is_within(parent, child) is False

    def test_batch_decode_empty(self):
        """Test batch decoding empty list."""
        result = decoder.batch_decode([])
        assert result == []

    def test_batch_decode_single(self):
        """Test batch decoding single code."""
        result = decoder.batch_decode(["39J49LL8T4"])
        assert len(result) == 1
        lat, lon = result[0]
        assert 28.6 < lat < 28.7
        assert 77.2 < lon < 77.3

    def test_batch_decode_preserves_order(self):
        """Test that batch decode preserves order."""
        codes = ["39J49LL8T4", "33J5T26TFP", "368TF2K98T"]
        results = decoder.batch_decode(codes)

        # Should have same length
        assert len(results) == len(codes)

        # First result should be Delhi
        lat1, lon1 = results[0]
        assert 28.6 < lat1 < 28.7
        assert 77.2 < lon1 < 77.3


class TestUtilsEdgeCases:
    """Additional edge cases for utils.py."""

    def test_validate_coordinate_exact_bounds(self):
        """Test validate_coordinate at exact boundary values."""
        # Exact minimum should work
        utils.validate_coordinate(utils.LAT_MIN, utils.LON_MIN)

        # Exact maximum should work
        utils.validate_coordinate(utils.LAT_MAX, utils.LON_MAX)

    def test_validate_coordinate_just_outside(self):
        """Test that coordinates just outside bounds raise error."""
        # Just below min latitude
        with pytest.raises(ValueError):
            utils.validate_coordinate(utils.LAT_MIN - 0.001, 77.0)

        # Just above max latitude
        with pytest.raises(ValueError):
            utils.validate_coordinate(utils.LAT_MAX + 0.001, 77.0)

        # Just below min longitude
        with pytest.raises(ValueError):
            utils.validate_coordinate(28.0, utils.LON_MIN - 0.001)

        # Just above max longitude
        with pytest.raises(ValueError):
            utils.validate_coordinate(28.0, utils.LON_MAX + 0.001)

    def test_validate_digipin_case_normalization(self):
        """Test that validate_digipin normalizes to uppercase."""
        result = utils.validate_digipin("39j49ll8t4")
        assert result == "39J49LL8T4"

        result = utils.validate_digipin("39J49ll8T4")  # Mixed case
        assert result == "39J49LL8T4"

    def test_validate_digipin_whitespace(self):
        """Test that validate_digipin handles whitespace."""
        # With whitespace should be invalid
        with pytest.raises(ValueError):
            utils.validate_digipin("39J49LL8T4 ")

        with pytest.raises(ValueError):
            utils.validate_digipin(" 39J49LL8T4")

    def test_is_valid_digipin_lengths(self):
        """Test is_valid_digipin with all valid lengths."""
        base = "39J49LL8T4"

        for length in range(1, 11):
            code = base[:length]
            assert utils.is_valid_digipin(code) is True

    def test_is_valid_digipin_invalid_chars(self):
        """Test is_valid_digipin rejects invalid characters."""
        # Contains '0' (ambiguous)
        assert utils.is_valid_digipin("39J049LL8T") is False

        # Contains '1' (ambiguous)
        assert utils.is_valid_digipin("39J149LL8T") is False

        # Contains 'O' (ambiguous)
        assert utils.is_valid_digipin("39JO9LL8T4") is False

        # Contains 'I' (ambiguous)
        assert utils.is_valid_digipin("39JI9LL8T4") is False

    def test_get_precision_info_all_levels(self):
        """Test get_precision_info for all 10 levels."""
        for level in range(1, 11):
            info = utils.get_precision_info(level)

            assert info["level"] == level
            assert info["code_length"] == level
            assert info["grid_size_lat_deg"] > 0
            assert info["grid_size_lon_deg"] > 0
            assert info["approx_distance_m"] > 0
            assert info["total_cells"] > 0
            assert isinstance(info["description"], str)

    def test_get_grid_size_decreases_with_level(self):
        """Test that grid size decreases as level increases."""
        sizes = [utils.get_grid_size(i) for i in range(1, 11)]

        for i in range(len(sizes) - 1):
            lat_current, lon_current = sizes[i]
            lat_next, lon_next = sizes[i + 1]

            # Next level should be smaller
            assert lat_next < lat_current
            assert lon_next < lon_current

    def test_get_approx_distance_all_levels(self):
        """Test get_approx_distance for all levels."""
        for level in range(1, 11):
            distance = utils.get_approx_distance(level)

            assert distance > 0
            assert isinstance(distance, float)

        # Level 1 should be much larger than level 10
        assert utils.get_approx_distance(1) > utils.get_approx_distance(10) * 100

    def test_get_symbol_from_position_all_cells(self):
        """Test get_symbol_from_position for all 16 cells."""
        symbols = set()

        for row in range(4):
            for col in range(4):
                symbol = utils.get_symbol_from_position(row, col)
                symbols.add(symbol)
                assert symbol in utils.DIGIPIN_ALPHABET

        # Should have all 16 symbols
        assert len(symbols) == 16

    def test_get_position_from_symbol_all_symbols(self):
        """Test get_position_from_symbol for all alphabet symbols."""
        for symbol in utils.DIGIPIN_ALPHABET:
            row, col = utils.get_position_from_symbol(symbol)

            # Should be valid positions
            assert 0 <= row < 4
            assert 0 <= col < 4

            # Reverse lookup should work
            assert utils.get_symbol_from_position(row, col) == symbol

    def test_get_position_from_symbol_invalid(self):
        """Test get_position_from_symbol with invalid symbols."""
        with pytest.raises(ValueError):
            utils.get_position_from_symbol("X")

        with pytest.raises(ValueError):
            utils.get_position_from_symbol("0")

        with pytest.raises(ValueError):
            utils.get_position_from_symbol("1")

    def test_constants_are_correct_type(self):
        """Test that constants have correct types."""
        assert isinstance(utils.LAT_MIN, (int, float))
        assert isinstance(utils.LAT_MAX, (int, float))
        assert isinstance(utils.LON_MIN, (int, float))
        assert isinstance(utils.LON_MAX, (int, float))
        assert isinstance(utils.DIGIPIN_ALPHABET, str)
        assert isinstance(utils.DIGIPIN_LEVELS, int)
        assert isinstance(utils.GRID_SUBDIVISION, int)

    def test_span_calculations(self):
        """Test LAT_SPAN and LON_SPAN calculations."""
        assert utils.LAT_SPAN == utils.LAT_MAX - utils.LAT_MIN
        assert utils.LON_SPAN == utils.LON_MAX - utils.LON_MIN

        # Should be 36 degrees each
        assert utils.LAT_SPAN == 36.0
        assert utils.LON_SPAN == 36.0

    def test_spiral_grid_structure(self):
        """Test SPIRAL_GRID structure."""
        # Should be 4x4
        assert len(utils.SPIRAL_GRID) == 4
        for row in utils.SPIRAL_GRID:
            assert len(row) == 4

        # All symbols should be from alphabet
        all_symbols = set()
        for row in utils.SPIRAL_GRID:
            for symbol in row:
                all_symbols.add(symbol)
                assert symbol in utils.DIGIPIN_ALPHABET

        # Should have all 16 symbols
        assert len(all_symbols) == 16


class TestCoordinateValidation:
    """Test coordinate validation edge cases."""

    def test_is_valid_coordinate_special_values(self):
        """Test is_valid_coordinate with special float values."""
        # NaN should be invalid
        import math

        assert utils.is_valid_coordinate(math.nan, 77.0) is False
        assert utils.is_valid_coordinate(28.0, math.nan) is False

        # Infinity should be invalid
        assert utils.is_valid_coordinate(math.inf, 77.0) is False
        assert utils.is_valid_coordinate(28.0, math.inf) is False

    def test_is_valid_coordinate_type_conversion(self):
        """Test that integers are accepted for coordinates."""
        # Integer coordinates should work
        assert utils.is_valid_coordinate(28, 77) is True

    def test_validate_coordinate_with_integers(self):
        """Test validate_coordinate with integer inputs."""
        # Should not raise
        utils.validate_coordinate(28, 77)

        # Out of bounds integers should raise
        with pytest.raises(ValueError):
            utils.validate_coordinate(0, 0)


class TestCodeValidation:
    """Test DIGIPIN code validation edge cases."""

    def test_is_valid_digipin_special_cases(self):
        """Test is_valid_digipin with special cases."""
        # Empty string
        assert utils.is_valid_digipin("") is False

        # Too long
        assert utils.is_valid_digipin("39J49LL8T4X") is False

        # Numeric only (but no forbidden chars)
        assert utils.is_valid_digipin("2345678923") is True

        # Letters only
        assert utils.is_valid_digipin("CFJKLMPTCF") is True

    def test_validate_digipin_error_messages(self):
        """Test that validate_digipin provides helpful error messages."""
        # Too short
        with pytest.raises(ValueError):
            utils.validate_digipin("")

        # Too long
        with pytest.raises(ValueError):
            utils.validate_digipin("39J49LL8T4X")

        # Invalid characters
        with pytest.raises(ValueError):
            utils.validate_digipin("39J49LL8T0")  # Contains '0'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
