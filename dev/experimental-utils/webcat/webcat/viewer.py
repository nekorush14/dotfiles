"""Interactive web viewer module for webcat.

This module provides the interactive viewer functionality for navigating
and displaying web pages in the terminal.
"""

import webbrowser
from dataclasses import dataclass
from typing import Optional

from .fetcher import WebFetcher
from .parser import HTMLParser, ParsedPage, Link
from .renderer import TerminalRenderer


@dataclass
class HistoryEntry:
    """Browsing history entry."""

    url: str
    scroll_position: int = 0


class WebViewer:
    """Interactive web viewer with navigation and history."""

    # Scroll settings
    SCROLL_LINES = 1
    SCROLL_HALF_PAGE = 15
    SCROLL_FULL_PAGE = 30

    def __init__(
        self,
        initial_url: Optional[str] = None,
        width: Optional[int] = None,
        show_images: bool = True,
        use_readability: bool = True,
        user_agent: str = "webcat/1.0",
        timeout: float = 30.0,
    ) -> None:
        """Initialize WebViewer.

        Args:
            initial_url: Initial URL to load
            width: Output width
            show_images: Show images
            use_readability: Use readability extraction
            user_agent: User-Agent header
            timeout: Request timeout
        """
        self._width = width
        self._show_images = show_images
        self._use_readability = use_readability

        self._fetcher = WebFetcher(user_agent, timeout)
        self._parser = HTMLParser(use_readability, include_links=True, include_images=show_images)
        self._renderer = TerminalRenderer(width, show_images)

        self._history: list[HistoryEntry] = []
        self._history_index: int = -1
        self._current_page: Optional[ParsedPage] = None
        self._current_url: str = ""
        self._scroll_position: int = 0
        self._selected_link: int = -1
        self._lines: list[str] = []

        if initial_url:
            self.load_url(initial_url)

    @property
    def current_url(self) -> str:
        """Get current URL."""
        return self._current_url

    @property
    def current_page(self) -> Optional[ParsedPage]:
        """Get current page."""
        return self._current_page

    @property
    def scroll_position(self) -> int:
        """Get current scroll position."""
        return self._scroll_position

    @property
    def selected_link(self) -> int:
        """Get selected link index."""
        return self._selected_link

    def load_url(self, url: str) -> bool:
        """Load a URL.

        Args:
            url: URL to load

        Returns:
            True if successful
        """
        try:
            result = self._fetcher.fetch(url)

            if not result.is_html:
                return False

            self._current_page = self._parser.parse(result.text, result.url)
            self._current_url = result.url
            self._scroll_position = 0
            self._selected_link = -1
            self._lines = self._current_page.text.split("\n")

            # Add to history
            if self._history_index >= 0:
                # Clear forward history
                self._history = self._history[: self._history_index + 1]

            self._history.append(HistoryEntry(url=result.url))
            self._history_index = len(self._history) - 1

            return True

        except Exception:
            return False

    def reload(self) -> bool:
        """Reload current page.

        Returns:
            True if successful
        """
        if not self._current_url:
            return False

        try:
            result = self._fetcher.fetch(self._current_url)
            self._current_page = self._parser.parse(result.text, result.url)
            self._lines = self._current_page.text.split("\n")
            self._selected_link = -1
            return True
        except Exception:
            return False

    def go_back(self) -> bool:
        """Go back in history.

        Returns:
            True if navigated
        """
        if self._history_index <= 0:
            return False

        # Save current scroll position
        if self._history_index < len(self._history):
            self._history[self._history_index].scroll_position = self._scroll_position

        self._history_index -= 1
        entry = self._history[self._history_index]

        try:
            result = self._fetcher.fetch(entry.url)
            self._current_page = self._parser.parse(result.text, result.url)
            self._current_url = result.url
            self._scroll_position = entry.scroll_position
            self._selected_link = -1
            self._lines = self._current_page.text.split("\n")
            return True
        except Exception:
            return False

    def go_forward(self) -> bool:
        """Go forward in history.

        Returns:
            True if navigated
        """
        if self._history_index >= len(self._history) - 1:
            return False

        # Save current scroll position
        if self._history_index >= 0 and self._history_index < len(self._history):
            self._history[self._history_index].scroll_position = self._scroll_position

        self._history_index += 1
        entry = self._history[self._history_index]

        try:
            result = self._fetcher.fetch(entry.url)
            self._current_page = self._parser.parse(result.text, result.url)
            self._current_url = result.url
            self._scroll_position = entry.scroll_position
            self._selected_link = -1
            self._lines = self._current_page.text.split("\n")
            return True
        except Exception:
            return False

    def scroll_down(self, lines: int = 1) -> bool:
        """Scroll down.

        Args:
            lines: Number of lines to scroll

        Returns:
            True if scrolled
        """
        max_scroll = max(0, len(self._lines) - self.SCROLL_FULL_PAGE)
        new_pos = min(self._scroll_position + lines, max_scroll)

        if new_pos != self._scroll_position:
            self._scroll_position = new_pos
            return True
        return False

    def scroll_up(self, lines: int = 1) -> bool:
        """Scroll up.

        Args:
            lines: Number of lines to scroll

        Returns:
            True if scrolled
        """
        new_pos = max(0, self._scroll_position - lines)

        if new_pos != self._scroll_position:
            self._scroll_position = new_pos
            return True
        return False

    def scroll_to_top(self) -> None:
        """Scroll to top of page."""
        self._scroll_position = 0

    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page."""
        max_scroll = max(0, len(self._lines) - self.SCROLL_FULL_PAGE)
        self._scroll_position = max_scroll

    def scroll_to_line(self, line: int) -> None:
        """Scroll to specific line.

        Args:
            line: Line number (0-indexed)
        """
        max_scroll = max(0, len(self._lines) - self.SCROLL_FULL_PAGE)
        self._scroll_position = max(0, min(line, max_scroll))

    def select_next_link(self) -> bool:
        """Select next link.

        Returns:
            True if selected
        """
        if not self._current_page or not self._current_page.links:
            return False

        self._selected_link = (self._selected_link + 1) % len(self._current_page.links)
        return True

    def select_previous_link(self) -> bool:
        """Select previous link.

        Returns:
            True if selected
        """
        if not self._current_page or not self._current_page.links:
            return False

        if self._selected_link <= 0:
            self._selected_link = len(self._current_page.links) - 1
        else:
            self._selected_link -= 1
        return True

    def follow_selected_link(self) -> bool:
        """Follow the currently selected link.

        Returns:
            True if navigated
        """
        if self._selected_link < 0:
            return False

        link = self.get_link_by_index(self._selected_link)
        if link:
            return self.load_url(link.url)
        return False

    def get_link_by_index(self, index: int) -> Optional[Link]:
        """Get link by index.

        Args:
            index: Link index

        Returns:
            Link object or None
        """
        if not self._current_page or not self._current_page.links:
            return None

        if 0 <= index < len(self._current_page.links):
            return self._current_page.links[index]
        return None

    def display(self) -> str:
        """Get current display output.

        Returns:
            Terminal output string
        """
        if not self._current_page:
            return ""

        return self._renderer.render_page(self._current_page)

    def get_lines(self) -> list[str]:
        """Get text lines.

        Returns:
            List of text lines
        """
        return self._lines.copy()

    def get_status_info(self) -> dict:
        """Get status information.

        Returns:
            Status info dictionary
        """
        return {
            "url": self._current_url,
            "title": self._current_page.title if self._current_page else "",
            "scroll": self._scroll_position,
            "total_lines": len(self._lines),
            "selected_link": self._selected_link,
            "history_index": self._history_index,
            "history_length": len(self._history),
        }

    def toggle_images(self) -> None:
        """Toggle image display."""
        self._show_images = not self._show_images
        self._renderer.show_images = self._show_images

    def open_in_browser(self) -> bool:
        """Open current page in default browser.

        Returns:
            True if browser was opened
        """
        if not self._current_url:
            return False

        webbrowser.open(self._current_url)
        return True

    def open_link_in_browser(self, index: Optional[int] = None) -> bool:
        """Open a link in default browser.

        Args:
            index: Link index (uses selected_link if None)

        Returns:
            True if browser was opened
        """
        if index is None:
            index = self._selected_link

        if index < 0:
            return False

        link = self.get_link_by_index(index)
        if not link:
            return False

        webbrowser.open(link.url)
        return True

    def close(self) -> None:
        """Close viewer and release resources."""
        self._fetcher.close()

    def __enter__(self) -> "WebViewer":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()
