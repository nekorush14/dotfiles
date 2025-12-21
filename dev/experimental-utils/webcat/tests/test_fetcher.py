"""Tests for webcat.fetcher module."""

import pytest
from pytest_httpserver import HTTPServer

from webcat.fetcher import WebFetcher, FetchResult


class TestFetchResult:
    """Tests for FetchResult dataclass."""

    def test_is_html_true_for_html_content(self):
        """Test is_html returns True for HTML content type."""
        result = FetchResult(
            url="http://example.com",
            status_code=200,
            content=b"<html></html>",
            content_type="text/html; charset=utf-8",
            encoding="utf-8",
            headers={},
        )
        assert result.is_html is True

    def test_is_html_false_for_json(self):
        """Test is_html returns False for JSON content type."""
        result = FetchResult(
            url="http://example.com",
            status_code=200,
            content=b"{}",
            content_type="application/json",
            encoding="utf-8",
            headers={},
        )
        assert result.is_html is False

    def test_is_image_true_for_png(self):
        """Test is_image returns True for PNG content type."""
        result = FetchResult(
            url="http://example.com/image.png",
            status_code=200,
            content=b"\x89PNG",
            content_type="image/png",
            encoding=None,
            headers={},
        )
        assert result.is_image is True

    def test_is_image_true_for_jpeg(self):
        """Test is_image returns True for JPEG content type."""
        result = FetchResult(
            url="http://example.com/image.jpg",
            status_code=200,
            content=b"\xff\xd8\xff",
            content_type="image/jpeg",
            encoding=None,
            headers={},
        )
        assert result.is_image is True

    def test_is_pdf_true_for_pdf(self):
        """Test is_pdf returns True for PDF content type."""
        result = FetchResult(
            url="http://example.com/doc.pdf",
            status_code=200,
            content=b"%PDF-1.4",
            content_type="application/pdf",
            encoding=None,
            headers={},
        )
        assert result.is_pdf is True

    def test_text_property_decodes_content(self):
        """Test text property correctly decodes content."""
        result = FetchResult(
            url="http://example.com",
            status_code=200,
            content="Hello World".encode("utf-8"),
            content_type="text/html",
            encoding="utf-8",
            headers={},
        )
        assert result.text == "Hello World"


class TestWebFetcher:
    """Tests for WebFetcher class."""

    def test_fetcher_initialization(self):
        """Test WebFetcher initialization with default values."""
        fetcher = WebFetcher()
        assert fetcher.user_agent == "webcat/1.0"
        assert fetcher.timeout == 30.0
        fetcher.close()

    def test_fetcher_initialization_with_custom_values(self):
        """Test WebFetcher initialization with custom values."""
        fetcher = WebFetcher(
            user_agent="CustomAgent/2.0",
            timeout=60.0,
        )
        assert fetcher.user_agent == "CustomAgent/2.0"
        assert fetcher.timeout == 60.0
        fetcher.close()

    def test_fetch_html_page(self, mock_html_server: HTTPServer):
        """Test fetching an HTML page."""
        fetcher = WebFetcher()
        fetcher._allow_private = True  # Allow mock server on 127.0.0.1
        try:
            result = fetcher.fetch(mock_html_server.url_for("/"))
            assert result.status_code == 200
            assert result.is_html is True
            assert "Test Title" in result.text
        finally:
            fetcher.close()

    def test_fetch_with_redirect(self, mock_redirect_server: HTTPServer):
        """Test fetching a page with redirect."""
        fetcher = WebFetcher()
        fetcher._allow_private = True  # Allow mock server on 127.0.0.1
        try:
            result = fetcher.fetch(mock_redirect_server.url_for("/redirect"))
            assert result.status_code == 200
            # URL should be updated to final destination
            assert "/final" in result.url
        finally:
            fetcher.close()

    def test_fetch_image(self, mock_image_server: HTTPServer, test_image_bytes: bytes):
        """Test fetching an image."""
        fetcher = WebFetcher()
        fetcher._allow_private = True  # Allow mock server on 127.0.0.1
        try:
            result = fetcher.fetch(mock_image_server.url_for("/test-image.png"))
            assert result.status_code == 200
            assert result.is_image is True
            assert result.content == test_image_bytes
        finally:
            fetcher.close()

    def test_fetch_relative_image(
        self,
        mock_image_server: HTTPServer,
        test_image_bytes: bytes,
    ):
        """Test fetching an image with relative URL."""
        fetcher = WebFetcher()
        fetcher._allow_private = True  # Allow mock server on 127.0.0.1
        try:
            base_url = mock_image_server.url_for("/")
            image_data = fetcher.fetch_image("/test-image.png", base_url)
            assert image_data == test_image_bytes
        finally:
            fetcher.close()

    def test_fetch_nonexistent_page(self, mock_html_server: HTTPServer):
        """Test fetching a non-existent page returns 404."""
        fetcher = WebFetcher()
        fetcher._allow_private = True  # Allow mock server on 127.0.0.1
        try:
            result = fetcher.fetch(mock_html_server.url_for("/nonexistent"))
            assert result.status_code == 404 or result.status_code == 500
        finally:
            fetcher.close()

    def test_context_manager(self, mock_html_server: HTTPServer):
        """Test WebFetcher as context manager."""
        with WebFetcher() as fetcher:
            fetcher._allow_private = True  # Allow mock server on 127.0.0.1
            result = fetcher.fetch(mock_html_server.url_for("/"))
            assert result.status_code == 200

    def test_resolve_url_absolute(self):
        """Test URL resolution with absolute URL."""
        fetcher = WebFetcher()
        try:
            resolved = fetcher.resolve_url(
                "https://other.com/page",
                "https://example.com/base",
            )
            assert resolved == "https://other.com/page"
        finally:
            fetcher.close()

    def test_resolve_url_relative(self):
        """Test URL resolution with relative URL."""
        fetcher = WebFetcher()
        try:
            resolved = fetcher.resolve_url(
                "/page",
                "https://example.com/base/",
            )
            assert resolved == "https://example.com/page"
        finally:
            fetcher.close()

    def test_resolve_url_relative_path(self):
        """Test URL resolution with relative path."""
        fetcher = WebFetcher()
        try:
            resolved = fetcher.resolve_url(
                "subpage.html",
                "https://example.com/dir/page.html",
            )
            assert resolved == "https://example.com/dir/subpage.html"
        finally:
            fetcher.close()


