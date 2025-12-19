"""Tests for imgcat.renderer module."""

import pytest
from PIL import Image

from imgcat.renderer import ImageRenderer


class TestImageRenderer:
    """Tests for ImageRenderer class."""

    def test_init_with_valid_png(self, sample_png: str):
        """Test renderer initialization with valid PNG file."""
        renderer = ImageRenderer(sample_png)
        assert renderer.image_path.suffix == ".png"
        renderer.close()

    def test_init_with_valid_jpeg(self, sample_jpeg: str):
        """Test renderer initialization with valid JPEG file."""
        renderer = ImageRenderer(sample_jpeg)
        assert renderer.image_path.suffix == ".jpg"
        renderer.close()

    def test_init_with_nonexistent_file(self):
        """Test renderer initialization with nonexistent file."""
        with pytest.raises(FileNotFoundError):
            ImageRenderer("/nonexistent/path/image.png")

    def test_init_with_unsupported_format(self, tmp_path):
        """Test renderer initialization with unsupported format."""
        path = tmp_path / "test.xyz"
        path.write_text("dummy")
        with pytest.raises(ValueError, match="Unsupported"):
            ImageRenderer(str(path))

    def test_get_image_size_png(self, sample_png: str):
        """Test getting image size for PNG."""
        with ImageRenderer(sample_png) as renderer:
            width, height = renderer.get_image_size()
            assert width == 100
            assert height == 100

    def test_get_image_size_jpeg(self, sample_jpeg: str):
        """Test getting image size for JPEG."""
        with ImageRenderer(sample_jpeg) as renderer:
            width, height = renderer.get_image_size()
            assert width == 100
            assert height == 100

    def test_render_default_zoom(self, sample_png: str):
        """Test rendering with default zoom (1.0)."""
        with ImageRenderer(sample_png) as renderer:
            img = renderer.render()
            assert isinstance(img, Image.Image)
            assert img.size == (100, 100)

    def test_render_with_zoom_in(self, sample_png: str):
        """Test rendering with zoom in (2x)."""
        with ImageRenderer(sample_png) as renderer:
            img = renderer.render(zoom=2.0)
            assert img.size == (200, 200)

    def test_render_with_zoom_out(self, sample_png: str):
        """Test rendering with zoom out (0.5x)."""
        with ImageRenderer(sample_png) as renderer:
            img = renderer.render(zoom=0.5)
            assert img.size == (50, 50)

    def test_render_with_max_width(self, sample_png: str):
        """Test rendering with max_width constraint."""
        with ImageRenderer(sample_png) as renderer:
            img = renderer.render(max_width=50)
            assert img.size[0] == 50
            assert img.size[1] == 50  # Aspect ratio preserved

    def test_render_with_max_height(self, sample_png: str):
        """Test rendering with max_height constraint."""
        with ImageRenderer(sample_png) as renderer:
            img = renderer.render(max_height=50)
            assert img.size[0] == 50  # Aspect ratio preserved
            assert img.size[1] == 50

    def test_render_with_max_width_and_zoom(self, sample_png: str):
        """Test rendering with both max_width and zoom."""
        with ImageRenderer(sample_png) as renderer:
            # max_width=50 gives fit_scale=0.5, then zoom=2.0 gives final=1.0
            img = renderer.render(zoom=2.0, max_width=50)
            assert img.size == (100, 100)

    def test_render_webp(self, sample_webp: str):
        """Test rendering WebP format."""
        with ImageRenderer(sample_webp) as renderer:
            img = renderer.render()
            assert isinstance(img, Image.Image)
            assert img.size == (100, 100)

    def test_render_bmp(self, sample_bmp: str):
        """Test rendering BMP format."""
        with ImageRenderer(sample_bmp) as renderer:
            img = renderer.render()
            assert isinstance(img, Image.Image)
            assert img.size == (100, 100)

    def test_render_gif(self, sample_gif: str):
        """Test rendering static GIF format."""
        with ImageRenderer(sample_gif) as renderer:
            img = renderer.render()
            assert isinstance(img, Image.Image)

    def test_is_svg_property(self, sample_svg: str, sample_png: str):
        """Test is_svg property."""
        with ImageRenderer(sample_svg) as renderer:
            assert renderer.is_svg is True

        with ImageRenderer(sample_png) as renderer:
            assert renderer.is_svg is False

    def test_is_animated_static_gif(self, sample_gif: str):
        """Test is_animated property for static GIF."""
        with ImageRenderer(sample_gif) as renderer:
            assert renderer.is_animated is False
            assert renderer.frame_count == 1

    def test_is_animated_animated_gif(self, sample_animated_gif: str):
        """Test is_animated property for animated GIF."""
        with ImageRenderer(sample_animated_gif) as renderer:
            assert renderer.is_animated is True
            assert renderer.frame_count == 3

    def test_render_animated_gif_frame(self, sample_animated_gif: str):
        """Test rendering specific frame of animated GIF."""
        with ImageRenderer(sample_animated_gif) as renderer:
            # Render each frame
            for frame in range(renderer.frame_count):
                img = renderer.render(frame=frame)
                assert isinstance(img, Image.Image)
                assert img.size == (50, 50)

    def test_get_frame_duration(self, sample_animated_gif: str):
        """Test getting frame duration for animated GIF."""
        with ImageRenderer(sample_animated_gif) as renderer:
            duration = renderer.get_frame_duration(0)
            assert duration == 100  # We set 100ms in fixture

    def test_get_frame_duration_static_image(self, sample_png: str):
        """Test getting frame duration for static image returns 0."""
        with ImageRenderer(sample_png) as renderer:
            duration = renderer.get_frame_duration(0)
            assert duration == 0

    def test_context_manager(self, sample_png: str):
        """Test context manager usage."""
        with ImageRenderer(sample_png) as renderer:
            img = renderer.render()
            assert img is not None
        # After exiting context, internal image should be closed

    def test_close_method(self, sample_png: str):
        """Test explicit close method."""
        renderer = ImageRenderer(sample_png)
        _ = renderer.render()  # Trigger lazy load
        renderer.close()
        # Image should be closed

    def test_render_svg(self, sample_svg: str):
        """Test rendering SVG file."""
        with ImageRenderer(sample_svg) as renderer:
            img = renderer.render()
            assert isinstance(img, Image.Image)
            # SVG is 100x100
            assert img.size[0] > 0
            assert img.size[1] > 0

    def test_render_svg_with_zoom(self, sample_svg: str):
        """Test rendering SVG with zoom."""
        with ImageRenderer(sample_svg) as renderer:
            base_img = renderer.render(zoom=1.0)
            base_size = base_img.size

            zoomed_img = renderer.render(zoom=2.0)
            assert zoomed_img.size[0] == base_size[0] * 2
            assert zoomed_img.size[1] == base_size[1] * 2
