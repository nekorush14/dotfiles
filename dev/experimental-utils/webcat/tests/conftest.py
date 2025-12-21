"""Shared test fixtures for webcat tests."""

import pytest
from pytest_httpserver import HTTPServer


@pytest.fixture
def test_html_content() -> str:
    """Create test HTML content."""
    return """<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Test Title</h1>
    <p>This is a test paragraph with <a href="/link1">link one</a>.</p>
    <p>Another paragraph with <a href="https://example.com/external">external link</a>.</p>
    <img src="/test-image.png" alt="Test image">
    <div class="content">
        <p>Main content goes here.</p>
    </div>
</body>
</html>"""


@pytest.fixture
def test_image_bytes() -> bytes:
    """Create a minimal valid PNG image."""
    from io import BytesIO
    from PIL import Image

    # Create a 10x10 red image
    img = Image.new("RGB", (10, 10), color="red")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


@pytest.fixture(scope="session")
def httpserver_listen_address():
    """Configure httpserver to listen on localhost."""
    return ("127.0.0.1", 0)


@pytest.fixture
def mock_html_server(httpserver: HTTPServer, test_html_content: str) -> HTTPServer:
    """Create a mock HTTP server serving test HTML."""
    httpserver.expect_request("/").respond_with_data(
        test_html_content,
        content_type="text/html; charset=utf-8",
    )
    httpserver.expect_request("/page2").respond_with_data(
        "<html><body><h1>Page 2</h1></body></html>",
        content_type="text/html",
    )
    return httpserver


@pytest.fixture
def mock_image_server(
    httpserver: HTTPServer,
    test_html_content: str,
    test_image_bytes: bytes,
) -> HTTPServer:
    """Create a mock HTTP server serving HTML and images."""
    httpserver.expect_request("/").respond_with_data(
        test_html_content,
        content_type="text/html; charset=utf-8",
    )
    httpserver.expect_request("/test-image.png").respond_with_data(
        test_image_bytes,
        content_type="image/png",
    )
    return httpserver


@pytest.fixture
def mock_redirect_server(httpserver: HTTPServer, test_html_content: str) -> HTTPServer:
    """Create a mock HTTP server with redirect."""
    httpserver.expect_request("/redirect").respond_with_data(
        "",
        status=302,
        headers={"Location": "/final"},
    )
    httpserver.expect_request("/final").respond_with_data(
        test_html_content,
        content_type="text/html",
    )
    return httpserver
