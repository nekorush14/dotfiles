"""Pytest configuration and fixtures for videocat tests."""

import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from PIL import Image


@pytest.fixture
def sample_frame():
    """Create a sample PIL Image for testing."""
    return Image.new("RGB", (640, 480), color=(128, 128, 128))


class MockSocket:
    """Mock socket for IPC communication."""

    def __init__(self):
        self._properties = {
            "duration": 60.0,
            "time-pos": 0.0,
            "width": 1920,
            "height": 1080,
            "pause": False,
            "mute": False,
            "volume": 100,
            "core-idle": False,
        }
        self._connected = False
        self._last_command = None
        self._pending_response = None

    def connect(self, path):
        self._connected = True

    def settimeout(self, timeout):
        pass

    def sendall(self, data):
        self._last_command = json.loads(data.decode())
        # Prepare response with request_id and newline
        cmd = self._last_command.get("command", [])
        request_id = self._last_command.get("request_id", 0)

        if cmd[0] == "get_property":
            prop_name = cmd[1]
            value = self._properties.get(prop_name)
            response = {"data": value, "error": "success", "request_id": request_id}
        elif cmd[0] == "set_property":
            prop_name = cmd[1]
            value = cmd[2]
            self._properties[prop_name] = value
            response = {"error": "success", "request_id": request_id}
        elif cmd[0] == "seek":
            response = {"error": "success", "request_id": request_id}
        elif cmd[0] == "quit":
            response = {"error": "success", "request_id": request_id}
        else:
            response = {"error": "success", "request_id": request_id}

        self._pending_response = json.dumps(response) + "\n"

    def recv(self, size):
        if self._pending_response:
            response = self._pending_response.encode()
            self._pending_response = None
            return response
        return b""

    def close(self):
        self._connected = False


@pytest.fixture
def mock_mpv_player():
    """Create a mock mpv IPC player for testing."""
    mock_socket = MockSocket()
    mock_process = MagicMock()
    mock_process.terminate = MagicMock()
    mock_process.wait = MagicMock()
    mock_process.kill = MagicMock()

    with patch("videocat.player.subprocess.Popen", return_value=mock_process):
        with patch("videocat.player.socket.socket", return_value=mock_socket):
            with patch("videocat.player.os.path.exists", return_value=True):
                with patch("videocat.player.os.remove"):
                    yield mock_socket


@pytest.fixture
def temp_video_path(tmp_path):
    """Create a temporary path for video file (doesn't create actual video)."""
    video_path = tmp_path / "test_video.mp4"
    video_path.touch()
    return video_path
