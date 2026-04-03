"""
Tests for __init__.py backend selection and metadata.

Tests the automatic Cython vs Python fallback mechanism and
ensures all exports are properly exposed.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import digipin


class TestBackendInfo:
    """Test backend information and selection logic."""

    def test_get_backend_info_structure(self):
        """Test that get_backend_info returns correct structure."""
        info = digipin.get_backend_info()

        # Should have all required keys
        assert "backend" in info
        assert "performance" in info
        assert "description" in info

        # Backend should be either 'cython' or 'python'
        assert info["backend"] in ("cython", "python")

        # Should have valid descriptions
        assert isinstance(info["performance"], str)
        assert isinstance(info["description"], str)

    def test_backend_consistency(self):
        """Test that backend type matches performance multiplier."""
        info = digipin.get_backend_info()

        if info["backend"] == "cython":
            assert "10-15x" in info["performance"]
            assert "Cython" in info["description"]
        elif info["backend"] == "python":
            assert "1x" in info["performance"]
            assert "Pure Python" in info["description"]


class TestPackageMetadata:
    """Test package-level metadata and constants."""

    def test_version_exists(self):
        """Test that __version__ is defined."""
        assert hasattr(digipin, "__version__")
        assert isinstance(digipin.__version__, str)
        # Should be semantic versioning format
        version_parts = digipin.__version__.split(".")
        assert len(version_parts) >= 2  # At least major.minor

    def test_author_exists(self):
        """Test that __author__ is defined."""
        assert hasattr(digipin, "__author__")
        assert isinstance(digipin.__author__, str)
        assert len(digipin.__author__) > 0

    def test_license_exists(self):
        """Test that __license__ is defined."""
        assert hasattr(digipin, "__license__")
        assert digipin.__license__ == "MIT"


class TestCoreAPIExports:
    """Test that all core API functions are properly exported."""

    def test_core_functions_exported(self):
        """Test that core encode/decode functions are accessible."""
        # Core functions
        assert hasattr(digipin, "encode")
        assert hasattr(digipin, "decode")
        assert hasattr(digipin, "is_valid")

        # All should be callable
        assert callable(digipin.encode)
        assert callable(digipin.decode)
        assert callable(digipin.is_valid)

    def test_batch_operations_exported(self):
        """Test that batch operations are accessible."""
        assert hasattr(digipin, "batch_encode")
        assert hasattr(digipin, "batch_decode")

        assert callable(digipin.batch_encode)
        assert callable(digipin.batch_decode)

    def test_hierarchical_operations_exported(self):
        """Test that hierarchical functions are accessible."""
        assert hasattr(digipin, "get_bounds")
        assert hasattr(digipin, "encode_with_bounds")
        assert hasattr(digipin, "decode_with_bounds")
        assert hasattr(digipin, "get_parent")
        assert hasattr(digipin, "is_within")

        assert callable(digipin.get_bounds)
        assert callable(digipin.encode_with_bounds)
        assert callable(digipin.decode_with_bounds)
        assert callable(digipin.get_parent)
        assert callable(digipin.is_within)

    def test_neighbor_functions_exported(self):
        """Test that neighbor discovery functions are accessible."""
        assert hasattr(digipin, "get_neighbors")
        assert hasattr(digipin, "get_ring")
        assert hasattr(digipin, "get_disk")
        assert hasattr(digipin, "get_surrounding_cells")
        assert hasattr(digipin, "expand_search_area")

        assert callable(digipin.get_neighbors)
        assert callable(digipin.get_ring)
        assert callable(digipin.get_disk)
        assert callable(digipin.get_surrounding_cells)
        assert callable(digipin.expand_search_area)

    def test_utility_functions_exported(self):
        """Test that utility functions are accessible."""
        assert hasattr(digipin, "is_valid_coordinate")
        assert hasattr(digipin, "get_precision_info")
        assert hasattr(digipin, "get_grid_size")
        assert hasattr(digipin, "get_approx_distance")

        assert callable(digipin.is_valid_coordinate)
        assert callable(digipin.get_precision_info)
        assert callable(digipin.get_grid_size)
        assert callable(digipin.get_approx_distance)

    def test_constants_exported(self):
        """Test that constants are accessible."""
        assert hasattr(digipin, "LAT_MIN")
        assert hasattr(digipin, "LAT_MAX")
        assert hasattr(digipin, "LON_MIN")
        assert hasattr(digipin, "LON_MAX")
        assert hasattr(digipin, "DIGIPIN_ALPHABET")
        assert hasattr(digipin, "DIGIPIN_LEVELS")

        # Verify values
        assert digipin.LAT_MIN == 2.5
        assert digipin.LAT_MAX == 38.5
        assert digipin.LON_MIN == 63.5
        assert digipin.LON_MAX == 99.5
        assert len(digipin.DIGIPIN_ALPHABET) == 16
        assert digipin.DIGIPIN_LEVELS == 10


class TestOptionalFeatures:
    """Test optional feature availability (geo, viz)."""

    def test_polyfill_functions(self):
        """Test polyfill functions (may be None if shapely not installed)."""
        # Should have attributes even if None
        assert hasattr(digipin, "polyfill")
        assert hasattr(digipin, "polyfill_quadtree")
        assert hasattr(digipin, "get_polygon_boundary")

        # If shapely is installed, they should be callable
        if digipin.polyfill is not None:
            assert callable(digipin.polyfill)
            assert callable(digipin.polyfill_quadtree)
            assert callable(digipin.get_polygon_boundary)

    def test_viz_functions(self):
        """Test visualization functions (may be None if folium not installed)."""
        # Should have attributes even if None
        assert hasattr(digipin, "plot_pins")
        assert hasattr(digipin, "plot_coverage")
        assert hasattr(digipin, "plot_neighbors")

        # If folium is installed, they should be callable
        if digipin.plot_pins is not None:
            assert callable(digipin.plot_pins)
            assert callable(digipin.plot_coverage)
            assert callable(digipin.plot_neighbors)


class TestImportIntegrity:
    """Test that imports don't have circular dependencies or errors."""

    def test_reimport_works(self):
        """Test that module can be imported multiple times."""
        import importlib

        # Should be able to reload without errors
        importlib.reload(digipin)

        # Core functions should still work after reload
        assert digipin.encode(28.622788, 77.213033) == "39J49LL8T4"

    def test_all_list_matches_exports(self):
        """Test that __all__ list includes all public exports."""
        # Get __all__ if it exists
        if hasattr(digipin, "__all__"):
            all_items = digipin.__all__

            # All items in __all__ should be accessible
            for item in all_items:
                assert hasattr(digipin, item), f"{item} in __all__ but not exported"

            # Core functions should be in __all__
            core_functions = [
                "encode",
                "decode",
                "is_valid",
                "batch_encode",
                "batch_decode",
                "get_neighbors",
                "get_ring",
                "get_disk",
            ]
            for func in core_functions:
                assert func in all_items, f"{func} should be in __all__"


