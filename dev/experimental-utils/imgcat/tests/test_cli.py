"""Tests for imgcat.cli module."""

import pytest
from click.testing import CliRunner

from imgcat.cli import main, get_terminal_pixel_size, calculate_fit_size


class TestCLI:
    """Tests for CLI functions."""

    def test_main_with_single_file(self, sample_png: str):
        """Test CLI with single image file (help text)."""
        runner = CliRunner()
        # We can't test interactive mode, but we can test --help
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Display images" in result.output

    def test_main_with_nonexistent_file(self):
        """Test CLI with nonexistent file."""
        runner = CliRunner()
        result = runner.invoke(main, ["/nonexistent/file.png"])
        assert result.exit_code != 0

    def test_main_no_files_empty_directory(self, tmp_path, monkeypatch):
        """Test CLI without any files in empty directory."""
        monkeypatch.chdir(tmp_path)
        runner = CliRunner()
        result = runner.invoke(main, [])
        assert result.exit_code != 0
        assert "No image files found" in result.output

    def test_get_terminal_pixel_size(self):
        """Test terminal pixel size detection."""
        width, height = get_terminal_pixel_size()
        # Should return reasonable values
        assert width > 0
        assert height > 0

    def test_calculate_fit_size(self):
        """Test fit size calculation."""
        max_width, max_height = calculate_fit_size(0.5)
        assert max_width > 0
        assert max_height > 0

        # Smaller ratio should give smaller size
        max_width_small, max_height_small = calculate_fit_size(0.25)
        assert max_width_small <= max_width
        assert max_height_small <= max_height


class TestAnimationController:
    """Tests for animation controller."""

    def test_animation_controller_init(self):
        """Test AnimationController initialization."""
        from imgcat.animation import AnimationController

        controller = AnimationController(3, [100, 100, 100])
        assert controller.frame_count == 3
        assert controller.current_frame == 0
        assert controller.is_playing is True

    def test_animation_controller_toggle(self):
        """Test toggle_play_pause."""
        from imgcat.animation import AnimationController

        controller = AnimationController(3, [100, 100, 100])
        assert controller.is_playing is True

        controller.toggle_play_pause()
        assert controller.is_playing is False

        controller.toggle_play_pause()
        assert controller.is_playing is True

    def test_animation_controller_next_frame(self):
        """Test manual next frame."""
        from imgcat.animation import AnimationController

        controller = AnimationController(3, [100, 100, 100])
        assert controller.current_frame == 0

        controller.next_frame()
        assert controller.current_frame == 1

        controller.next_frame()
        assert controller.current_frame == 2

        # Should wrap around
        controller.next_frame()
        assert controller.current_frame == 0

    def test_animation_controller_prev_frame(self):
        """Test manual previous frame."""
        from imgcat.animation import AnimationController

        controller = AnimationController(3, [100, 100, 100])
        assert controller.current_frame == 0

        # Should wrap around to last frame
        controller.prev_frame()
        assert controller.current_frame == 2

        controller.prev_frame()
        assert controller.current_frame == 1

    def test_animation_controller_seek_frame(self):
        """Test seeking to specific frame."""
        from imgcat.animation import AnimationController

        controller = AnimationController(3, [100, 100, 100])

        controller.seek_frame(2)
        assert controller.current_frame == 2

        # Invalid frame should be ignored
        controller.seek_frame(10)
        assert controller.current_frame == 2

        controller.seek_frame(-1)
        assert controller.current_frame == 2


class TestKittyGraphics:
    """Tests for Kitty graphics protocol."""

    def test_kitty_encode_image(self, sample_png: str):
        """Test image encoding."""
        from PIL import Image
        from imgcat.kitty import KittyGraphics

        kitty = KittyGraphics()
        img = Image.new("RGB", (10, 10), color="red")
        encoded = kitty.encode_image(img)

        assert isinstance(encoded, str)
        assert len(encoded) > 0

    def test_kitty_display_image(self, sample_png: str):
        """Test display image command generation."""
        from PIL import Image
        from imgcat.kitty import KittyGraphics

        kitty = KittyGraphics()
        img = Image.new("RGB", (10, 10), color="red")
        command = kitty.display_image(img)

        assert isinstance(command, str)
        assert "\x1b_G" in command  # Kitty graphics escape

    def test_kitty_clear_screen(self):
        """Test clear screen command."""
        from imgcat.kitty import KittyGraphics

        kitty = KittyGraphics()
        command = kitty.clear_screen()

        assert isinstance(command, str)
        assert "\x1b_G" in command
