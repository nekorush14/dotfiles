"""Tests for webcat.renderer module."""

import pytest
from PIL import Image

from webcat.renderer import TerminalRenderer
from webcat.parser import ParsedPage, Link, ImageInfo


class TestTerminalRenderer:
    """Tests for TerminalRenderer class."""

    def test_renderer_initialization(self):
        """Test TerminalRenderer initialization with defaults."""
        renderer = TerminalRenderer()
        assert renderer.width is None  # Auto-detect
        assert renderer.show_images is True
        assert renderer.image_max_width is None
        assert renderer.image_max_height is None

    def test_renderer_initialization_custom(self):
        """Test TerminalRenderer with custom settings."""
        renderer = TerminalRenderer(
            width=100,
            show_images=False,
            image_max_width=800,
            image_max_height=600,
        )
        assert renderer.width == 100
        assert renderer.show_images is False
        assert renderer.image_max_width == 800
        assert renderer.image_max_height == 600

    def test_render_page_simple(self):
        """Test rendering a simple page."""
        renderer = TerminalRenderer(width=80)
        page = ParsedPage(
            title="Test Page",
            text="Hello World\nThis is a test.",
        )
        output = renderer.render_page(page)

        assert "Test Page" in output
        assert "Hello World" in output
        assert "This is a test" in output

    def test_render_page_with_links(self):
        """Test rendering a page with links."""
        renderer = TerminalRenderer(width=80)
        page = ParsedPage(
            title="Page",
            text="Click [1] here.",
            links=[
                Link("here", "https://example.com", 0, 1),
            ],
        )
        output = renderer.render_page(page)

        # Should include link reference section
        assert "https://example.com" in output or "[1]" in output

    def test_render_text_segment(self):
        """Test rendering a portion of text."""
        renderer = TerminalRenderer(width=80)
        lines = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]

        output = renderer.render_text_segment(lines, 1, 3)

        assert "Line 2" in output
        assert "Line 3" in output
        assert "Line 1" not in output
        assert "Line 4" not in output

    def test_render_text_segment_bounds(self):
        """Test render_text_segment with out-of-bounds indices."""
        renderer = TerminalRenderer(width=80)
        lines = ["Line 1", "Line 2"]

        # Should handle gracefully
        output = renderer.render_text_segment(lines, 0, 10)
        assert "Line 1" in output
        assert "Line 2" in output

    def test_render_image(self, test_image_bytes: bytes):
        """Test rendering an image."""
        renderer = TerminalRenderer(show_images=True)
        output = renderer.render_image(test_image_bytes)

        # Should produce Kitty protocol escape sequence
        assert "\x1b_G" in output
        assert "\x1b\\" in output

    def test_render_image_disabled(self, test_image_bytes: bytes):
        """Test render_image when images are disabled."""
        renderer = TerminalRenderer(show_images=False)
        output = renderer.render_image(test_image_bytes)

        # Should return empty or placeholder
        assert "\x1b_G" not in output

    def test_render_image_with_size_constraints(self, test_image_bytes: bytes):
        """Test rendering an image with size constraints."""
        renderer = TerminalRenderer(
            show_images=True,
            image_max_width=50,
            image_max_height=50,
        )
        output = renderer.render_image(test_image_bytes)

        # Should still produce Kitty protocol output
        assert "\x1b_G" in output

    def test_render_link_highlight_normal(self):
        """Test link highlight formatting."""
        renderer = TerminalRenderer()
        output = renderer.render_link_highlight(1, selected=False)

        # Should contain ANSI escape codes for styling
        assert "\x1b[" in output or "[1]" in output

    def test_render_link_highlight_selected(self):
        """Test selected link highlight."""
        renderer = TerminalRenderer()
        output = renderer.render_link_highlight(1, selected=True)

        # Selected should have different styling
        assert "\x1b[" in output

    def test_clear(self):
        """Test clear command."""
        renderer = TerminalRenderer()
        output = renderer.clear()

        # Should contain clear screen escape sequence
        assert "\x1b[2J" in output or "\x1b_G" in output

    def test_render_title(self):
        """Test title rendering with proper formatting."""
        renderer = TerminalRenderer(width=80)
        output = renderer._render_title("Test Title")

        assert "Test Title" in output
        # Should have some visual separation
        assert "=" in output or "-" in output or "─" in output

    def test_render_links_section(self):
        """Test rendering links reference section."""
        renderer = TerminalRenderer(width=80)
        links = [
            Link("Example", "https://example.com", 0, 1),
            Link("Test", "https://test.com", 0, 2),
        ]
        output = renderer._render_links_section(links)

        assert "[1]" in output
        assert "[2]" in output
        assert "https://example.com" in output
        assert "https://test.com" in output

    def test_render_links_section_empty(self):
        """Test rendering empty links section."""
        renderer = TerminalRenderer()
        output = renderer._render_links_section([])

        assert output == ""
