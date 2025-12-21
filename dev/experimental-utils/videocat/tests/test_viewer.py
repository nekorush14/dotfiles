"""Tests for VideoViewer class."""

import pytest
from unittest.mock import MagicMock, patch
from PIL import Image


@pytest.fixture
def mock_video_player():
    """Create a mock VideoPlayer."""
    player = MagicMock()
    player.duration = 60.0
    player.position = 0.0
    player.volume = 100
    player.is_paused = False
    player.is_muted = False
    player.is_playing = True
    player.is_idle = False
    player.width = 1920
    player.height = 1080
    player.wait_until_playing.return_value = True
    return player


class TestVideoViewer:
    """Tests for VideoViewer initialization."""

    def test_viewer_initialization(self, mock_video_player):
        """Test that VideoViewer initializes correctly."""
        with patch("videocat.viewer.VideoPlayer", return_value=mock_video_player):
            from videocat.viewer import VideoViewer

            viewer = VideoViewer("test.mp4")
            assert viewer is not None


class TestVideoViewerInfo:
    """Tests for VideoViewer info methods."""

    def test_get_playback_info(self, mock_video_player):
        """Test getting playback info."""
        with patch("videocat.viewer.VideoPlayer", return_value=mock_video_player):
            from videocat.viewer import VideoViewer

            viewer = VideoViewer("test.mp4")
            info = viewer.get_playback_info()

            assert "position" in info
            assert "duration" in info
            assert "volume" in info
            assert "paused" in info
            assert "muted" in info

    def test_format_time(self, mock_video_player):
        """Test time formatting."""
        with patch("videocat.viewer.VideoPlayer", return_value=mock_video_player):
            from videocat.viewer import VideoViewer

            viewer = VideoViewer("test.mp4")

            assert viewer.format_time(0) == "0:00"
            assert viewer.format_time(65) == "1:05"
            assert viewer.format_time(3661) == "1:01:01"


class TestVideoViewerControls:
    """Tests for VideoViewer playback controls."""

    def test_toggle_pause(self, mock_video_player):
        """Test pause toggle."""
        with patch("videocat.viewer.VideoPlayer", return_value=mock_video_player):
            from videocat.viewer import VideoViewer

            viewer = VideoViewer("test.mp4")
            viewer.toggle_pause()
            mock_video_player.toggle_pause.assert_called_once()

    def test_seek_forward(self, mock_video_player):
        """Test seeking forward."""
        with patch("videocat.viewer.VideoPlayer", return_value=mock_video_player):
            from videocat.viewer import VideoViewer

            viewer = VideoViewer("test.mp4")
            viewer.seek_forward(5)
            mock_video_player.seek.assert_called_with(5)

    def test_seek_backward(self, mock_video_player):
        """Test seeking backward."""
        with patch("videocat.viewer.VideoPlayer", return_value=mock_video_player):
            from videocat.viewer import VideoViewer

            viewer = VideoViewer("test.mp4")
            viewer.seek_backward(5)
            mock_video_player.seek.assert_called_with(-5)

    def test_seek_absolute(self, mock_video_player):
        """Test seeking to absolute position."""
        with patch("videocat.viewer.VideoPlayer", return_value=mock_video_player):
            from videocat.viewer import VideoViewer

            viewer = VideoViewer("test.mp4")
            viewer.seek_absolute(30)
            mock_video_player.seek_absolute.assert_called_with(30)

    def test_volume_up(self, mock_video_player):
        """Test volume up."""
        with patch("videocat.viewer.VideoPlayer", return_value=mock_video_player):
            from videocat.viewer import VideoViewer

            viewer = VideoViewer("test.mp4")
            viewer.volume_up(5)
            mock_video_player.set_volume.assert_called()

    def test_volume_down(self, mock_video_player):
        """Test volume down."""
        with patch("videocat.viewer.VideoPlayer", return_value=mock_video_player):
            from videocat.viewer import VideoViewer

            viewer = VideoViewer("test.mp4")
            viewer.volume_down(5)
            mock_video_player.set_volume.assert_called()

    def test_toggle_mute(self, mock_video_player):
        """Test mute toggle."""
        with patch("videocat.viewer.VideoPlayer", return_value=mock_video_player):
            from videocat.viewer import VideoViewer

            viewer = VideoViewer("test.mp4")
            viewer.toggle_mute()
            mock_video_player.toggle_mute.assert_called_once()


class TestVideoViewerLifecycle:
    """Tests for VideoViewer lifecycle."""

    def test_close(self, mock_video_player):
        """Test closing viewer."""
        with patch("videocat.viewer.VideoPlayer", return_value=mock_video_player):
            from videocat.viewer import VideoViewer

            viewer = VideoViewer("test.mp4")
            viewer.close()
            mock_video_player.close.assert_called_once()

    def test_is_playing(self, mock_video_player):
        """Test is_playing property."""
        with patch("videocat.viewer.VideoPlayer", return_value=mock_video_player):
            from videocat.viewer import VideoViewer

            viewer = VideoViewer("test.mp4")
            assert viewer.is_playing is True

    def test_wait_until_playing(self, mock_video_player):
        """Test wait_until_playing method."""
        with patch("videocat.viewer.VideoPlayer", return_value=mock_video_player):
            from videocat.viewer import VideoViewer

            viewer = VideoViewer("test.mp4")
            result = viewer.wait_until_playing()
            assert result is True
            mock_video_player.wait_until_playing.assert_called_once()
