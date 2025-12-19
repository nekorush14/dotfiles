"""Image viewer for imgcat.

This module provides the main viewer logic for navigating and displaying
multiple image files with zoom control and animation support.
"""

from pathlib import Path
from typing import Optional

from .animation import AnimationController
from .kitty import KittyGraphics
from .renderer import ImageRenderer


class ImageViewer:
    """Interactive image viewer with multiple file and animation support."""

    # Zoom settings
    ZOOM_STEP_SMALL = 0.05  # 5% increment
    ZOOM_STEP_LARGE = 0.10  # 10% increment
    MIN_ZOOM = 0.25
    MAX_ZOOM = 4.0

    def __init__(
        self,
        image_paths: list[str],
        initial_zoom: float = 1.0,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
    ):
        """Initialize the image viewer.

        Args:
            image_paths: List of image file paths
            initial_zoom: Initial zoom level (default: 1.0)
            max_width: Maximum display width in pixels
            max_height: Maximum display height in pixels
        """
        self.image_paths = [Path(p) for p in image_paths]
        self.current_file_index = 0
        self.zoom_level = initial_zoom
        self.max_width = max_width
        self.max_height = max_height
        self.total_files = len(self.image_paths)

        self.kitty = KittyGraphics()
        self.renderer: Optional[ImageRenderer] = None
        self.animation: Optional[AnimationController] = None

        # Load the first file
        self._load_current_file()

    def _load_current_file(self) -> None:
        """Load the current file."""
        # Clean up existing renderer
        if self.renderer is not None:
            self.renderer.close()

        current_path = self.image_paths[self.current_file_index]
        self.renderer = ImageRenderer(str(current_path))

        # Set up animation controller for animated GIFs
        if self.renderer.is_animated:
            frame_durations = [
                self.renderer.get_frame_duration(i)
                for i in range(self.renderer.frame_count)
            ]
            self.animation = AnimationController(
                self.renderer.frame_count,
                frame_durations,
            )
        else:
            self.animation = None

    def next_file(self) -> bool:
        """Navigate to the next file.

        Returns:
            True if navigation succeeded, False if already at last file
        """
        if self.current_file_index < self.total_files - 1:
            self.current_file_index += 1
            self._load_current_file()
            return True
        return False

    def previous_file(self) -> bool:
        """Navigate to the previous file.

        Returns:
            True if navigation succeeded, False if already at first file
        """
        if self.current_file_index > 0:
            self.current_file_index -= 1
            self._load_current_file()
            return True
        return False

    def go_to_file(self, file_num: int) -> None:
        """Navigate to a specific file by number (1-indexed).

        Args:
            file_num: File number (1-indexed), will be clamped to valid range
        """
        # Convert to 0-indexed and clamp
        index = max(0, min(file_num - 1, self.total_files - 1))
        if index != self.current_file_index:
            self.current_file_index = index
            self._load_current_file()

    def go_to_first_file(self) -> None:
        """Navigate to the first file."""
        self.go_to_file(1)

    def go_to_last_file(self) -> None:
        """Navigate to the last file."""
        self.go_to_file(self.total_files)

    def zoom_in(self, large: bool = False) -> bool:
        """Increase zoom level.

        Args:
            large: If True, use 10% increment; otherwise use 5% increment

        Returns:
            True if zoom changed, False if already at max
        """
        step = self.ZOOM_STEP_LARGE if large else self.ZOOM_STEP_SMALL
        new_zoom = self.zoom_level + step
        if new_zoom <= self.MAX_ZOOM:
            self.zoom_level = new_zoom
            return True
        return False

    def zoom_out(self, large: bool = False) -> bool:
        """Decrease zoom level.

        Args:
            large: If True, use 10% increment; otherwise use 5% increment

        Returns:
            True if zoom changed, False if already at min
        """
        step = self.ZOOM_STEP_LARGE if large else self.ZOOM_STEP_SMALL
        new_zoom = self.zoom_level - step
        if new_zoom >= self.MIN_ZOOM:
            self.zoom_level = new_zoom
            return True
        return False

    def set_zoom(self, zoom: float) -> None:
        """Set zoom level directly.

        Args:
            zoom: Zoom level (will be clamped to valid range)
        """
        self.zoom_level = max(self.MIN_ZOOM, min(zoom, self.MAX_ZOOM))

    def reset_zoom(self) -> None:
        """Reset zoom to 100%."""
        self.zoom_level = 1.0

    def toggle_animation(self) -> None:
        """Toggle animation play/pause."""
        if self.animation is not None:
            self.animation.toggle_play_pause()

    def update_animation(self) -> bool:
        """Update animation timer.

        Returns:
            True if frame changed, False otherwise
        """
        if self.animation is not None:
            return self.animation.update()
        return False

    def next_frame(self) -> None:
        """Manually advance to next frame."""
        if self.animation is not None:
            self.animation.next_frame()

    def prev_frame(self) -> None:
        """Manually go to previous frame."""
        if self.animation is not None:
            self.animation.prev_frame()

    def get_info(self) -> dict:
        """Get current viewer information.

        Returns:
            Dictionary with current state information
        """
        info = {
            "current_file": self.current_file_index + 1,
            "total_files": self.total_files,
            "filename": self.image_paths[self.current_file_index].name,
            "zoom": self.zoom_level,
            "is_animated": self.animation is not None,
        }

        if self.animation is not None:
            info["current_frame"] = self.animation.current_frame + 1
            info["total_frames"] = self.animation.frame_count
            info["is_playing"] = self.animation.is_playing

        return info

    def display_current(self) -> str:
        """Display the current image.

        Returns:
            Kitty protocol command string
        """
        if self.renderer is None:
            return ""

        # Get current frame for animated GIFs
        frame = 0
        if self.animation is not None:
            frame = self.animation.current_frame

        # Render the image
        img = self.renderer.render(
            zoom=self.zoom_level,
            max_width=self.max_width,
            max_height=self.max_height,
            frame=frame,
        )

        # Generate Kitty protocol command
        return self.kitty.display_image(img, delete_previous=True)

    def clear_display(self) -> str:
        """Clear the display.

        Returns:
            Kitty protocol command to clear images
        """
        return self.kitty.clear_screen()

    def close(self) -> None:
        """Close the viewer and release resources."""
        if self.renderer is not None:
            self.renderer.close()
            self.renderer = None

    def __enter__(self) -> "ImageViewer":
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        self.close()
