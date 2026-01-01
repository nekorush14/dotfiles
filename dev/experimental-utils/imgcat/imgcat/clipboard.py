"""Clipboard operations for imgcat.

This module provides functions to copy images to the system clipboard.
Currently supports macOS.
"""

import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

from PIL import Image


def _get_clipboard_command(image_path: str) -> Optional[list[str]]:
    """Get platform-specific command to copy image to clipboard.

    Args:
        image_path: Path to the image file (must be PNG format)

    Returns:
        Command list for subprocess, or None if platform not supported
    """
    if sys.platform == "darwin":
        # macOS: use osascript to copy image to clipboard
        # The image must be in a format that osascript can read (PNG works best)
        script = f'set the clipboard to (read (POSIX file "{image_path}") as «class PNGf»)'
        return ["osascript", "-e", script]

    # Linux with xclip could be added:
    # if sys.platform == "linux":
    #     return ["xclip", "-selection", "clipboard", "-t", "image/png", "-i", image_path]

    return None


def copy_image_to_clipboard(image_path: str) -> bool:
    """Copy an image to the system clipboard.

    Args:
        image_path: Path to the image file

    Returns:
        True if successful, False otherwise

    Raises:
        FileNotFoundError: If the image file does not exist
        ValueError: If the file is not a valid image
    """
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {image_path}")

    # Verify it's a valid image by trying to open it
    try:
        with Image.open(path) as img:
            # If the image is not PNG, convert it to PNG in a temp file
            if path.suffix.lower() != ".png":
                with tempfile.NamedTemporaryFile(
                    suffix=".png", delete=False
                ) as tmp:
                    temp_path = tmp.name
                    img.save(temp_path, "PNG")
                    return _copy_png_to_clipboard(temp_path)
            else:
                return _copy_png_to_clipboard(str(path.resolve()))
    except Exception as e:
        raise ValueError(f"Invalid image file: {e}")


def _copy_png_to_clipboard(png_path: str) -> bool:
    """Copy a PNG file to clipboard.

    Args:
        png_path: Path to the PNG file

    Returns:
        True if successful, False otherwise
    """
    cmd = _get_clipboard_command(png_path)

    if cmd is None:
        # Platform not supported
        return False

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False
