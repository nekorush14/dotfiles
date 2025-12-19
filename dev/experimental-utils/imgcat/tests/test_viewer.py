"""Tests for imgcat.viewer module."""

import pytest

from imgcat.viewer import ImageViewer


class TestImageViewer:
    """Tests for ImageViewer class."""

    def test_init_single_file(self, sample_png: str):
        """Test viewer initialization with single file."""
        viewer = ImageViewer([sample_png])
        assert viewer.total_files == 1
        assert viewer.current_file_index == 0
        viewer.close()

    def test_init_multiple_files(self, multiple_images: list[str]):
        """Test viewer initialization with multiple files."""
        viewer = ImageViewer(multiple_images)
        assert viewer.total_files == 5
        assert viewer.current_file_index == 0
        viewer.close()

    def test_init_with_zoom(self, sample_png: str):
        """Test viewer initialization with custom zoom."""
        viewer = ImageViewer([sample_png], initial_zoom=2.0)
        assert viewer.zoom_level == 2.0
        viewer.close()

    def test_next_file(self, multiple_images: list[str]):
        """Test navigating to next file."""
        viewer = ImageViewer(multiple_images)
        assert viewer.current_file_index == 0

        result = viewer.next_file()
        assert result is True
        assert viewer.current_file_index == 1

        viewer.close()

    def test_next_file_at_last(self, multiple_images: list[str]):
        """Test next_file at last file returns False."""
        viewer = ImageViewer(multiple_images)

        # Go to last file
        for _ in range(4):
            viewer.next_file()

        assert viewer.current_file_index == 4
        result = viewer.next_file()
        assert result is False
        assert viewer.current_file_index == 4

        viewer.close()

    def test_previous_file(self, multiple_images: list[str]):
        """Test navigating to previous file."""
        viewer = ImageViewer(multiple_images)
        viewer.next_file()
        viewer.next_file()
        assert viewer.current_file_index == 2

        result = viewer.previous_file()
        assert result is True
        assert viewer.current_file_index == 1

        viewer.close()

    def test_previous_file_at_first(self, sample_png: str):
        """Test previous_file at first file returns False."""
        viewer = ImageViewer([sample_png])
        result = viewer.previous_file()
        assert result is False
        assert viewer.current_file_index == 0
        viewer.close()

    def test_go_to_file(self, multiple_images: list[str]):
        """Test navigating to specific file by index."""
        viewer = ImageViewer(multiple_images)

        viewer.go_to_file(3)
        assert viewer.current_file_index == 2  # 0-indexed

        viewer.go_to_file(1)
        assert viewer.current_file_index == 0

        viewer.close()

    def test_go_to_file_invalid(self, multiple_images: list[str]):
        """Test go_to_file with invalid index."""
        viewer = ImageViewer(multiple_images)

        # Too large
        viewer.go_to_file(100)
        assert viewer.current_file_index == 4  # Clamps to last

        # Too small
        viewer.go_to_file(0)
        assert viewer.current_file_index == 0  # Clamps to first

        viewer.close()

    def test_go_to_first_file(self, multiple_images: list[str]):
        """Test navigating to first file."""
        viewer = ImageViewer(multiple_images)
        viewer.go_to_file(5)  # Go to last
        viewer.go_to_first_file()
        assert viewer.current_file_index == 0
        viewer.close()

    def test_go_to_last_file(self, multiple_images: list[str]):
        """Test navigating to last file."""
        viewer = ImageViewer(multiple_images)
        viewer.go_to_last_file()
        assert viewer.current_file_index == 4
        viewer.close()

    def test_zoom_in(self, sample_png: str):
        """Test zoom in with small (5%) and large (10%) steps."""
        viewer = ImageViewer([sample_png], initial_zoom=1.0)

        # Default (small) step: 5%
        result = viewer.zoom_in()
        assert result is True
        assert viewer.zoom_level == pytest.approx(1.05)

        # Large step: 10%
        result = viewer.zoom_in(large=True)
        assert result is True
        assert viewer.zoom_level == pytest.approx(1.15)

        viewer.close()

    def test_zoom_in_at_max(self, sample_png: str):
        """Test zoom in at maximum zoom returns False."""
        viewer = ImageViewer([sample_png], initial_zoom=4.0)

        result = viewer.zoom_in()
        assert result is False
        assert viewer.zoom_level == 4.0

        viewer.close()

    def test_zoom_out(self, sample_png: str):
        """Test zoom out with small (5%) and large (10%) steps."""
        viewer = ImageViewer([sample_png], initial_zoom=1.0)

        # Default (small) step: 5%
        result = viewer.zoom_out()
        assert result is True
        assert viewer.zoom_level == pytest.approx(0.95)

        # Large step: 10%
        result = viewer.zoom_out(large=True)
        assert result is True
        assert viewer.zoom_level == pytest.approx(0.85)

        viewer.close()

    def test_zoom_out_at_min(self, sample_png: str):
        """Test zoom out at minimum zoom returns False."""
        viewer = ImageViewer([sample_png], initial_zoom=0.25)

        result = viewer.zoom_out()
        assert result is False
        assert viewer.zoom_level == 0.25

        viewer.close()

    def test_set_zoom(self, sample_png: str):
        """Test setting zoom directly."""
        viewer = ImageViewer([sample_png])

        viewer.set_zoom(2.5)
        assert viewer.zoom_level == 2.5

        # Should clamp to max
        viewer.set_zoom(10.0)
        assert viewer.zoom_level == 4.0

        # Should clamp to min
        viewer.set_zoom(0.1)
        assert viewer.zoom_level == 0.25

        viewer.close()

    def test_reset_zoom(self, sample_png: str):
        """Test resetting zoom to 1.0."""
        viewer = ImageViewer([sample_png], initial_zoom=2.0)

        viewer.reset_zoom()
        assert viewer.zoom_level == 1.0

        viewer.close()

    def test_get_info(self, multiple_images: list[str]):
        """Test getting current viewer info."""
        viewer = ImageViewer(multiple_images, initial_zoom=1.5)
        viewer.next_file()  # Go to second file

        info = viewer.get_info()
        assert info["current_file"] == 2
        assert info["total_files"] == 5
        assert "image_1.png" in info["filename"]
        assert info["zoom"] == 1.5

        viewer.close()

    def test_get_info_animated_gif(self, sample_animated_gif: str):
        """Test get_info for animated GIF."""
        viewer = ImageViewer([sample_animated_gif])

        info = viewer.get_info()
        assert info["is_animated"] is True
        assert info["total_frames"] == 3
        assert info["current_frame"] == 1  # 1-indexed for display

        viewer.close()

    def test_display_current(self, sample_png: str):
        """Test displaying current image returns Kitty command."""
        viewer = ImageViewer([sample_png])

        command = viewer.display_current()
        assert isinstance(command, str)
        assert "\x1b_G" in command  # Kitty graphics escape

        viewer.close()

    def test_clear_display(self, sample_png: str):
        """Test clear display returns Kitty command."""
        viewer = ImageViewer([sample_png])

        command = viewer.clear_display()
        assert isinstance(command, str)
        assert "\x1b_G" in command

        viewer.close()

    def test_toggle_animation(self, sample_animated_gif: str):
        """Test toggling animation play/pause."""
        viewer = ImageViewer([sample_animated_gif])

        info = viewer.get_info()
        assert info["is_playing"] is True

        viewer.toggle_animation()
        info = viewer.get_info()
        assert info["is_playing"] is False

        viewer.toggle_animation()
        info = viewer.get_info()
        assert info["is_playing"] is True

        viewer.close()

    def test_toggle_animation_static_image(self, sample_png: str):
        """Test toggle_animation on static image does nothing."""
        viewer = ImageViewer([sample_png])

        # Should not raise
        viewer.toggle_animation()

        info = viewer.get_info()
        assert info["is_animated"] is False

        viewer.close()

    def test_context_manager(self, sample_png: str):
        """Test viewer as context manager."""
        with ImageViewer([sample_png]) as viewer:
            assert viewer.total_files == 1

    def test_update_animation(self, sample_animated_gif: str):
        """Test update_animation returns bool."""
        viewer = ImageViewer([sample_animated_gif])

        result = viewer.update_animation()
        # First call should return False (not enough time passed)
        assert isinstance(result, bool)

        viewer.close()

    def test_update_animation_static(self, sample_png: str):
        """Test update_animation for static image returns False."""
        viewer = ImageViewer([sample_png])

        result = viewer.update_animation()
        assert result is False

        viewer.close()

    def test_next_frame(self, sample_animated_gif: str):
        """Test manual next frame navigation."""
        viewer = ImageViewer([sample_animated_gif])

        initial_frame = viewer.get_info()["current_frame"]
        viewer.next_frame()
        new_frame = viewer.get_info()["current_frame"]

        assert new_frame == initial_frame + 1

        viewer.close()

    def test_prev_frame(self, sample_animated_gif: str):
        """Test manual previous frame navigation."""
        viewer = ImageViewer([sample_animated_gif])

        # Go to frame 2
        viewer.next_frame()
        viewer.prev_frame()

        assert viewer.get_info()["current_frame"] == 1

        viewer.close()
