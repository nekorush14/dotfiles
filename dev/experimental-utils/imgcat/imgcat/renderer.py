"""Image renderer for imgcat.

This module handles loading and rendering various image formats
including PNG, JPEG, GIF (static and animated), WebP, BMP, TIFF, and SVG.
"""

from pathlib import Path
from typing import Optional
from PIL import Image
from io import BytesIO
import cairosvg


# Supported image formats
SUPPORTED_FORMATS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".bmp",
    ".tiff",
    ".tif",
    ".svg",
}


class ImageRenderer:
    """Image renderer supporting multiple formats with zoom and resize."""

    def __init__(self, image_path: str):
        """Initialize the image renderer.

        Args:
            image_path: Path to the image file

        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the format is not supported
        """
        self.image_path = Path(image_path)

        if not self.image_path.exists():
            raise FileNotFoundError(f"File not found: {image_path}")

        suffix = self.image_path.suffix.lower()
        if suffix not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {suffix}")

        self._image: Optional[Image.Image] = None
        self._is_animated = False
        self._frame_count = 1

    @property
    def is_svg(self) -> bool:
        """Check if the file is an SVG."""
        return self.image_path.suffix.lower() == ".svg"

    @property
    def is_animated(self) -> bool:
        """Check if the image is an animated GIF."""
        if self._image is None:
            self._load_image()
        return self._is_animated

    @property
    def frame_count(self) -> int:
        """Get the number of frames (for animated GIF)."""
        if self._image is None:
            self._load_image()
        return self._frame_count

    def _load_image(self) -> None:
        """Load the image (lazy loading)."""
        if self.is_svg:
            self._load_svg()
        else:
            self._image = Image.open(self.image_path)

            # Check for animated GIF
            if self.image_path.suffix.lower() == ".gif":
                try:
                    self._frame_count = self._image.n_frames
                    self._is_animated = self._frame_count > 1
                except AttributeError:
                    self._is_animated = False
                    self._frame_count = 1

    def _load_svg(self) -> None:
        """Load and rasterize SVG file using CairoSVG."""
        png_data = cairosvg.svg2png(url=str(self.image_path))
        self._image = Image.open(BytesIO(png_data))

    def get_image_size(self) -> tuple[int, int]:
        """Get the original image size.

        Returns:
            Tuple of (width, height)
        """
        if self._image is None:
            self._load_image()
        return self._image.size

    def render(
        self,
        zoom: float = 1.0,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
        frame: int = 0,
    ) -> Image.Image:
        """Render the image with optional zoom and size constraints.

        Args:
            zoom: Zoom level (1.0 = 100%)
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels
            frame: Frame number for animated GIF (0-indexed)

        Returns:
            Rendered PIL Image
        """
        if self._image is None:
            self._load_image()

        # For animated GIF, seek to the specified frame
        if self._is_animated and frame < self._frame_count:
            self._image.seek(frame)

        # Convert to RGB mode (GIF might be in P mode)
        if self._image.mode in ("P", "RGBA"):
            img = self._image.convert("RGB")
        else:
            img = self._image.copy()

        # Get original size
        orig_width, orig_height = img.size

        # Calculate effective zoom with max_width/max_height constraints
        effective_zoom = zoom

        if max_width or max_height:
            if max_width:
                width_scale = max_width / orig_width
            else:
                width_scale = float("inf")

            if max_height:
                height_scale = max_height / orig_height
            else:
                height_scale = float("inf")

            fit_scale = min(width_scale, height_scale)
            effective_zoom = fit_scale * zoom

        # Calculate new size
        new_width = int(orig_width * effective_zoom)
        new_height = int(orig_height * effective_zoom)

        if new_width <= 0 or new_height <= 0:
            raise ValueError(f"Invalid size after zoom: {new_width}x{new_height}")

        # Resize if needed
        if (new_width, new_height) != img.size:
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        return img

    def get_frame_duration(self, frame: int = 0) -> int:
        """Get the display duration for a frame (in milliseconds).

        Args:
            frame: Frame number (0-indexed)

        Returns:
            Duration in milliseconds (0 for static images)
        """
        if self._image is None:
            self._load_image()

        if not self._is_animated:
            return 0

        self._image.seek(frame)
        return self._image.info.get("duration", 100)

    def close(self) -> None:
        """Close the image and release resources."""
        if self._image is not None:
            self._image.close()
            self._image = None

    def __enter__(self) -> "ImageRenderer":
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        self.close()
