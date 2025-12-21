"""Tests for webcat.parser module."""

import pytest

from webcat.parser import HTMLParser, ParsedPage, Link, ImageInfo


class TestLink:
    """Tests for Link dataclass."""

    def test_link_creation(self):
        """Test creating a Link object."""
        link = Link(
            text="Example Link",
            url="https://example.com",
            position=10,
            index=1,
        )
        assert link.text == "Example Link"
        assert link.url == "https://example.com"
        assert link.position == 10
        assert link.index == 1


class TestImageInfo:
    """Tests for ImageInfo dataclass."""

    def test_image_info_creation(self):
        """Test creating an ImageInfo object."""
        img = ImageInfo(
            src="https://example.com/image.png",
            alt="Test image",
            position=5,
        )
        assert img.src == "https://example.com/image.png"
        assert img.alt == "Test image"
        assert img.position == 5
        assert img.width is None
        assert img.height is None

    def test_image_info_with_dimensions(self):
        """Test creating an ImageInfo with dimensions."""
        img = ImageInfo(
            src="/image.png",
            alt="Sized image",
            position=10,
            width=800,
            height=600,
        )
        assert img.width == 800
        assert img.height == 600


class TestParsedPage:
    """Tests for ParsedPage dataclass."""

    def test_parsed_page_creation(self):
        """Test creating a ParsedPage object."""
        page = ParsedPage(
            title="Test Page",
            text="Hello World",
        )
        assert page.title == "Test Page"
        assert page.text == "Hello World"
        assert page.links == []
        assert page.images == []

    def test_parsed_page_with_links(self):
        """Test ParsedPage with links."""
        link = Link("Click", "/url", 0, 1)
        page = ParsedPage(
            title="Page",
            text="Text",
            links=[link],
        )
        assert len(page.links) == 1
        assert page.links[0].text == "Click"


class TestHTMLParser:
    """Tests for HTMLParser class."""

    def test_parser_initialization(self):
        """Test HTMLParser initialization."""
        parser = HTMLParser()
        assert parser.use_readability is True
        assert parser.include_links is True
        assert parser.include_images is True

    def test_parser_initialization_custom(self):
        """Test HTMLParser with custom settings."""
        parser = HTMLParser(
            use_readability=False,
            include_links=False,
            include_images=False,
        )
        assert parser.use_readability is False
        assert parser.include_links is False
        assert parser.include_images is False

    def test_parse_simple_html(self, test_html_content: str):
        """Test parsing simple HTML content."""
        parser = HTMLParser(use_readability=False)
        result = parser.parse(test_html_content, "https://example.com")

        assert isinstance(result, ParsedPage)
        assert result.title == "Test Page"
        assert "Test Title" in result.text

    def test_parse_extracts_links(self, test_html_content: str):
        """Test that parser extracts links."""
        parser = HTMLParser(use_readability=False)
        result = parser.parse(test_html_content, "https://example.com")

        assert len(result.links) >= 1
        link_urls = [link.url for link in result.links]
        # Relative link should be resolved
        assert any("/link1" in url or "link1" in url for url in link_urls)

    def test_parse_extracts_images(self, test_html_content: str):
        """Test that parser extracts images."""
        parser = HTMLParser(use_readability=False)
        result = parser.parse(test_html_content, "https://example.com")

        assert len(result.images) >= 1
        assert any("test-image.png" in img.src for img in result.images)

    def test_parse_resolves_relative_urls(self):
        """Test that relative URLs are resolved."""
        html = '<html><body><a href="/page">Link</a></body></html>'
        parser = HTMLParser(use_readability=False)
        result = parser.parse(html, "https://example.com/base/")

        assert len(result.links) == 1
        assert result.links[0].url == "https://example.com/page"

    def test_parse_without_images(self, test_html_content: str):
        """Test parsing with images disabled."""
        parser = HTMLParser(use_readability=False, include_images=False)
        result = parser.parse(test_html_content, "https://example.com")

        assert result.images == []

    def test_parse_without_links(self, test_html_content: str):
        """Test parsing with links disabled."""
        parser = HTMLParser(use_readability=False, include_links=False)
        result = parser.parse(test_html_content, "https://example.com")

        assert result.links == []

    def test_html_to_text_basic(self):
        """Test HTML to text conversion."""
        parser = HTMLParser()
        html = "<html><body><h1>Title</h1><p>Paragraph text.</p></body></html>"
        text, links = parser.html_to_text(html)

        assert "Title" in text
        assert "Paragraph text" in text

    def test_html_to_text_with_links(self):
        """Test HTML to text with link references."""
        parser = HTMLParser()
        html = '<html><body><p>Click <a href="/test">here</a>.</p></body></html>'
        text, links = parser.html_to_text(html, include_link_refs=True)

        # Link text should be in output
        assert "here" in text
        assert len(links) == 1
        assert links[0].url == "/test"

    def test_html_to_text_width(self):
        """Test HTML to text with custom width."""
        parser = HTMLParser()
        html = "<html><body><p>" + "word " * 50 + "</p></body></html>"
        text, _ = parser.html_to_text(html, width=40)

        # Lines should be wrapped
        lines = text.strip().split("\n")
        # Most lines should be under width limit
        assert all(len(line) <= 50 for line in lines)

    def test_extract_images_basic(self):
        """Test image extraction."""
        parser = HTMLParser()
        html = '<html><body><img src="/img.png" alt="Test"></body></html>'
        images = parser.extract_images(html, "https://example.com")

        assert len(images) == 1
        assert images[0].src == "https://example.com/img.png"
        assert images[0].alt == "Test"

    def test_extract_images_no_alt(self):
        """Test image extraction without alt text."""
        parser = HTMLParser()
        html = '<html><body><img src="/img.png"></body></html>'
        images = parser.extract_images(html, "https://example.com")

        assert len(images) == 1
        assert images[0].alt == ""

    def test_extract_images_with_dimensions(self):
        """Test image extraction with width/height."""
        parser = HTMLParser()
        html = '<html><body><img src="/img.png" width="100" height="200"></body></html>'
        images = parser.extract_images(html, "https://example.com")

        assert len(images) == 1
        assert images[0].width == 100
        assert images[0].height == 200

    def test_parse_empty_html(self):
        """Test parsing empty HTML."""
        parser = HTMLParser(use_readability=False)
        result = parser.parse("", "https://example.com")

        assert result.title == ""
        assert result.text == ""

    def test_parse_malformed_html(self):
        """Test parsing malformed HTML."""
        parser = HTMLParser(use_readability=False)
        html = "<html><body><p>Unclosed paragraph<div>Nested</p></div></body>"
        result = parser.parse(html, "https://example.com")

        # Should not raise, should handle gracefully
        assert isinstance(result, ParsedPage)
        assert "Unclosed" in result.text or "Nested" in result.text
