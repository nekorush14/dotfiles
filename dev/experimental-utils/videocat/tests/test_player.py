"""Tests for VideoPlayer class."""

import pytest
from unittest.mock import MagicMock, patch


class TestVideoPlayer:
    """Tests for VideoPlayer initialization and basic functionality."""

    def test_player_initialization(self, mock_mpv_player, temp_video_path):
        """Test that VideoPlayer initializes correctly."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        assert player is not None

    def test_player_has_duration(self, mock_mpv_player, temp_video_path):
        """Test that VideoPlayer exposes video duration."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        assert player.duration == 60.0

    def test_player_has_current_position(self, mock_mpv_player, temp_video_path):
        """Test that VideoPlayer tracks current position."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        assert player.position == 0.0

    def test_player_has_video_dimensions(self, mock_mpv_player, temp_video_path):
        """Test that VideoPlayer exposes video dimensions."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        assert player.width == 1920
        assert player.height == 1080


class TestVideoPlayerPlayback:
    """Tests for VideoPlayer playback controls."""

    def test_toggle_pause(self, mock_mpv_player, temp_video_path):
        """Test pause toggle functionality."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        initial_pause = player.is_paused
        player.toggle_pause()
        assert player.is_paused != initial_pause

    def test_seek_forward(self, mock_mpv_player, temp_video_path):
        """Test seeking forward in video."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        player.seek(5.0)  # Seek 5 seconds forward
        # Command is sent via IPC
        assert mock_mpv_player._last_command["command"] == ["seek", 5.0, "relative"]

    def test_seek_backward(self, mock_mpv_player, temp_video_path):
        """Test seeking backward in video."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        player.seek(-5.0)  # Seek 5 seconds backward
        assert mock_mpv_player._last_command["command"] == ["seek", -5.0, "relative"]

    def test_seek_absolute(self, mock_mpv_player, temp_video_path):
        """Test seeking to absolute position."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        player.seek_absolute(30.0)  # Seek to 30 seconds
        assert mock_mpv_player._last_command["command"] == ["seek", 30.0, "absolute"]


class TestVideoPlayerVolume:
    """Tests for VideoPlayer volume controls."""

    def test_get_volume(self, mock_mpv_player, temp_video_path):
        """Test getting current volume."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        assert player.volume == 100

    def test_set_volume(self, mock_mpv_player, temp_video_path):
        """Test setting volume."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        player.set_volume(50)
        assert mock_mpv_player._properties["volume"] == 50

    def test_volume_clamp_max(self, mock_mpv_player, temp_video_path):
        """Test that volume is clamped to max 100."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        player.set_volume(150)
        assert mock_mpv_player._properties["volume"] == 100

    def test_volume_clamp_min(self, mock_mpv_player, temp_video_path):
        """Test that volume is clamped to min 0."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        player.set_volume(-10)
        assert mock_mpv_player._properties["volume"] == 0

    def test_toggle_mute(self, mock_mpv_player, temp_video_path):
        """Test mute toggle functionality."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        initial_mute = player.is_muted
        player.toggle_mute()
        assert player.is_muted != initial_mute


class TestVideoPlayerLifecycle:
    """Tests for VideoPlayer lifecycle management."""

    def test_close(self, mock_mpv_player, temp_video_path):
        """Test closing the player."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        player.close()
        assert not mock_mpv_player._connected

    def test_is_playing(self, mock_mpv_player, temp_video_path):
        """Test checking if video is playing."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        mock_mpv_player._properties["time-pos"] = 10.0
        assert player.is_playing is True

    def test_is_finished(self, mock_mpv_player, temp_video_path):
        """Test checking if video has finished."""
        from videocat.player import VideoPlayer

        player = VideoPlayer(str(temp_video_path))
        mock_mpv_player._properties["time-pos"] = None  # mpv returns None when finished
        assert player.is_playing is False
