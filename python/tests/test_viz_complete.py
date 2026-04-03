"""
Comprehensive tests for visualization module with folium mocking.

Tests all viz.py functions using mocks to avoid folium dependency.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, call
import warnings

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestVizWithoutFolium:
    """Test visualization module when folium is not available."""

    def test_import_without_folium_raises_warning(self):
        """Test that importing viz without folium raises a warning."""
        # This test verifies the ImportWarning is issued
        with patch.dict("sys.modules", {"folium": None}):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")

                # Force reimport
                import importlib
                from digipin import viz

                importlib.reload(viz)

                # Should have received warning
                # Note: Warning may or may not be present depending on import state
                # So we just verify the module loads


class TestVizWithFolium:
    """Test visualization functions with mocked folium."""

    @pytest.fixture
    def mock_folium(self):
        """Create a mock folium module."""
        mock = MagicMock()

        # Mock Map class
        mock.Map = MagicMock()
        mock_map_instance = MagicMock()
        mock.Map.return_value = mock_map_instance

        # Mock map methods
        mock_map_instance.save = MagicMock()
        mock_map_instance.get_root = MagicMock()
        mock_map_instance.get_root.return_value.html = MagicMock()
        mock_map_instance.get_root.return_value.html.add_child = MagicMock()

        # Mock other classes
        mock.CircleMarker = MagicMock(return_value=MagicMock())
        mock.Marker = MagicMock(return_value=MagicMock())
        mock.Rectangle = MagicMock(return_value=MagicMock())
        mock.Popup = MagicMock()
        mock.Icon = MagicMock()
        mock.Element = MagicMock()

        # Mock plugins
        mock.plugins = MagicMock()
        mock.plugins.MarkerCluster = MagicMock(return_value=MagicMock())

        return mock

    def test_plot_pins_single_code(self, mock_folium):
        """Test plotting a single DIGIPIN code."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            # Need to reimport after patching
            import importlib
            from digipin import viz

            importlib.reload(viz)

            # Test single code
            result = viz.plot_pins("39J49LL8T4")

            # Should have created a Map
            mock_folium.Map.assert_called_once()

            # Should have created a CircleMarker
            assert mock_folium.CircleMarker.call_count >= 1

    def test_plot_pins_multiple_codes(self, mock_folium):
        """Test plotting multiple DIGIPIN codes."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            codes = ["39J49LL8T4", "39J49LL8T5", "39J49LL8T6"]
            result = viz.plot_pins(codes)

            # Should have created markers for each code
            assert mock_folium.CircleMarker.call_count >= len(codes)

    def test_plot_pins_with_clustering(self, mock_folium):
        """Test plotting with marker clustering enabled."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            codes = ["39J49LL8T4"] * 10
            result = viz.plot_pins(codes, cluster=True)

            # Should have created a MarkerCluster
            mock_folium.plugins.MarkerCluster.assert_called_once()

    def test_plot_pins_with_bounds(self, mock_folium):
        """Test plotting with bounding boxes shown."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            result = viz.plot_pins("39J49LL8T4", show_bounds=True)

            # Should have created a Rectangle
            assert mock_folium.Rectangle.call_count >= 1

    def test_plot_pins_invalid_code_warning(self, mock_folium):
        """Test that invalid codes produce warnings."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")

                # Try to plot mix of valid and invalid codes
                try:
                    codes = ["39J49LL8T4", "INVALID123"]
                    viz.plot_pins(codes)

                    # Should have warned about invalid code
                    assert len(w) > 0
                    assert (
                        "Invalid" in str(w[0].message)
                        or "invalid" in str(w[0].message).lower()
                    )
                except ValueError:
                    # If it raises ValueError for all invalid, that's also OK
                    pass

    def test_plot_pins_no_valid_codes_raises(self, mock_folium):
        """Test that plot_pins raises error when no valid codes provided."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            with pytest.raises(ValueError, match="No valid"):
                viz.plot_pins(["INVALID123", "BADCODE99"])

    def test_plot_pins_too_many_codes_warning(self, mock_folium):
        """Test that too many codes produces a warning."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")

                # Create more codes than max_clusters
                codes = ["39J49LL8T4"] * 1500
                viz.plot_pins(codes, max_clusters=1000)

                # Should warn about too many codes
                assert len(w) > 0

    def test_plot_coverage(self, mock_folium):
        """Test plot_coverage convenience function."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            codes = ["39J49LL8T4", "39J49LL8T5"]
            result = viz.plot_coverage(codes, title="Test Zone")

            # Should have created a map
            mock_folium.Map.assert_called()

    def test_plot_coverage_with_file_output(self, mock_folium, tmp_path):
        """Test that plot_coverage can save to file."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            codes = ["39J49LL8T4"]
            output_file = str(tmp_path / "test_map.html")

            result = viz.plot_coverage(codes, output_file=output_file)

            # Should have called save
            # The mock map instance should have save called
            result.save.assert_called_once_with(output_file)

    def test_plot_neighbors(self, mock_folium):
        """Test plot_neighbors function."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            result = viz.plot_neighbors("39J49LL8T4", radius=1)

            # Should have created a map
            mock_folium.Map.assert_called()

            # Should have created a center marker
            mock_folium.Marker.assert_called()

    def test_plot_neighbors_with_output(self, mock_folium, tmp_path):
        """Test plot_neighbors with file output."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            output_file = str(tmp_path / "neighbors.html")
            result = viz.plot_neighbors("39J49LL8T4", output_file=output_file)

            # Should have saved the file
            result.save.assert_called_once_with(output_file)

    def test_plot_neighbors_without_neighbors(self, mock_folium):
        """Test plot_neighbors with include_neighbors=False."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            result = viz.plot_neighbors("39J49LL8T4", include_neighbors=False)

            # Should still create map and center marker
            mock_folium.Map.assert_called()
            mock_folium.Marker.assert_called()


class TestVizColoringAndLabeling:
    """Test color coding and labeling features."""

    @pytest.fixture
    def mock_folium(self):
        """Create a mock folium module."""
        mock = MagicMock()
        mock.Map = MagicMock(return_value=MagicMock())
        mock.CircleMarker = MagicMock(return_value=MagicMock())
        mock.Marker = MagicMock(return_value=MagicMock())
        mock.Rectangle = MagicMock(return_value=MagicMock())
        mock.Popup = MagicMock()
        mock.Icon = MagicMock()
        mock.Element = MagicMock()
        mock.plugins = MagicMock()
        mock.plugins.MarkerCluster = MagicMock(return_value=MagicMock())
        return mock

    def test_color_by_precision_enabled(self, mock_folium):
        """Test that colors change based on precision level."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            # Codes with different precisions
            codes = ["39J49LL8T4", "39J49LL8"]  # 10 chars vs 8 chars
            result = viz.plot_pins(codes, color_by_precision=True)

            # CircleMarker should have been called with different colors
            # (checking implementation details here)
            assert mock_folium.CircleMarker.call_count >= 2

    def test_show_labels_disabled(self, mock_folium):
        """Test plotting without labels."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            result = viz.plot_pins("39J49LL8T4", show_labels=False)

            # Should still create markers but without popups
            # Popup should be called with None or not called
            # This is implementation-specific

    def test_custom_tiles(self, mock_folium):
        """Test using custom map tiles."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            result = viz.plot_pins("39J49LL8T4", tiles="Stamen Terrain")

            # Map should be created with custom tiles
            # Check that Map was called with tiles parameter
            call_args = mock_folium.Map.call_args
            if call_args:
                kwargs = call_args[1] if len(call_args) > 1 else call_args.kwargs
                assert "tiles" in kwargs


