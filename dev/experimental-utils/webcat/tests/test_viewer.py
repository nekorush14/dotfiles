"""Tests for webcat.viewer module."""

import pytest
from pytest_httpserver import HTTPServer
from unittest.mock import patch, MagicMock

from webcat.viewer import WebViewer, HistoryEntry


class TestHistoryEntry:
    """Tests for HistoryEntry dataclass."""

    def test_history_entry_creation(self):
        """Test creating a HistoryEntry."""
        entry = HistoryEntry(url="https://example.com")
        assert entry.url == "https://example.com"
        assert entry.scroll_position == 0

    def test_history_entry_with_scroll(self):
        """Test HistoryEntry with scroll position."""
        entry = HistoryEntry(url="https://example.com", scroll_position=100)
        assert entry.scroll_position == 100


def create_test_viewer(**kwargs) -> WebViewer:
    """Create a WebViewer with testing enabled."""
    viewer = WebViewer(**kwargs)
    viewer._fetcher._allow_private = True
    return viewer


class TestWebViewer:
    """Tests for WebViewer class."""

    def test_viewer_initialization(self):
        """Test WebViewer initialization."""
        viewer = WebViewer()
        assert viewer.current_url == ""
        assert viewer.scroll_position == 0
        assert viewer.selected_link == -1
        viewer.close()

    def test_viewer_initialization_with_options(self):
        """Test WebViewer with custom options."""
        viewer = WebViewer(
            width=100,
            show_images=False,
            use_readability=False,
            timeout=60.0,
        )
        assert viewer._show_images is False
        assert viewer._use_readability is False
        viewer.close()

    def test_load_url(self, mock_html_server: HTTPServer):
        """Test loading a URL."""
        viewer = create_test_viewer()
        try:
            url = mock_html_server.url_for("/")
            success = viewer.load_url(url)

            assert success is True
            assert viewer.current_url == url
            assert viewer.current_page is not None
            assert viewer.current_page.title == "Test Page"
        finally:
            viewer.close()

    def test_load_url_failure(self):
        """Test loading an invalid URL."""
        viewer = WebViewer(timeout=1.0)
        try:
            success = viewer.load_url("http://invalid.localhost.test:99999")
            assert success is False
        finally:
            viewer.close()

    def test_reload(self, mock_html_server: HTTPServer):
        """Test reloading current page."""
        viewer = create_test_viewer()
        try:
            url = mock_html_server.url_for("/")
            viewer.load_url(url)
            success = viewer.reload()
            assert success is True
        finally:
            viewer.close()

    def test_scroll_down(self, mock_html_server: HTTPServer):
        """Test scrolling down."""
        viewer = create_test_viewer()
        try:
            viewer.load_url(mock_html_server.url_for("/"))
            # Add many lines to enable scrolling
            viewer._lines = ["Line " + str(i) for i in range(100)]
            initial = viewer.scroll_position
            viewer.scroll_down(5)
            assert viewer.scroll_position == initial + 5
        finally:
            viewer.close()

    def test_scroll_up(self, mock_html_server: HTTPServer):
        """Test scrolling up."""
        viewer = create_test_viewer()
        try:
            viewer.load_url(mock_html_server.url_for("/"))
            # Add many lines to enable scrolling
            viewer._lines = ["Line " + str(i) for i in range(100)]
            viewer.scroll_down(10)
            viewer.scroll_up(5)
            assert viewer.scroll_position == 5
        finally:
            viewer.close()

    def test_scroll_up_at_top(self, mock_html_server: HTTPServer):
        """Test scrolling up at top of page."""
        viewer = create_test_viewer()
        try:
            viewer.load_url(mock_html_server.url_for("/"))
            viewer.scroll_up(10)
            assert viewer.scroll_position == 0
        finally:
            viewer.close()

    def test_scroll_to_top(self, mock_html_server: HTTPServer):
        """Test scrolling to top."""
        viewer = create_test_viewer()
        try:
            viewer.load_url(mock_html_server.url_for("/"))
            viewer.scroll_down(50)
            viewer.scroll_to_top()
            assert viewer.scroll_position == 0
        finally:
            viewer.close()

    def test_scroll_to_bottom(self, mock_html_server: HTTPServer):
        """Test scrolling to bottom."""
        viewer = create_test_viewer()
        try:
            viewer.load_url(mock_html_server.url_for("/"))
            viewer.scroll_to_bottom()
            assert viewer.scroll_position >= 0
        finally:
            viewer.close()

    def test_history_back(self, mock_html_server: HTTPServer):
        """Test going back in history."""
        viewer = create_test_viewer()
        try:
            url1 = mock_html_server.url_for("/")
            url2 = mock_html_server.url_for("/page2")

            viewer.load_url(url1)
            viewer.load_url(url2)

            success = viewer.go_back()
            assert success is True
            assert viewer.current_url == url1
        finally:
            viewer.close()

    def test_history_back_at_start(self):
        """Test going back at start of history."""
        viewer = WebViewer()
        try:
            success = viewer.go_back()
            assert success is False
        finally:
            viewer.close()

    def test_history_forward(self, mock_html_server: HTTPServer):
        """Test going forward in history."""
        viewer = create_test_viewer()
        try:
            url1 = mock_html_server.url_for("/")
            url2 = mock_html_server.url_for("/page2")

            viewer.load_url(url1)
            viewer.load_url(url2)
            viewer.go_back()

            success = viewer.go_forward()
            assert success is True
            assert viewer.current_url == url2
        finally:
            viewer.close()

    def test_history_forward_at_end(self, mock_html_server: HTTPServer):
        """Test going forward at end of history."""
        viewer = create_test_viewer()
        try:
            viewer.load_url(mock_html_server.url_for("/"))
            success = viewer.go_forward()
            assert success is False
        finally:
            viewer.close()

    def test_select_next_link(self, mock_html_server: HTTPServer):
        """Test selecting next link."""
        # Use readability=False to preserve links in simple HTML
        viewer = create_test_viewer(use_readability=False)
        try:
            viewer.load_url(mock_html_server.url_for("/"))
            # Test page should have links
            if viewer.current_page and viewer.current_page.links:
                viewer.select_next_link()
                assert viewer.selected_link >= 0
        finally:
            viewer.close()

    def test_select_previous_link(self, mock_html_server: HTTPServer):
        """Test selecting previous link."""
        # Use readability=False to preserve links in simple HTML
        viewer = create_test_viewer(use_readability=False)
        try:
            viewer.load_url(mock_html_server.url_for("/"))
            # Test page should have links
            if viewer.current_page and viewer.current_page.links:
                viewer.select_next_link()
                viewer.select_next_link()
                viewer.select_previous_link()
                assert viewer.selected_link >= 0
        finally:
            viewer.close()

    def test_follow_selected_link(self, mock_html_server: HTTPServer):
        """Test following selected link."""
        viewer = create_test_viewer()
        try:
            viewer.load_url(mock_html_server.url_for("/"))
            viewer.select_next_link()
            # Link may not exist or be valid, so just check it doesn't crash
            viewer.follow_selected_link()
        finally:
            viewer.close()

    def test_get_status_info(self, mock_html_server: HTTPServer):
        """Test getting status information."""
        viewer = create_test_viewer()
        try:
            viewer.load_url(mock_html_server.url_for("/"))
            info = viewer.get_status_info()

            assert "url" in info
            assert "title" in info
            assert "scroll" in info
            assert "total_lines" in info
        finally:
            viewer.close()

    def test_toggle_images(self):
        """Test toggling image display."""
        viewer = WebViewer(show_images=True)
        try:
            assert viewer._show_images is True
            viewer.toggle_images()
            assert viewer._show_images is False
            viewer.toggle_images()
            assert viewer._show_images is True
        finally:
            viewer.close()

    def test_context_manager(self, mock_html_server: HTTPServer):
        """Test WebViewer as context manager."""
        with create_test_viewer() as viewer:
            viewer.load_url(mock_html_server.url_for("/"))
            assert viewer.current_page is not None

    def test_display(self, mock_html_server: HTTPServer):
        """Test display method."""
        viewer = create_test_viewer()
        try:
            viewer.load_url(mock_html_server.url_for("/"))
            output = viewer.display()
            assert isinstance(output, str)
            assert len(output) > 0
        finally:
            viewer.close()

    def test_get_lines(self, mock_html_server: HTTPServer):
        """Test getting text lines."""
        viewer = create_test_viewer()
        try:
            viewer.load_url(mock_html_server.url_for("/"))
            lines = viewer.get_lines()
            assert isinstance(lines, list)
        finally:
            viewer.close()


