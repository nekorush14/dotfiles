"""Image file discovery for imgcat.

This module provides functions to discover and collect image files
from directories, enabling automatic file navigation.
"""

from pathlib import Path
from typing import Sequence

from .renderer import SUPPORTED_FORMATS


def discover_images(directory: Path) -> list[str]:
    """Discover all supported image files in a directory.

    Args:
        directory: Directory path to search

    Returns:
        Sorted list of absolute paths to image files

    Raises:
        FileNotFoundError: If directory does not exist
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if not directory.is_dir():
        raise ValueError(f"Not a directory: {directory}")

    images = []
    for path in directory.iterdir():
        if path.is_file() and path.suffix.lower() in SUPPORTED_FORMATS:
            images.append(str(path.resolve()))

    # Sort alphabetically by filename (case-insensitive)
    return sorted(images, key=lambda p: Path(p).name.lower())


def expand_to_directory(file_path: str) -> list[str]:
    """Expand a single file to include all images in its directory.

    The specified file will be placed first in the result list,
    followed by other images in alphabetical order.

    Args:
        file_path: Path to an image file

    Returns:
        List of image paths with the specified file first

    Raises:
        FileNotFoundError: If file does not exist
    """
    path = Path(file_path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    directory = path.parent
    all_images = discover_images(directory)

    # Ensure the target file is first
    target = str(path)
    if target in all_images:
        all_images.remove(target)

    return [target] + all_images


def discover_images_from_args(args: Sequence[str]) -> list[str]:
    """Process CLI arguments to get list of image files.

    Behavior:
    - No args: Discover images in current working directory
    - Single directory: Discover images in that directory
    - Single file: Expand to include sibling images
    - Multiple files/directories: Collect all images from each

    Args:
        args: CLI arguments (file or directory paths)

    Returns:
        List of image file paths

    Raises:
        FileNotFoundError: If no images found
    """
    if not args:
        # No arguments: discover from current directory
        cwd = Path.cwd()
        images = discover_images(cwd)
        if not images:
            raise FileNotFoundError(
                f"No image files found in current directory: {cwd}"
            )
        return images

    if len(args) == 1:
        path = Path(args[0]).resolve()

        if path.is_dir():
            # Single directory: discover images in it
            images = discover_images(path)
            if not images:
                raise FileNotFoundError(
                    f"No image files found in directory: {path}"
                )
            return images
        else:
            # Single file: expand to include siblings
            return expand_to_directory(args[0])

    # Multiple files/directories: collect unique images
    seen = set()
    result = []

    for arg in args:
        path = Path(arg).resolve()

        if path.is_dir():
            # Directory: discover all images in it
            dir_images = discover_images(path)
            for img in dir_images:
                if img not in seen:
                    seen.add(img)
                    result.append(img)
        else:
            # File: add it and expand to siblings
            path_str = str(path)

            if path_str not in seen:
                seen.add(path_str)
                result.append(path_str)

            # Add siblings from the same directory
            siblings = discover_images(path.parent)
            for sibling in siblings:
                if sibling not in seen:
                    seen.add(sibling)
                    result.append(sibling)

    if not result:
        raise FileNotFoundError("No image files found in specified paths")

    return result
