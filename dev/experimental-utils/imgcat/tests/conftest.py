"""Pytest fixtures for imgcat tests."""

import pytest
from pathlib import Path
from PIL import Image


@pytest.fixture
def sample_png(tmp_path: Path) -> str:
    """Create a sample PNG image for testing."""
    img = Image.new("RGB", (100, 100), color="red")
    path = tmp_path / "test.png"
    img.save(path)
    return str(path)


@pytest.fixture
def sample_jpeg(tmp_path: Path) -> str:
    """Create a sample JPEG image for testing."""
    img = Image.new("RGB", (100, 100), color="green")
    path = tmp_path / "test.jpg"
    img.save(path)
    return str(path)


@pytest.fixture
def sample_webp(tmp_path: Path) -> str:
    """Create a sample WebP image for testing."""
    img = Image.new("RGB", (100, 100), color="blue")
    path = tmp_path / "test.webp"
    img.save(path)
    return str(path)


@pytest.fixture
def sample_bmp(tmp_path: Path) -> str:
    """Create a sample BMP image for testing."""
    img = Image.new("RGB", (100, 100), color="yellow")
    path = tmp_path / "test.bmp"
    img.save(path)
    return str(path)


@pytest.fixture
def sample_gif(tmp_path: Path) -> str:
    """Create a sample static GIF image for testing."""
    img = Image.new("RGB", (100, 100), color="purple")
    path = tmp_path / "test.gif"
    img.save(path)
    return str(path)


@pytest.fixture
def sample_animated_gif(tmp_path: Path) -> str:
    """Create a sample animated GIF (3 frames) for testing."""
    frames = [
        Image.new("RGB", (50, 50), color="red"),
        Image.new("RGB", (50, 50), color="green"),
        Image.new("RGB", (50, 50), color="blue"),
    ]
    path = tmp_path / "animated.gif"
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
    )
    return str(path)


@pytest.fixture
def sample_svg(tmp_path: Path) -> str:
    """Create a sample SVG file for testing."""
    svg_content = '''<?xml version="1.0"?>
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="50" r="40" fill="blue"/>
</svg>'''
    path = tmp_path / "test.svg"
    path.write_text(svg_content)
    return str(path)


@pytest.fixture
def multiple_images(tmp_path: Path) -> list[str]:
    """Create multiple images for testing file navigation."""
    paths = []
    colors = ["red", "green", "blue", "yellow", "purple"]
    for i, color in enumerate(colors):
        img = Image.new("RGB", (100, 100), color=color)
        path = tmp_path / f"image_{i}.png"
        img.save(path)
        paths.append(str(path))
    return paths