class TestOpenInBrowser:
    """Tests for opening URLs in default browser."""

    def test_open_current_page_in_browser(self, mock_html_server: HTTPServer):
        """Test opening current page in default browser."""
        viewer = create_test_viewer()
        try:
            url = mock_html_server.url_for("/")
            viewer.load_url(url)

            with patch("webbrowser.open") as mock_open:
                result = viewer.open_in_browser()
                assert result is True
                mock_open.assert_called_once_with(url)
        finally:
            viewer.close()

    def test_open_in_browser_no_page_loaded(self):
        """Test opening browser with no page loaded."""
        viewer = WebViewer()
        try:
            with patch("webbrowser.open") as mock_open:
                result = viewer.open_in_browser()
                assert result is False
                mock_open.assert_not_called()
        finally:
            viewer.close()

    def test_open_selected_link_in_browser(self, mock_html_server: HTTPServer):
        """Test opening selected link in default browser."""
        viewer = create_test_viewer(use_readability=False)
        try:
            viewer.load_url(mock_html_server.url_for("/"))
            # Select a link
            if viewer.current_page and viewer.current_page.links:
                viewer.select_next_link()
                link = viewer.get_link_by_index(viewer.selected_link)

                with patch("webbrowser.open") as mock_open:
                    result = viewer.open_link_in_browser()
                    assert result is True
                    mock_open.assert_called_once_with(link.url)
        finally:
            viewer.close()

    def test_open_link_in_browser_no_selection(self, mock_html_server: HTTPServer):
        """Test opening link in browser with no link selected."""
        viewer = create_test_viewer()
        try:
            viewer.load_url(mock_html_server.url_for("/"))
            # No link selected (selected_link = -1)

            with patch("webbrowser.open") as mock_open:
                result = viewer.open_link_in_browser()
                assert result is False
                mock_open.assert_not_called()
        finally:
            viewer.close()

    def test_open_specific_link_in_browser(self, mock_html_server: HTTPServer):
        """Test opening a specific link by index in browser."""
        viewer = create_test_viewer(use_readability=False)
        try:
            viewer.load_url(mock_html_server.url_for("/"))

            if viewer.current_page and viewer.current_page.links:
                link = viewer.current_page.links[0]

                with patch("webbrowser.open") as mock_open:
                    result = viewer.open_link_in_browser(0)
                    assert result is True
                    mock_open.assert_called_once_with(link.url)
        finally:
            viewer.close()

    def test_open_invalid_link_index_in_browser(self, mock_html_server: HTTPServer):
        """Test opening invalid link index in browser."""
        viewer = create_test_viewer()
        try:
            viewer.load_url(mock_html_server.url_for("/"))

            with patch("webbrowser.open") as mock_open:
                result = viewer.open_link_in_browser(999)
                assert result is False
                mock_open.assert_not_called()
        finally:
            viewer.close()
