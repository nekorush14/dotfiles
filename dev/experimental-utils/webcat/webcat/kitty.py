"""Kitty graphics protocol implementation for terminal image display.

This module implements the Kitty graphics protocol for displaying images
in terminal emulators that support it (like Ghostty, Kitty, etc.).

Reference: https://sw.kovidgoyal.net/kitty/graphics-protocol/
"""

import base64
from io import BytesIO
from typing import Optional
from PIL import Image


# Maximum chunk size for Kitty protocol (4096 bytes is the limit)
CHUNK_SIZE = 4096


class KittyGraphics:
    """Handle Kitty graphics protocol for terminal image display."""

    def __init__(self):
        """Initialize KittyGraphics handler."""
        pass

    def encode_image(self, image: Image.Image, format: str = "PNG") -> str:
        """Encode PIL Image to base64 string for Kitty protocol.

        Args:
            image: PIL Image object to encode
            format: Image format to use (default: PNG)

        Returns:
            Base64 encoded string of the image data
        """
        buffer = BytesIO()
        image.save(buffer, format=format)
        buffer.seek(0)
        encoded = base64.b64encode(buffer.read()).decode("ascii")
        return encoded

    def _serialize_command(self, control: dict, payload: str = "") -> str:
        """Serialize a Kitty graphics command.

        Args:
            control: Dictionary of control parameters
            payload: Optional payload data

        Returns:
            Escape sequence string
        """
        control_str = ",".join(f"{k}={v}" for k, v in control.items())
        return f"\x1b_G{control_str};{payload}\x1b\\"

    def display_image(
        self,
        image: Image.Image,
        delete_previous: bool = True,
    ) -> str:
        """Display a PIL Image in the terminal using Kitty protocol.

        For large images, data is sent in chunks as required by the protocol.

        Args:
            image: PIL Image to display
            delete_previous: Whether to delete previous images

        Returns:
            Kitty protocol command string ready to print
        """
        # Encode image to base64
        encoded = self.encode_image(image)

        commands = []

        # Delete previous images if requested
        if delete_previous:
            commands.append(self._serialize_command({"a": "d", "d": "A"}))

        # Send image data in chunks
        # For data larger than CHUNK_SIZE, use chunked transmission
        if len(encoded) <= CHUNK_SIZE:
            # Small image - send in one command
            # a=T: transmit and display, f=100: PNG format
            control = {"a": "T", "f": "100"}
            commands.append(self._serialize_command(control, encoded))
        else:
            # Large image - send in chunks
            # First chunk: a=t (transmit), m=1 (more data coming), q=2 (suppress response)
            # Middle chunks: m=1
            # Last chunk: m=0, q=2, and we need to display after transmission
            chunks = [
                encoded[i : i + CHUNK_SIZE]
                for i in range(0, len(encoded), CHUNK_SIZE)
            ]

            for i, chunk in enumerate(chunks):
                is_first = i == 0
                is_last = i == len(chunks) - 1

                control = {}
                if is_first:
                    # First chunk: specify format, action, and assign an ID
                    control["a"] = "t"  # transmit (store, don't display yet)
                    control["f"] = "100"  # PNG format
                    control["i"] = "1"  # image ID
                    control["q"] = "2"  # suppress responses

                if is_last:
                    control["m"] = "0"  # no more data
                else:
                    control["m"] = "1"  # more data coming

                commands.append(self._serialize_command(control, chunk))

            # After all chunks sent, display the image with a=p (put/display)
            commands.append(self._serialize_command({"a": "p", "i": "1", "q": "2"}))

        return "".join(commands)

    def create_display_command(
        self,
        encoded_data: str,
        action: str = "t",
        format: int = 100,
        delete: bool = False,
    ) -> str:
        """Create Kitty graphics protocol command string (legacy method).

        Note: For large images, use display_image() instead which handles chunking.

        Args:
            encoded_data: Base64 encoded image data
            action: Action to perform (t=transmit and display, default)
            format: Image format (100=PNG)
            delete: Whether to delete previous images

        Returns:
            Complete Kitty protocol escape sequence
        """
        control = {"a": action, "f": str(format)}
        if delete:
            control["d"] = "A"
        return self._serialize_command(control, encoded_data)

    def clear_screen(self) -> str:
        """Create command to clear all images from screen.

        Returns:
            Kitty protocol command to delete all images
        """
        # Delete all images with action 'd'
        command = "\x1b_Ga=d\x1b\\"
        return command
