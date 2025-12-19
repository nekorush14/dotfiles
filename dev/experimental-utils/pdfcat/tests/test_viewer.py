"""Tests for interactive viewer logic."""

import pytest
from unittest.mock import Mock, MagicMock


class TestViewer:
    """Test cases for PDF viewer logic."""

    def test_viewer_initialization(self, sample_pdf):
        """Test initializing viewer with PDF file."""
        from pdfcat.viewer import PDFViewer

        viewer = PDFViewer(sample_pdf)
        assert viewer is not None
        assert viewer.current_page == 0
        assert viewer.zoom_level == 1.0

    def test_next_page(self, sample_pdf):
        """Test navigating to next page."""
        from pdfcat.viewer import PDFViewer

        viewer = PDFViewer(sample_pdf)
        initial_page = viewer.current_page

        viewer.next_page()
        assert viewer.current_page == initial_page + 1

    def test_next_page_at_end(self, sample_pdf):
        """Test next page at document end."""
        from pdfcat.viewer import PDFViewer

        viewer = PDFViewer(sample_pdf)

        # Go to last page
        viewer.current_page = viewer.total_pages - 1

        # Should not go beyond last page
        viewer.next_page()
        assert viewer.current_page == viewer.total_pages - 1

    def test_previous_page(self, sample_pdf):
        """Test navigating to previous page."""
        from pdfcat.viewer import PDFViewer

        viewer = PDFViewer(sample_pdf)
        viewer.current_page = 2

        viewer.previous_page()
        assert viewer.current_page == 1

    def test_previous_page_at_start(self, sample_pdf):
        """Test previous page at document start."""
        from pdfcat.viewer import PDFViewer

        viewer = PDFViewer(sample_pdf)
        viewer.current_page = 0

        # Should not go below 0
        viewer.previous_page()
        assert viewer.current_page == 0

    def test_zoom_in(self, sample_pdf):
        """Test zooming in."""
        from pdfcat.viewer import PDFViewer

        viewer = PDFViewer(sample_pdf)
        initial_zoom = viewer.zoom_level

        viewer.zoom_in()
        assert viewer.zoom_level > initial_zoom

    def test_zoom_out(self, sample_pdf):
        """Test zooming out."""
        from pdfcat.viewer import PDFViewer

        viewer = PDFViewer(sample_pdf)
        viewer.zoom_level = 2.0

        viewer.zoom_out()
        assert viewer.zoom_level < 2.0

    def test_zoom_out_minimum(self, sample_pdf):
        """Test zoom out has minimum limit."""
        from pdfcat.viewer import PDFViewer

        viewer = PDFViewer(sample_pdf)
        viewer.zoom_level = 0.5

        # Should not go below minimum
        viewer.zoom_out()
        viewer.zoom_out()
        viewer.zoom_out()
        assert viewer.zoom_level >= 0.25

    def test_get_current_page_info(self, sample_pdf):
        """Test getting current page information."""
        from pdfcat.viewer import PDFViewer

        viewer = PDFViewer(sample_pdf)
        viewer.current_page = 2

        info = viewer.get_page_info()
        assert isinstance(info, dict)
        assert info["current"] == 3  # 1-indexed for display
        assert info["total"] > 0
        assert info["zoom"] == viewer.zoom_level

    def test_display_current_page(self, sample_pdf):
        """Test displaying current page."""
        from pdfcat.viewer import PDFViewer

        viewer = PDFViewer(sample_pdf)

        # Should return display command string
        result = viewer.display_current_page()
        assert isinstance(result, str)

    def test_go_to_page(self, sample_pdf):
        """Test jumping to specific page."""
        from pdfcat.viewer import PDFViewer

        viewer = PDFViewer(sample_pdf)

        # 1-indexed page number (sample_pdf has 3 pages)
        viewer.go_to_page(2)
        assert viewer.current_page == 1  # 0-indexed internally

    def test_go_to_invalid_page(self, sample_pdf):
        """Test jumping to invalid page number."""
        from pdfcat.viewer import PDFViewer

        viewer = PDFViewer(sample_pdf)

        # Should raise ValueError
        with pytest.raises(ValueError):
            viewer.go_to_page(0)

        with pytest.raises(ValueError):
            viewer.go_to_page(9999)