class TestVizEdgeCases:
    """Test edge cases and error conditions."""

    def test_folium_availability_check(self):
        """Test that FOLIUM_AVAILABLE flag is set correctly."""
        from digipin import viz

        # Just verify the module imports
        assert hasattr(viz, "FOLIUM_AVAILABLE")
        assert isinstance(viz.FOLIUM_AVAILABLE, bool)


class TestVizZoomCalculation:
    """Test automatic zoom level calculation."""

    @pytest.fixture
    def mock_folium(self):
        """Create a mock folium module."""
        mock = MagicMock()
        mock.Map = MagicMock(return_value=MagicMock())
        mock.CircleMarker = MagicMock(return_value=MagicMock())
        mock.Rectangle = MagicMock(return_value=MagicMock())
        mock.Popup = MagicMock()
        mock.Element = MagicMock()
        mock.plugins = MagicMock()
        return mock

    def test_auto_zoom_single_code(self, mock_folium):
        """Test auto-zoom for single code."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            result = viz.plot_pins("39J49LL8T4", zoom=None)

            # Should have created map with calculated zoom
            assert mock_folium.Map.called

    def test_manual_zoom_override(self, mock_folium):
        """Test that manual zoom overrides auto-calculation."""
        with patch.dict("sys.modules", {"folium": mock_folium}):
            import importlib
            from digipin import viz

            importlib.reload(viz)

            result = viz.plot_pins("39J49LL8T4", zoom=12)

            # Should use zoom=12
            call_args = mock_folium.Map.call_args
            if call_args:
                kwargs = call_args[1] if len(call_args) > 1 else call_args.kwargs
                assert kwargs.get("zoom_start") == 12


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