class TestBackendFunctionality:
    """Test that backend functions work correctly."""

    def test_encode_works_regardless_of_backend(self):
        """Test encoding works with both backends."""
        result = digipin.encode(28.622788, 77.213033)
        assert result == "39J49LL8T4"

    def test_decode_works_regardless_of_backend(self):
        """Test decoding works with both backends."""
        lat, lon = digipin.decode("39J49LL8T4")
        assert 28.622 < lat < 28.623
        assert 77.212 < lon < 77.214

    def test_batch_encode_works(self):
        """Test batch encoding works with both backends."""
        coords = [(28.622788, 77.213033), (12.9716, 77.5946)]
        codes = digipin.batch_encode(coords)

        assert len(codes) == 2
        assert codes[0] == "39J49LL8T4"

    def test_batch_decode_works(self):
        """Test batch decoding works with both backends."""
        codes = ["39J49LL8T4", "33J5T26TFP"]
        coords = digipin.batch_decode(codes)

        assert len(coords) == 2
        assert isinstance(coords[0], tuple)
        assert len(coords[0]) == 2

    def test_get_bounds_works(self):
        """Test get_bounds works with both backends."""
        bounds = digipin.get_bounds("39J49LL8T4")

        assert len(bounds) == 4
        min_lat, max_lat, min_lon, max_lon = bounds
        assert min_lat < max_lat
        assert min_lon < max_lon


class TestDocumentation:
    """Test that docstrings are present and helpful."""

    def test_module_has_docstring(self):
        """Test that the module has a comprehensive docstring."""
        assert digipin.__doc__ is not None
        assert len(digipin.__doc__) > 100

        # Should mention DIGIPIN and India
        doc_lower = digipin.__doc__.lower()
        assert "digipin" in doc_lower
        assert "india" in doc_lower

    def test_core_functions_have_docstrings(self):
        """Test that core functions have docstrings."""
        functions = [
            digipin.encode,
            digipin.decode,
            digipin.is_valid,
            digipin.get_neighbors,
            digipin.get_backend_info,
        ]

        for func in functions:
            assert func.__doc__ is not None
            assert len(func.__doc__) > 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
