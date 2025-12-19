"""Animation controller for GIF playback.

This module provides animation timing and frame management
for animated GIF images.
"""

import time


class AnimationController:
    """Controller for GIF animation playback."""

    def __init__(self, frame_count: int, frame_durations: list[int]):
        """Initialize the animation controller.

        Args:
            frame_count: Total number of frames
            frame_durations: List of frame durations in milliseconds
        """
        self.frame_count = frame_count
        self.frame_durations = frame_durations
        self.current_frame = 0
        self.is_playing = True
        self._last_frame_time = time.time()

    def update(self) -> bool:
        """Update animation timer and advance frame if needed.

        Returns:
            True if frame changed, False otherwise
        """
        if not self.is_playing:
            return False

        current_time = time.time()
        elapsed_ms = (current_time - self._last_frame_time) * 1000

        # Check if we should advance to next frame
        if elapsed_ms >= self.frame_durations[self.current_frame]:
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self._last_frame_time = current_time
            return True

        return False

    def toggle_play_pause(self) -> None:
        """Toggle between play and pause states."""
        self.is_playing = not self.is_playing
        if self.is_playing:
            # Reset timer when resuming
            self._last_frame_time = time.time()

    def next_frame(self) -> None:
        """Manually advance to next frame."""
        self.current_frame = (self.current_frame + 1) % self.frame_count
        self._last_frame_time = time.time()

    def prev_frame(self) -> None:
        """Manually go to previous frame."""
        self.current_frame = (self.current_frame - 1) % self.frame_count
        self._last_frame_time = time.time()

    def seek_frame(self, frame: int) -> None:
        """Jump to a specific frame.

        Args:
            frame: Frame number (0-indexed)
        """
        if 0 <= frame < self.frame_count:
            self.current_frame = frame
            self._last_frame_time = time.time()
