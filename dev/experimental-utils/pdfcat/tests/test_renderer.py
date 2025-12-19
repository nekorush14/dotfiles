"""Tests for PDF rendering functionality."""

import pytest
from pathlib import Path
from PIL import Image


class TestPDFRenderer:
    """Test cases for PDF to image rendering."""

    def test_renderer_initialization(self, sample_pdf):
        """Test initializing PDFRenderer with a valid PDF file."""
        from pdfcat.renderer import PDFRenderer

        renderer = PDFRenderer(sample_pdf)
        assert renderer is not None
        assert renderer.pdf_path == sample_pdf

    def test_get_page_count(self, sample_pdf):
        """Test getting total page count from PDF."""
        from pdfcat.renderer import PDFRenderer

        renderer = PDFRenderer(sample_pdf)
        page_count = renderer.get_page_count()
        assert isinstance(page_count, int)
        assert page_count == 3  # Our test PDF has 3 pages

    def test_render_page(self, sample_pdf):
        """Test rendering a specific page to image."""
        from pdfcat.renderer import PDFRenderer

        renderer = PDFRenderer(sample_pdf)

        # Render first page (0-indexed)
        img = renderer.render_page(0)
        assert isinstance(img, Image.Image)
        assert img.width > 0
        assert img.height > 0

    def test_render_page_with_zoom(self, sample_pdf):
        """Test rendering a page with zoom factor."""
        from pdfcat.renderer import PDFRenderer

        renderer = PDFRenderer(sample_pdf)

        # Render with 2x zoom
        img_normal = renderer.render_page(0, zoom=1.0)
        img_zoomed = renderer.render_page(0, zoom=2.0)

        assert img_zoomed.width == img_normal.width * 2
        assert img_zoomed.height == img_normal.height * 2

    def test_render_invalid_page(self, sample_pdf):
        """Test rendering an invalid page number."""
        from pdfcat.renderer import PDFRenderer

        renderer = PDFRenderer(sample_pdf)

        # Should raise IndexError or ValueError
        with pytest.raises((IndexError, ValueError)):
            renderer.render_page(-1)

        with pytest.raises((IndexError, ValueError)):
            renderer.render_page(9999)

    def test_renderer_with_nonexistent_file(self):
        """Test initializing renderer with nonexistent file."""
        from pdfcat.renderer import PDFRenderer

        # Should raise FileNotFoundError
        with pytest.raises(FileNotFoundError):
            renderer = PDFRenderer("nonexistent.pdf")
            renderer.get_page_count()

    def test_render_page_with_max_width(self, sample_pdf):
        """Test rendering a page with maximum width constraint."""
        from pdfcat.renderer import PDFRenderer

        renderer = PDFRenderer(sample_pdf)

        # Render with max width
        img = renderer.render_page(0, max_width=800)
        assert img.width <= 800

    def test_close_renderer(self, sample_pdf):
        """Test properly closing the PDF renderer."""
        from pdfcat.renderer import PDFRenderer

        renderer = PDFRenderer(sample_pdf)
        renderer.close()

        # After closing, operations should fail
        with pytest.raises(Exception):
            renderer.render_page(0)
