"""Interactive PDF viewer logic.

This module provides the interactive viewer functionality for navigating
and displaying PDF documents in the terminal.
"""

import sys
from typing import Optional
from .renderer import PDFRenderer
from .kitty import KittyGraphics


class PDFViewer:
    """Interactive PDF viewer with navigation and zoom controls."""

    # Zoom settings
    ZOOM_STEP = 0.05
    ZOOM_STEP_LARGE = 0.10
    MIN_ZOOM = 0.25
    MAX_ZOOM = 4.0

    def __init__(
        self,
        pdf_path: str,
        initial_zoom: float = 1.0,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
    ):
        """Initialize PDF viewer.

        Args:
            pdf_path: Path to PDF file
            initial_zoom: Initial zoom level (default: 1.0)
            max_width: Maximum display width in pixels
            max_height: Maximum display height in pixels
        """
        self.pdf_path = pdf_path
        self.renderer = PDFRenderer(pdf_path)
        self.kitty = KittyGraphics()

        self.current_page = 0
        self.zoom_level = initial_zoom
        self.max_width = max_width
        self.max_height = max_height
        self.total_pages = self.renderer.get_page_count()

    def next_page(self) -> bool:
        """Navigate to next page.

        Returns:
            True if navigated, False if already at last page
        """
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            return True
        return False

    def previous_page(self) -> bool:
        """Navigate to previous page.

        Returns:
            True if navigated, False if already at first page
        """
        if self.current_page > 0:
            self.current_page -= 1
            return True
        return False

    def zoom_in(self, large: bool = False) -> bool:
        """Increase zoom level.

        Args:
            large: If True, use large step (10%), otherwise use small step (5%)

        Returns:
            True if zoomed in, False if already at max zoom
        """
        step = self.ZOOM_STEP_LARGE if large else self.ZOOM_STEP
        new_zoom = self.zoom_level + step
        if new_zoom <= self.MAX_ZOOM:
            self.zoom_level = new_zoom
            return True
        return False

    def zoom_out(self, large: bool = False) -> bool:
        """Decrease zoom level.

        Args:
            large: If True, use large step (10%), otherwise use small step (5%)

        Returns:
            True if zoomed out, False if already at min zoom
        """
        step = self.ZOOM_STEP_LARGE if large else self.ZOOM_STEP
        new_zoom = self.zoom_level - step
        if new_zoom >= self.MIN_ZOOM:
            self.zoom_level = new_zoom
            return True
        return False

    def set_zoom(self, zoom: float) -> None:
        """Set zoom level directly.

        Args:
            zoom: New zoom level (clamped to MIN_ZOOM and MAX_ZOOM)
        """
        self.zoom_level = max(self.MIN_ZOOM, min(zoom, self.MAX_ZOOM))

    def go_to_page(self, page_num: int) -> None:
        """Jump to specific page (1-indexed).

        Args:
            page_num: Page number (1-indexed for user display)

        Raises:
            ValueError: If page number is out of range
        """
        if page_num < 1 or page_num > self.total_pages:
            raise ValueError(
                f"Page number must be between 1 and {self.total_pages}"
            )

        self.current_page = page_num - 1

    def get_page_info(self) -> dict:
        """Get current page information.

        Returns:
            Dictionary with current page, total pages, and zoom level
        """
        return {
            "current": self.current_page + 1,  # 1-indexed for display
            "total": self.total_pages,
            "zoom": self.zoom_level,
        }

    def display_current_page(self) -> str:
        """Render and display the current page.

        Returns:
            Kitty protocol command string for display
        """
        # Render current page with current zoom
        img = self.renderer.render_page(
            self.current_page,
            zoom=self.zoom_level,
            max_width=self.max_width,
            max_height=self.max_height,
        )

        # Generate display command
        command = self.kitty.display_image(img, delete_previous=True)

        return command

    def clear_display(self) -> str:
        """Clear all images from display.

        Returns:
            Kitty protocol command to clear screen
        """
        return self.kitty.clear_screen()

    def close(self):
        """Close viewer and free resources."""
        self.renderer.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
