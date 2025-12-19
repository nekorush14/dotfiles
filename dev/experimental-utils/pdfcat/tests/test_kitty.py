"""Tests for Kitty graphics protocol implementation."""

import pytest
from io import BytesIO
from PIL import Image


class TestKittyProtocol:
    """Test cases for Kitty graphics protocol encoding."""

    def test_encode_image_to_base64(self):
        """Test encoding an image to base64 for Kitty protocol."""
        from pdfcat.kitty import KittyGraphics

        # Create a simple test image
        img = Image.new("RGB", (100, 100), color="red")
        kitty = KittyGraphics()

        # Should return base64 encoded PNG data
        encoded = kitty.encode_image(img)
        assert isinstance(encoded, str)
        assert len(encoded) > 0

    def test_create_display_command(self):
        """Test creating Kitty graphics display command."""
        from pdfcat.kitty import KittyGraphics

        kitty = KittyGraphics()
        encoded_data = "dGVzdGRhdGE="  # base64 test data

        # Should return proper Kitty protocol escape sequence
        command = kitty.create_display_command(encoded_data)
        assert isinstance(command, str)
        assert command.startswith("\x1b_G")  # Kitty graphics escape sequence
        assert "dGVzdGRhdGE=" in command
        assert command.endswith("\x1b\\")  # Kitty graphics terminator

    def test_display_image(self):
        """Test displaying an image using Kitty protocol."""
        from pdfcat.kitty import KittyGraphics

        img = Image.new("RGB", (100, 100), color="blue")
        kitty = KittyGraphics()

        # Should return the complete command string
        result = kitty.display_image(img)
        assert isinstance(result, str)
        assert result.startswith("\x1b_G")
        assert result.endswith("\x1b\\")

    def test_clear_screen(self):
        """Test clearing images from screen."""
        from pdfcat.kitty import KittyGraphics

        kitty = KittyGraphics()

        # Should return proper clear command
        command = kitty.clear_screen()
        assert isinstance(command, str)
        assert "\x1b_Ga=d" in command  # Delete action

    def test_encode_image_with_format(self):
        """Test encoding image with specific format."""
        from pdfcat.kitty import KittyGraphics

        img = Image.new("RGB", (50, 50), color="green")
        kitty = KittyGraphics()

        # Should support PNG format
        encoded_png = kitty.encode_image(img, format="PNG")
        assert isinstance(encoded_png, str)
        assert len(encoded_png) > 0
