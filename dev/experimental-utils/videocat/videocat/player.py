"""Video player module using mpv as backend.

This module provides a VideoPlayer class that controls mpv via IPC socket
for video playback with terminal-based controls.
"""

import json
import os
import socket
import subprocess
import tempfile
import time
from typing import Optional


class VideoPlayer:
    """Video player using mpv backend with IPC socket control."""

    def __init__(
        self,
        video_path: str,
        volume: int = 100,
    ):
        """Initialize the video player.

        Args:
            video_path: Path to the video file
            volume: Initial volume (0-100)
        """
        self._socket_path = f"/tmp/mpv-videocat-{os.getpid()}.sock"
        if os.path.exists(self._socket_path):
            os.remove(self._socket_path)

        self._process = subprocess.Popen(
            [
                "mpv",
                f"--input-ipc-server={self._socket_path}",
                "--no-terminal",
                "--no-input-default-bindings",
                "--no-osc",
                "--keep-open=yes",
                f"--volume={volume}",
                video_path,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        self._socket: Optional[socket.socket] = None
        self._recv_buffer = ""  # Buffer for receiving data
        self._volume = volume
        self._muted = False
        self._request_id = 0

        # Wait for socket and connect
        self._connect_socket()

    def _connect_socket(self, timeout: float = 5.0) -> None:
        """Connect to mpv IPC socket.

        Args:
            timeout: Maximum time to wait for socket
        """
        start = time.time()
        while time.time() - start < timeout:
            if os.path.exists(self._socket_path):
                try:
                    self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    self._socket.connect(self._socket_path)
                    self._socket.settimeout(0.5)
                    return
                except (ConnectionRefusedError, FileNotFoundError):
                    if self._socket:
                        self._socket.close()
                        self._socket = None
            time.sleep(0.05)
        raise ConnectionError("Failed to connect to mpv IPC socket")

    def _recv_line(self) -> Optional[str]:
        """Receive a complete line from the socket.

        Returns:
            A complete line (without newline) or None on error
        """
        if not self._socket:
            return None

        try:
            while "\n" not in self._recv_buffer:
                data = self._socket.recv(4096)
                if not data:
                    return None
                self._recv_buffer += data.decode()

            line, self._recv_buffer = self._recv_buffer.split("\n", 1)
            return line
        except (socket.timeout, OSError):
            return None

    def _send_command(self, command: list) -> Optional[dict]:
        """Send command to mpv via IPC.

        Args:
            command: Command list to send

        Returns:
            Response dict or None on error
        """
        if not self._socket:
            return None
        try:
            self._request_id += 1
            msg = json.dumps({"command": command, "request_id": self._request_id}) + "\n"
            self._socket.sendall(msg.encode())

            # Read responses until we get one with our request_id
            while True:
                line = self._recv_line()
                if line is None:
                    return None
                try:
                    response = json.loads(line)
                    # Skip event messages, wait for response with our request_id
                    if response.get("request_id") == self._request_id:
                        return response
                    # Also accept responses without request_id for backwards compat
                    if "request_id" not in response and "event" not in response:
                        return response
                except json.JSONDecodeError:
                    continue
        except (BrokenPipeError, OSError):
            return None

    def _get_property(self, name: str) -> Optional[any]:
        """Get property value from mpv.

        Args:
            name: Property name

        Returns:
            Property value or None
        """
        result = self._send_command(["get_property", name])
        if result and result.get("error") == "success":
            return result.get("data")
        return None

    def _set_property(self, name: str, value: any) -> bool:
        """Set property value in mpv.

        Args:
            name: Property name
            value: Property value

        Returns:
            True on success
        """
        result = self._send_command(["set_property", name, value])
        return result is not None and result.get("error") == "success"

    @property
    def duration(self) -> Optional[float]:
        """Get video duration in seconds."""
        return self._get_property("duration")

    @property
    def position(self) -> float:
        """Get current playback position in seconds."""
        pos = self._get_property("time-pos")
        return pos if pos is not None else 0.0

    @property
    def width(self) -> int:
        """Get video width in pixels."""
        return self._get_property("width") or 0

    @property
    def height(self) -> int:
        """Get video height in pixels."""
        return self._get_property("height") or 0

    @property
    def is_paused(self) -> bool:
        """Check if playback is paused."""
        return self._get_property("pause") or False

    @property
    def is_muted(self) -> bool:
        """Check if audio is muted."""
        return self._get_property("mute") or False

    @property
    def volume(self) -> int:
        """Get current volume level (0-100)."""
        vol = self._get_property("volume")
        return int(vol) if vol is not None else self._volume

    @property
    def is_playing(self) -> bool:
        """Check if video is currently playing (not finished)."""
        return self._get_property("time-pos") is not None

    @property
    def is_idle(self) -> bool:
        """Check if player is idle (finished or not started)."""
        return self._get_property("core-idle") or False

    def wait_until_playing(self, timeout: float = 5.0) -> bool:
        """Wait until video starts playing.

        Args:
            timeout: Maximum time to wait in seconds

        Returns:
            True if video started, False if timeout
        """
        start = time.time()
        while time.time() - start < timeout:
            if self._get_property("time-pos") is not None:
                return True
            time.sleep(0.05)
        return False

    def toggle_pause(self) -> None:
        """Toggle pause state."""
        current = self.is_paused
        self._set_property("pause", not current)

    def seek(self, seconds: float) -> None:
        """Seek relative to current position.

        Args:
            seconds: Seconds to seek (positive = forward, negative = backward)
        """
        self._send_command(["seek", seconds, "relative"])

    def seek_absolute(self, seconds: float) -> None:
        """Seek to absolute position.

        Args:
            seconds: Target position in seconds
        """
        self._send_command(["seek", seconds, "absolute"])

    def set_volume(self, level: int) -> None:
        """Set volume level.

        Args:
            level: Volume level (0-100), clamped to valid range
        """
        level = max(0, min(100, level))
        self._set_property("volume", level)
        self._volume = level

    def toggle_mute(self) -> None:
        """Toggle mute state."""
        current = self.is_muted
        self._set_property("mute", not current)

    def frame_step(self) -> None:
        """Step forward one frame."""
        self._send_command(["frame-step"])

    def frame_back_step(self) -> None:
        """Step backward one frame."""
        self._send_command(["frame-back-step"])

    @property
    def is_loop(self) -> bool:
        """Check if loop is enabled."""
        loop = self._get_property("loop-file")
        return loop == "inf" or loop is True

    def toggle_loop(self) -> None:
        """Toggle loop mode."""
        if self.is_loop:
            self._set_property("loop-file", "no")
        else:
            self._set_property("loop-file", "inf")

    @property
    def zoom(self) -> float:
        """Get current zoom level."""
        zoom = self._get_property("video-zoom")
        return zoom if zoom is not None else 0.0

    def set_zoom(self, level: float) -> None:
        """Set zoom level.

        Args:
            level: Zoom level (0.0 = normal, positive = zoom in, negative = zoom out)
        """
        self._set_property("video-zoom", level)

    def zoom_in(self, amount: float = 0.1) -> None:
        """Zoom in.

        Args:
            amount: Amount to zoom in
        """
        current = self.zoom
        self.set_zoom(current + amount)

    def zoom_out(self, amount: float = 0.1) -> None:
        """Zoom out.

        Args:
            amount: Amount to zoom out
        """
        current = self.zoom
        self.set_zoom(current - amount)

    def reset_zoom(self) -> None:
        """Reset zoom to normal."""
        self.set_zoom(0.0)

    @property
    def eof_reached(self) -> bool:
        """Check if end of file has been reached."""
        return self._get_property("eof-reached") or False

    def close(self) -> None:
        """Close the player and release resources."""
        if self._socket:
            try:
                self._send_command(["quit"])
            except Exception:
                pass
            self._socket.close()
            self._socket = None

        if self._process:
            try:
                self._process.terminate()
                self._process.wait(timeout=2)
            except Exception:
                self._process.kill()

        if os.path.exists(self._socket_path):
            try:
                os.remove(self._socket_path)
            except Exception:
                pass

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
