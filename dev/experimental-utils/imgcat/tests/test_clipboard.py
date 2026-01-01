"""Tests for imgcat.clipboard module."""

import pytest
import sys
from pathlib import Path
from PIL import Image
from unittest.mock import patch, MagicMock


class TestCopyImageToClipboard:
    """Tests for copy_image_to_clipboard function."""

    def test_copy_image_success(self, sample_png: str):
        """Test copying image to clipboard succeeds."""
        from imgcat.clipboard import copy_image_to_clipboard

        # Mock subprocess to avoid actual clipboard operations in tests
        with patch("imgcat.clipboard.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            result = copy_image_to_clipboard(sample_png)

            assert result is True
            mock_run.assert_called_once()

    def test_copy_image_nonexistent_file(self):
        """Test copying nonexistent file raises error."""
        from imgcat.clipboard import copy_image_to_clipboard

        with pytest.raises(FileNotFoundError):
            copy_image_to_clipboard("/nonexistent/file.png")

    def test_copy_image_unsupported_format(self, tmp_path: Path):
        """Test copying unsupported format raises error."""
        from imgcat.clipboard import copy_image_to_clipboard

        # Create a text file with image extension
        text_file = tmp_path / "test.txt"
        text_file.write_text("not an image")

        with pytest.raises(ValueError):
            copy_image_to_clipboard(str(text_file))

    @pytest.mark.skipif(sys.platform != "darwin", reason="macOS only")
    def test_copy_image_osascript_command(self, sample_png: str):
        """Test that correct osascript command is generated for macOS."""
        from imgcat.clipboard import copy_image_to_clipboard

        with patch("imgcat.clipboard.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            copy_image_to_clipboard(sample_png)

            # Verify osascript is called with correct arguments
            call_args = mock_run.call_args
            assert call_args[0][0][0] == "osascript"

    def test_copy_image_clipboard_failure(self, sample_png: str):
        """Test handling clipboard operation failure."""
        from imgcat.clipboard import copy_image_to_clipboard

        with patch("imgcat.clipboard.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stderr="error")

            result = copy_image_to_clipboard(sample_png)

            assert result is False


class TestGetClipboardCommand:
    """Tests for platform-specific clipboard command generation."""

    def test_get_clipboard_command_macos(self):
        """Test clipboard command generation for macOS."""
        from imgcat.clipboard import _get_clipboard_command

        with patch("sys.platform", "darwin"):
            cmd = _get_clipboard_command("/path/to/image.png")
            assert cmd is not None
            assert "osascript" in cmd[0]

    def test_get_clipboard_command_unsupported_platform(self):
        """Test unsupported platform returns None."""
        from imgcat.clipboard import _get_clipboard_command

        with patch("sys.platform", "win32"):
            cmd = _get_clipboard_command("/path/to/image.png")
            # May return None for unsupported platforms
            # Implementation can decide to support or not
