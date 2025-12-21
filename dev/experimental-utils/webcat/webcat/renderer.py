"""Terminal renderer module for webcat.

This module handles rendering pages and images to the terminal.
"""

import shutil
from io import BytesIO
from typing import Optional

from PIL import Image

from .kitty import KittyGraphics
from .parser import ParsedPage, Link


class TerminalRenderer:
    """Terminal output renderer."""

    def __init__(
        self,
        width: Optional[int] = None,
        show_images: bool = True,
        image_max_width: Optional[int] = None,
        image_max_height: Optional[int] = None,
    ) -> None:
        """Initialize TerminalRenderer.

        Args:
            width: Output width (None for terminal width)
            show_images: Show images
            image_max_width: Maximum image width in pixels
            image_max_height: Maximum image height in pixels
        """
        self.width = width
        self.show_images = show_images
        self.image_max_width = image_max_width
        self.image_max_height = image_max_height
        self._kitty = KittyGraphics()

    def _get_width(self) -> int:
        """Get the effective output width."""
        if self.width is not None:
            return self.width
        term_size = shutil.get_terminal_size()
        return term_size.columns

    def render_page(self, page: ParsedPage) -> str:
        """Render a full page.

        Args:
            page: ParsedPage object

        Returns:
            Terminal output string
        """
        parts = []

        # Render title
        if page.title:
            parts.append(self._render_title(page.title))
            parts.append("")

        # Render text content
        parts.append(page.text)

        # Render links section
        if page.links:
            links_section = self._render_links_section(page.links)
            if links_section:
                parts.append("")
                parts.append(links_section)

        return "\n".join(parts)

    def _render_title(self, title: str) -> str:
        """Render page title with visual formatting.

        Args:
            title: Page title

        Returns:
            Formatted title string
        """
        width = self._get_width()
        separator = "─" * min(len(title) + 4, width)
        return f"{separator}\n  {title}\n{separator}"

    def _render_links_section(self, links: list[Link]) -> str:
        """Render links reference section.

        Args:
            links: List of Link objects

        Returns:
            Formatted links section
        """
        if not links:
            return ""

        parts = ["", "Links:"]
        for link in links:
            parts.append(f"  [{link.index}] {link.url}")

        return "\n".join(parts)

    def render_text_segment(
        self,
        lines: list[str],
        start_line: int,
        end_line: int,
    ) -> str:
        """Render a portion of text lines.

        Args:
            lines: All text lines
            start_line: Start line index
            end_line: End line index (exclusive)

        Returns:
            Terminal output string
        """
        # Clamp indices to valid range
        start = max(0, start_line)
        end = min(len(lines), end_line)

        return "\n".join(lines[start:end])

    def render_image(
        self,
        image_data: bytes,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
    ) -> str:
        """Render an image using Kitty protocol.

        Args:
            image_data: Image binary data
            max_width: Override max width
            max_height: Override max height

        Returns:
            Kitty protocol command string
        """
        if not self.show_images:
            return ""

        try:
            # Load image
            img = Image.open(BytesIO(image_data))

            # Use provided constraints or defaults
            max_w = max_width or self.image_max_width
            max_h = max_height or self.image_max_height

            # Resize if needed
            if max_w or max_h:
                img = self._resize_image(img, max_w, max_h)

            # Convert to RGB if necessary
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")

            # Generate Kitty protocol output
            return self._kitty.display_image(img, delete_previous=False)

        except Exception:
            return ""

    def _resize_image(
        self,
        img: Image.Image,
        max_width: Optional[int],
        max_height: Optional[int],
    ) -> Image.Image:
        """Resize image to fit within constraints.

        Args:
            img: PIL Image
            max_width: Maximum width
            max_height: Maximum height

        Returns:
            Resized image
        """
        orig_width, orig_height = img.size

        if not max_width and not max_height:
            return img

        # Calculate scale factors
        scale_w = max_width / orig_width if max_width else float("inf")
        scale_h = max_height / orig_height if max_height else float("inf")
        scale = min(scale_w, scale_h)

        if scale >= 1.0:
            return img

        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)

        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def render_link_highlight(
        self,
        link_index: int,
        selected: bool = False,
    ) -> str:
        """Render a link with highlight formatting.

        Args:
            link_index: Link reference number
            selected: Whether the link is selected

        Returns:
            ANSI-formatted link text
        """
        if selected:
            # Bold + reverse video for selected
            return f"\x1b[1;7m[{link_index}]\x1b[0m"
        else:
            # Cyan color for normal links
            return f"\x1b[36m[{link_index}]\x1b[0m"

    def clear(self) -> str:
        """Clear the terminal display.

        Returns:
            Clear screen command
        """
        # Clear screen and move cursor to top-left
        # Also clear any Kitty images
        return "\x1b[2J\x1b[H" + self._kitty.clear_screen()
