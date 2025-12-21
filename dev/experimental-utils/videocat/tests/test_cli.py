"""Tests for CLI module."""

import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch


class TestCLI:
    """Tests for CLI entry point."""

    def test_cli_help(self):
        """Test CLI help message."""
        from videocat.cli import main

        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "video" in result.output.lower() or "VIDEO_FILE" in result.output

    def test_cli_version(self):
        """Test CLI version option."""
        from videocat.cli import main

        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_cli_missing_file(self):
        """Test CLI with missing file."""
        from videocat.cli import main

        runner = CliRunner()
        result = runner.invoke(main, ["nonexistent.mp4"])
        assert result.exit_code != 0


class TestTimeFormatting:
    """Tests for time formatting functions."""

    def test_format_time_seconds(self):
        """Test formatting seconds."""
        from videocat.cli import format_time

        assert format_time(0) == "0:00"
        assert format_time(5) == "0:05"
        assert format_time(59) == "0:59"

    def test_format_time_minutes(self):
        """Test formatting minutes."""
        from videocat.cli import format_time

        assert format_time(60) == "1:00"
        assert format_time(65) == "1:05"
        assert format_time(125) == "2:05"

    def test_format_time_hours(self):
        """Test formatting hours."""
        from videocat.cli import format_time

        assert format_time(3600) == "1:00:00"
        assert format_time(3661) == "1:01:01"
        assert format_time(7325) == "2:02:05"


class TestStatusDisplay:
    """Tests for status display functions."""

    def test_format_status_normal(self):
        """Test status formatting in normal mode."""
        from videocat.cli import format_status

        status = format_status(
            mode="NORMAL",
            position=65.0,
            duration=120.0,
            volume=80,
            paused=False,
            muted=False,
        )

        assert "NORMAL" in status
        assert "1:05" in status
        assert "2:00" in status
        assert "80%" in status

    def test_format_status_paused(self):
        """Test status formatting when paused."""
        from videocat.cli import format_status

        status = format_status(
            mode="NORMAL",
            position=0.0,
            duration=60.0,
            volume=100,
            paused=True,
            muted=False,
        )

        assert "||" in status

    def test_format_status_muted(self):
        """Test status formatting when muted."""
        from videocat.cli import format_status

        status = format_status(
            mode="NORMAL",
            position=0.0,
            duration=60.0,
            volume=100,
            paused=False,
            muted=True,
        )

        assert "MUTE" in status


class TestShowHelp:
    """Tests for help display."""

    def test_show_help_content(self):
        """Test help content includes keybindings."""
        from videocat.cli import get_help_text

        help_text = get_help_text()

        # Check for navigation keys
        assert "space" in help_text.lower() or "pause" in help_text.lower()
        assert "j" in help_text or "→" in help_text
        assert "k" in help_text or "←" in help_text

        # Check for volume keys
        assert "volume" in help_text.lower()
        assert "m" in help_text.lower() or "mute" in help_text.lower()

        # Check for quit
        assert "q" in help_text.lower() or "quit" in help_text.lower()

        # Check for vim-style navigation
        assert "gg" in help_text
        assert "G" in help_text
