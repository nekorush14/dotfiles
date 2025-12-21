"""HTML parser module for webcat.

This module handles HTML parsing, readability extraction, and text conversion.
"""

from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import html2text


@dataclass
class Link:
    """Page link information."""

    text: str
    url: str
    position: int
    index: int


@dataclass
class ImageInfo:
    """Image information."""

    src: str
    alt: str
    position: int
    width: Optional[int] = None
    height: Optional[int] = None


@dataclass
class ParsedPage:
    """Parsed page content."""

    title: str
    text: str
    links: list[Link] = field(default_factory=list)
    images: list[ImageInfo] = field(default_factory=list)
    raw_html: str = ""
    readable_html: str = ""


class HTMLParser:
    """HTML parser with readability extraction."""

    def __init__(
        self,
        use_readability: bool = True,
        include_links: bool = True,
        include_images: bool = True,
    ) -> None:
        """Initialize HTMLParser.

        Args:
            use_readability: Use readability extraction for main content
            include_links: Extract and include links
            include_images: Extract and include images
        """
        self.use_readability = use_readability
        self.include_links = include_links
        self.include_images = include_images

    def parse(self, html: str, base_url: str) -> ParsedPage:
        """Parse HTML content.

        Args:
            html: HTML string
            base_url: Base URL for resolving relative links

        Returns:
            ParsedPage object
        """
        if not html.strip():
            return ParsedPage(title="", text="", raw_html=html)

        soup = BeautifulSoup(html, "lxml")

        # Extract title
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # Optionally use readability extraction
        if self.use_readability:
            content_html = self._extract_readable(soup)
        else:
            body = soup.find("body")
            content_html = str(body) if body else str(soup)

        # Convert to text with links
        text, links = self.html_to_text(
            content_html,
            include_link_refs=self.include_links,
            base_url=base_url,
        )

        # Clear links if disabled
        if not self.include_links:
            links = []

        # Extract images
        if self.include_images:
            images = self.extract_images(content_html, base_url)
        else:
            images = []

        return ParsedPage(
            title=title,
            text=text,
            links=links,
            images=images,
            raw_html=html,
            readable_html=content_html,
        )

    def _extract_readable(self, soup: BeautifulSoup) -> str:
        """Extract readable content from soup.

        Args:
            soup: BeautifulSoup object

        Returns:
            HTML string of main content
        """
        # Try to find main content areas
        main_selectors = [
            "article",
            "main",
            '[role="main"]',
            ".content",
            ".post",
            ".article",
            "#content",
            "#main",
        ]

        for selector in main_selectors:
            content = soup.select_one(selector)
            if content:
                return str(content)

        # Fallback: use body
        body = soup.find("body")
        if body:
            # Remove navigation, header, footer, etc.
            for tag in body.find_all(["nav", "header", "footer", "aside", "script", "style"]):
                tag.decompose()
            return str(body)

        return str(soup)

    def html_to_text(
        self,
        html: str,
        width: int = 80,
        include_link_refs: bool = True,
        base_url: str = "",
    ) -> tuple[str, list[Link]]:
        """Convert HTML to plain text.

        Args:
            html: HTML string
            width: Output width for wrapping
            include_link_refs: Include link reference numbers
            base_url: Base URL for resolving relative links

        Returns:
            Tuple of (text, list of links)
        """
        # Configure html2text
        h = html2text.HTML2Text()
        h.body_width = width
        h.unicode_snob = True
        h.skip_internal_links = False
        h.inline_links = False
        h.wrap_links = True
        h.ignore_images = True  # We handle images separately

        # Convert HTML to text
        text = h.handle(html)

        # Extract links from HTML
        links = self._extract_links(html, base_url)

        return text.strip(), links

    def _extract_links(self, html: str, base_url: str) -> list[Link]:
        """Extract links from HTML.

        Args:
            html: HTML string
            base_url: Base URL for resolving relative links

        Returns:
            List of Link objects
        """
        soup = BeautifulSoup(html, "lxml")
        links = []
        index = 1

        for anchor in soup.find_all("a", href=True):
            href = anchor.get("href", "")
            text = anchor.get_text(strip=True)

            # Skip empty links
            if not href or not text:
                continue

            # Skip fragment-only links
            if href.startswith("#"):
                continue

            # Resolve relative URL
            if base_url:
                href = urljoin(base_url, href)

            links.append(Link(
                text=text,
                url=href,
                position=0,  # Will be updated during rendering
                index=index,
            ))
            index += 1

        return links

    def extract_images(self, html: str, base_url: str) -> list[ImageInfo]:
        """Extract image information from HTML.

        Args:
            html: HTML string
            base_url: Base URL for resolving relative URLs

        Returns:
            List of ImageInfo objects
        """
        soup = BeautifulSoup(html, "lxml")
        images = []

        for img in soup.find_all("img", src=True):
            src = img.get("src", "")
            if not src:
                continue

            # Resolve relative URL
            src = urljoin(base_url, src)

            alt = img.get("alt", "")

            # Parse dimensions
            width = None
            height = None
            try:
                width_str = img.get("width")
                if width_str:
                    width = int(width_str)
                height_str = img.get("height")
                if height_str:
                    height = int(height_str)
            except (ValueError, TypeError):
                pass

            images.append(ImageInfo(
                src=src,
                alt=alt,
                position=0,  # Will be updated during rendering
                width=width,
                height=height,
            ))

        return images
