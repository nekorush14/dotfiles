"""Tests for webcat.cli module."""

import pytest
from click.testing import CliRunner
from pytest_httpserver import HTTPServer
from unittest.mock import patch

from webcat.cli import main


class TestCLIDumpMode:
    """Tests for CLI dump mode (non-interactive)."""

    def test_dump_mode_basic(self, mock_html_server: HTTPServer):
        """Test dump mode outputs page content."""
        runner = CliRunner()
        # Patch WebViewer to allow private IPs for testing
        with patch("webcat.cli.WebViewer") as MockViewer:
            instance = MockViewer.return_value
            instance.load_url.return_value = True
            instance.display.return_value = "Test Page Content"
            instance.close.return_value = None

            result = runner.invoke(main, [mock_html_server.url_for("/"), "--dump"])

            assert result.exit_code == 0

    def test_dump_mode_with_raw(self, mock_html_server: HTTPServer):
        """Test dump mode with raw HTML."""
        runner = CliRunner()
        with patch("webcat.cli.WebViewer") as MockViewer:
            instance = MockViewer.return_value
            instance.load_url.return_value = True
            instance.display.return_value = "Raw HTML Content"
            instance.close.return_value = None

            result = runner.invoke(
                main,
                [mock_html_server.url_for("/"), "--dump", "--raw"],
            )

            assert result.exit_code == 0

    def test_dump_mode_no_images(self, mock_html_server: HTTPServer):
        """Test dump mode without images."""
        runner = CliRunner()
        with patch("webcat.cli.WebViewer") as MockViewer:
            instance = MockViewer.return_value
            instance.load_url.return_value = True
            instance.display.return_value = "Content without images"
            instance.close.return_value = None

            result = runner.invoke(
                main,
                [mock_html_server.url_for("/"), "--dump", "--no-images"],
            )

            assert result.exit_code == 0

    def test_dump_mode_with_width(self, mock_html_server: HTTPServer):
        """Test dump mode with custom width."""
        runner = CliRunner()
        with patch("webcat.cli.WebViewer") as MockViewer:
            instance = MockViewer.return_value
            instance.load_url.return_value = True
            instance.display.return_value = "Narrow content"
            instance.close.return_value = None

            result = runner.invoke(
                main,
                [mock_html_server.url_for("/"), "--dump", "--width", "40"],
            )

            assert result.exit_code == 0

    def test_dump_mode_invalid_url(self):
        """Test dump mode with invalid URL."""
        runner = CliRunner()
        with patch("webcat.cli.WebViewer") as MockViewer:
            instance = MockViewer.return_value
            instance.load_url.return_value = False
            instance.close.return_value = None

            result = runner.invoke(
                main,
                ["http://invalid.localhost.test:99999", "--dump"],
            )

            assert result.exit_code != 0


class TestCLIOptions:
    """Tests for CLI options."""

    def test_help_option(self):
        """Test --help option."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "--dump" in result.output
        assert "--raw" in result.output
        assert "--no-images" in result.output
        assert "--user-agent" in result.output

    def test_version_option(self):
        """Test --version option."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])

        assert result.exit_code == 0
        assert "0.1.0" in result.output or "webcat" in result.output

    def test_timeout_option(self, mock_html_server: HTTPServer):
        """Test --timeout option."""
        runner = CliRunner()
        with patch("webcat.cli.WebViewer") as MockViewer:
            instance = MockViewer.return_value
            instance.load_url.return_value = True
            instance.display.return_value = "Content"
            instance.close.return_value = None

            result = runner.invoke(
                main,
                [mock_html_server.url_for("/"), "--dump", "--timeout", "5"],
            )

            assert result.exit_code == 0

    def test_user_agent_option(self):
        """Test --user-agent option."""
        runner = CliRunner()
        with patch("webcat.cli.WebViewer") as MockViewer:
            instance = MockViewer.return_value
            instance.load_url.return_value = True
            instance.display.return_value = "Content"
            instance.close.return_value = None

            result = runner.invoke(
                main,
                ["https://example.com", "--dump", "--user-agent", "CustomBot/1.0"],
            )

            assert result.exit_code == 0
            # Verify WebViewer was called with custom user_agent
            MockViewer.assert_called_once()
            call_kwargs = MockViewer.call_args[1]
            assert call_kwargs["user_agent"] == "CustomBot/1.0"


class TestCLINoURL:
    """Tests for CLI without URL argument."""

    def test_no_url_shows_usage(self):
        """Test that missing URL shows usage info."""
        runner = CliRunner()
        result = runner.invoke(main, ["--dump"])

        # Should show error or usage
        assert result.exit_code != 0 or "Usage" in result.output or "Error" in result.output
