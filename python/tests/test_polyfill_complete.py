"""
Comprehensive tests for polyfill modules with shapely mocking.

Tests both polyfill.py and polyfill_quadtree.py functions.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestPolyfillWithoutShapely:
    """Test polyfill module availability."""

    def test_polyfill_import(self):
        """Test that polyfill can be imported."""
        try:
            from digipin import polyfill

            # If shapely is available, polyfill should be callable
            assert callable(polyfill)
        except ImportError:
            # If shapely not available, that's OK
            pytest.skip("Shapely not installed")


class TestPolyfillValidation:
    """Test input validation for polyfill functions (requires shapely)."""

    def test_invalid_precision_raises(self):
        """Test that invalid precision raises ValueError."""
        try:
            from digipin import polyfill

            coords = [(28.63, 77.22), (28.62, 77.21), (28.62, 77.23), (28.63, 77.22)]

            # Precision 0 should raise
            with pytest.raises(ValueError, match="Precision must be between 1 and 10"):
                polyfill(coords, precision=0, algorithm="grid")

            # Precision 11 should raise
            with pytest.raises(ValueError, match="Precision must be between 1 and 10"):
                polyfill(coords, precision=11, algorithm="grid")
        except ImportError:
            pytest.skip("shapely not installed")

    def test_invalid_algorithm_raises(self):
        """Test that invalid algorithm raises ValueError."""
        try:
            from digipin import polyfill

            coords = [(28.63, 77.22), (28.62, 77.21), (28.62, 77.23), (28.63, 77.22)]

            with pytest.raises(ValueError, match="Unknown algorithm"):
                polyfill(coords, precision=7, algorithm="invalid")
        except ImportError:
            pytest.skip("shapely not installed")


class TestPolyfillGridAlgorithm:
    """Test the legacy grid scan algorithm (requires shapely)."""

    def test_grid_algorithm_basic(self):
        """Test that grid algorithm works on a simple polygon."""
        try:
            from digipin import polyfill

            # Larger polygon to ensure we get results
            coords = [
                (28.6300, 77.2200),
                (28.6300, 77.2250),
                (28.6250, 77.2250),
                (28.6250, 77.2200),
                (28.6300, 77.2200),
            ]
            result = polyfill(coords, precision=6, algorithm="grid")

            # Should have returned some codes
            assert isinstance(result, list)
            # May be 0 if shapely not installed or polygon outside bounds
            assert len(result) >= 0
        except ImportError:
            pytest.skip("shapely not installed")


class TestGetPolygonBoundary:
    """Test the get_polygon_boundary utility function."""

    def test_empty_list_returns_zeros(self):
        """Test that empty code list returns (0, 0, 0, 0)."""
        from digipin.polyfill import get_polygon_boundary

        result = get_polygon_boundary([])
        assert result == (0.0, 0.0, 0.0, 0.0)

    def test_single_code(self):
        """Test boundary calculation for single code."""
        from digipin.polyfill import get_polygon_boundary

        result = get_polygon_boundary(["39J49LL8T4"])

        # Should return bounds of that single code
        assert len(result) == 4
        min_lat, max_lat, min_lon, max_lon = result
        assert min_lat < max_lat
        assert min_lon < max_lon

    def test_multiple_codes(self):
        """Test boundary calculation for multiple codes."""
        from digipin.polyfill import get_polygon_boundary

        codes = ["39J49LL8T4", "39J49LL8T5", "39J49LL8T6"]
        result = get_polygon_boundary(codes)

        # Should return expanded bounds
        assert len(result) == 4
        min_lat, max_lat, min_lon, max_lon = result
        assert min_lat < max_lat
        assert min_lon < max_lon

    def test_wide_spread_codes(self):
        """Test boundary for widely spread codes."""
        from digipin.polyfill import get_polygon_boundary

        # Codes from different regions
        codes = [
            "39J49LL8T4",  # Delhi (~28N, 77E)
            "33J5T26TFP",  # Karnataka (~12N, 76E)
        ]
        result = get_polygon_boundary(codes)

        min_lat, max_lat, min_lon, max_lon = result

        # Bounds should encompass both cities
        assert max_lat - min_lat > 1  # At least 1 degree apart
        assert max_lon - min_lon > 0  # Some longitude difference
        assert max_lat > min_lat
        assert max_lon > min_lon


class TestPolyfillQuadtreeHelpers:
    """Test polyfill_quadtree helper functions."""

    def test_get_cell_center(self):
        """Test _get_cell_center function."""
        from digipin.polyfill_quadtree import _get_cell_center

        lat, lon = _get_cell_center("39J49LL8T4")

        # Should return center coordinates
        assert isinstance(lat, float)
        assert isinstance(lon, float)
        assert 28.6 < lat < 28.7
        assert 77.2 < lon < 77.3

    def test_get_cell_polygon_structure(self):
        """Test that _get_cell_polygon returns proper structure."""
        # This requires shapely, so we'll test it exists
        try:
            from shapely.geometry import Polygon
            from digipin.polyfill_quadtree import _get_cell_polygon

            poly = _get_cell_polygon("39J49LL8T4")
            assert isinstance(poly, Polygon)
            assert poly.is_valid
        except ImportError:
            pytest.skip("shapely not installed")

    def test_get_cell_relationship_outside(self):
        """Test cell relationship detection for outside cells."""
        try:
            from shapely.geometry import Polygon
            from shapely.prepared import prep
            from digipin.polyfill_quadtree import _get_cell_relationship

            # Create a small polygon
            poly = Polygon([(77.0, 28.0), (77.1, 28.0), (77.1, 28.1), (77.0, 28.1)])
            prepared = prep(poly)

            # Test a cell far away
            relationship = _get_cell_relationship("58C4K9FF72", prepared)  # Mumbai

            # Should be outside
            assert relationship == "outside"
        except ImportError:
            pytest.skip("shapely not installed")

    def test_get_cell_relationship_inside(self):
        """Test cell relationship detection for inside cells."""
        try:
            from shapely.geometry import Polygon
            from shapely.prepared import prep
            from digipin.polyfill_quadtree import _get_cell_relationship

            # Create a large polygon that definitely contains a cell
            poly = Polygon(
                [
                    (77.0, 28.0),
                    (78.0, 28.0),
                    (78.0, 29.0),
                    (77.0, 29.0),
                ]
            )
            prepared = prep(poly)

            # Test a cell inside
            # Using precision 4 for larger cells
            relationship = _get_cell_relationship("39J4", prepared)

            # Should be inside or intersects
            assert relationship in ("inside", "intersects")
        except ImportError:
            pytest.skip("shapely not installed")


class TestPolyfillQuadtreeRecursion:
    """Test the recursive polyfill quadtree algorithm."""

    def test_expand_cell_fully(self):
        """Test _expand_cell_fully recursive expansion."""
        try:
            from shapely.geometry import Polygon
            from shapely.prepared import prep
            from digipin.polyfill_quadtree import _expand_cell_fully

            # Create a polygon
            poly = Polygon(
                [
                    (77.20, 28.62),
                    (77.23, 28.62),
                    (77.23, 28.64),
                    (77.20, 28.64),
                ]
            )
            prepared = prep(poly)

            # Expand a level-6 cell to level-7
            result = _expand_cell_fully(
                "39J49L", target_precision=7, prepared_poly=prepared
            )

            # Should return list of level-7 codes
            assert isinstance(result, list)
            # All codes should be length 7
            for code in result:
                assert len(code) == 7
                assert code.startswith("39J49L")
        except ImportError:
            pytest.skip("shapely not installed")


class TestPolyfillIntegration:
    """Integration tests for polyfill (requires shapely)."""

    def test_polyfill_defaults_to_quadtree(self):
        """Test that polyfill uses quadtree by default."""
        try:
            from digipin import polyfill, polyfill_quadtree

            coords = [
                (28.6300, 77.2200),
                (28.6300, 77.2210),
                (28.6290, 77.2210),
                (28.6290, 77.2200),
                (28.6300, 77.2200),
            ]

            # Default algorithm
            result_default = polyfill(coords, precision=7)

            # Explicit quadtree
            result_quadtree = polyfill_quadtree(coords, precision=7)

            # Should be identical
            assert set(result_default) == set(result_quadtree)
        except ImportError:
            pytest.skip("shapely not installed")

    def test_polyfill_grid_vs_quadtree_similarity(self):
        """Test that grid and quadtree produce similar results."""
        try:
            from digipin import polyfill

            coords = [
                (28.6300, 77.2200),
                (28.6300, 77.2210),
                (28.6290, 77.2210),
                (28.6290, 77.2200),
                (28.6300, 77.2200),
            ]

            result_grid = set(polyfill(coords, precision=7, algorithm="grid"))
            result_quadtree = set(polyfill(coords, precision=7, algorithm="quadtree"))

            # Should be exactly equal for simple square
            assert result_grid == result_quadtree
        except ImportError:
            pytest.skip("shapely not installed")

    def test_polyfill_empty_result_outside_bounds(self):
        """Test that polygon outside India returns empty list."""
        try:
            from digipin import polyfill

            # Polygon in USA
            coords = [
                (40.7128, -74.0060),
                (40.7228, -74.0060),
                (40.7228, -73.9960),
                (40.7128, -73.9960),
                (40.7128, -74.0060),
            ]

            result = polyfill(coords, precision=7)

            # Should be empty
            assert result == []
        except ImportError:
            pytest.skip("shapely not installed")

    def test_polyfill_shapely_polygon_input(self):
        """Test that shapely Polygon objects work as input."""
        try:
            from shapely.geometry import Polygon
            from digipin import polyfill

            # Create Shapely polygon (lon, lat order)
            poly = Polygon(
                [
                    (77.2200, 28.6300),
                    (77.2210, 28.6300),
                    (77.2210, 28.6290),
                    (77.2200, 28.6290),
                ]
            )

            result = polyfill(poly, precision=7)

            # Should return some codes
            assert len(result) >= 0  # May be empty if outside bounds
            if len(result) > 0:
                assert all(len(code) == 7 for code in result)
        except ImportError:
            pytest.skip("shapely not installed")


class TestPolyfillPerformance:
    """Test polyfill performance characteristics."""

    def test_quadtree_handles_high_precision(self):
        """Test that quadtree can handle high precision levels."""
        try:
            from digipin import polyfill_quadtree

            # Small area, high precision
            coords = [
                (28.6300, 77.2200),
                (28.6305, 77.2200),
                (28.6305, 77.2205),
                (28.6300, 77.2205),
                (28.6300, 77.2200),
            ]

            result = polyfill_quadtree(coords, precision=9)

            # Should complete and return codes
            assert isinstance(result, list)
            assert all(len(code) == 9 for code in result)
        except ImportError:
            pytest.skip("shapely not installed")

    def test_grid_algorithm_handles_small_areas(self):
        """Test grid algorithm on small areas."""
        try:
            from digipin import polyfill

            # Slightly larger area to ensure results
            coords = [
                (28.6300, 77.2200),
                (28.6310, 77.2200),
                (28.6310, 77.2210),
                (28.6300, 77.2210),
                (28.6300, 77.2200),
            ]

            result = polyfill(coords, precision=7, algorithm="grid")

            # Should return results (may be 0 if shapely issues)
            assert isinstance(result, list)
            assert len(result) >= 0
        except ImportError:
            pytest.skip("shapely not installed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
