"""Video viewer module for terminal control.

This module provides the VideoViewer class that wraps VideoPlayer
and provides a terminal-based control interface.
"""

from typing import Optional
from .player import VideoPlayer


class VideoViewer:
    """Video viewer with terminal-based control interface."""

    def __init__(
        self,
        video_path: str,
        volume: int = 100,
    ):
        """Initialize the video viewer.

        Args:
            video_path: Path to the video file
            volume: Initial volume (0-100)
        """
        self._player = VideoPlayer(video_path, volume=volume)

    @property
    def is_playing(self) -> bool:
        """Check if video is playing."""
        return self._player.is_playing

    @property
    def is_idle(self) -> bool:
        """Check if player is idle."""
        return self._player.is_idle

    @property
    def is_paused(self) -> bool:
        """Check if video is paused."""
        return self._player.is_paused

    def wait_until_playing(self, timeout: float = 5.0) -> bool:
        """Wait until video starts playing."""
        return self._player.wait_until_playing(timeout)

    def get_playback_info(self) -> dict:
        """Get current playback information.

        Returns:
            Dictionary with playback info
        """
        return {
            "position": self._player.position,
            "duration": self._player.duration,
            "volume": self._player.volume,
            "paused": self._player.is_paused,
            "muted": self._player.is_muted,
            "loop": self._player.is_loop,
            "zoom": self._player.zoom,
        }

    def format_time(self, seconds: float) -> str:
        """Format seconds as human-readable time string.

        Args:
            seconds: Time in seconds

        Returns:
            Formatted time string (e.g., "1:05" or "1:01:01")
        """
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"

    def toggle_pause(self) -> None:
        """Toggle pause state."""
        self._player.toggle_pause()

    def seek_forward(self, seconds: float = 5.0) -> None:
        """Seek forward in video.

        Args:
            seconds: Seconds to seek forward
        """
        self._player.seek(seconds)

    def seek_backward(self, seconds: float = 5.0) -> None:
        """Seek backward in video.

        Args:
            seconds: Seconds to seek backward
        """
        self._player.seek(-seconds)

    def seek_absolute(self, seconds: float) -> None:
        """Seek to absolute position.

        Args:
            seconds: Target position in seconds
        """
        self._player.seek_absolute(seconds)

    def volume_up(self, amount: int = 5) -> None:
        """Increase volume.

        Args:
            amount: Amount to increase volume
        """
        current = self._player.volume
        self._player.set_volume(current + amount)

    def volume_down(self, amount: int = 5) -> None:
        """Decrease volume.

        Args:
            amount: Amount to decrease volume
        """
        current = self._player.volume
        self._player.set_volume(current - amount)

    def toggle_mute(self) -> None:
        """Toggle mute state."""
        self._player.toggle_mute()

    def frame_step(self) -> None:
        """Step forward one frame."""
        self._player.frame_step()

    def frame_back_step(self) -> None:
        """Step backward one frame."""
        self._player.frame_back_step()

    @property
    def is_loop(self) -> bool:
        """Check if loop is enabled."""
        return self._player.is_loop

    def toggle_loop(self) -> None:
        """Toggle loop mode."""
        self._player.toggle_loop()

    @property
    def zoom(self) -> float:
        """Get current zoom level."""
        return self._player.zoom

    def zoom_in(self, amount: float = 0.1) -> None:
        """Zoom in."""
        self._player.zoom_in(amount)

    def zoom_out(self, amount: float = 0.1) -> None:
        """Zoom out."""
        self._player.zoom_out(amount)

    def reset_zoom(self) -> None:
        """Reset zoom to normal."""
        self._player.reset_zoom()

    @property
    def eof_reached(self) -> bool:
        """Check if end of file has been reached."""
        return self._player.eof_reached

    def close(self) -> None:
        """Close the viewer and release resources."""
        self._player.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