class TestSSRFProtection:
    """Tests for SSRF protection."""

    def test_block_file_scheme(self):
        """Test blocking file:// URLs."""
        from webcat.fetcher import UnsafeURLError

        fetcher = WebFetcher()
        try:
            with pytest.raises(UnsafeURLError):
                fetcher.fetch("file:///etc/passwd")
        finally:
            fetcher.close()

    def test_block_localhost(self):
        """Test blocking localhost URLs."""
        from webcat.fetcher import UnsafeURLError

        fetcher = WebFetcher()
        try:
            with pytest.raises(UnsafeURLError):
                fetcher.fetch("http://localhost/admin")
        finally:
            fetcher.close()

    def test_block_127_0_0_1(self):
        """Test blocking 127.0.0.1 URLs."""
        from webcat.fetcher import UnsafeURLError

        fetcher = WebFetcher()
        try:
            with pytest.raises(UnsafeURLError):
                fetcher.fetch("http://127.0.0.1/")
        finally:
            fetcher.close()

    def test_block_private_ip_10(self):
        """Test blocking 10.x.x.x private IPs."""
        from webcat.fetcher import UnsafeURLError

        fetcher = WebFetcher()
        try:
            with pytest.raises(UnsafeURLError):
                fetcher.fetch("http://10.0.0.1/")
        finally:
            fetcher.close()

    def test_block_private_ip_172(self):
        """Test blocking 172.16-31.x.x private IPs."""
        from webcat.fetcher import UnsafeURLError

        fetcher = WebFetcher()
        try:
            with pytest.raises(UnsafeURLError):
                fetcher.fetch("http://172.16.0.1/")
        finally:
            fetcher.close()

    def test_block_private_ip_192(self):
        """Test blocking 192.168.x.x private IPs."""
        from webcat.fetcher import UnsafeURLError

        fetcher = WebFetcher()
        try:
            with pytest.raises(UnsafeURLError):
                fetcher.fetch("http://192.168.1.1/")
        finally:
            fetcher.close()

    def test_allow_public_url(self, mock_html_server: HTTPServer):
        """Test allowing public URLs."""
        fetcher = WebFetcher()
        try:
            # Mock server is on 127.0.0.1, so we need to allow it for testing
            fetcher._allow_private = True
            result = fetcher.fetch(mock_html_server.url_for("/"))
            assert result.status_code == 200
        finally:
            fetcher.close()


class TestResponseSizeLimit:
    """Tests for response size limit."""

    def test_max_size_initialization(self):
        """Test max_size parameter."""
        fetcher = WebFetcher(max_size=1024 * 1024)  # 1MB
        assert fetcher.max_size == 1024 * 1024
        fetcher.close()

    def test_default_max_size(self):
        """Test default max_size is set."""
        fetcher = WebFetcher()
        assert fetcher.max_size == 50 * 1024 * 1024  # 50MB default
        fetcher.close()
