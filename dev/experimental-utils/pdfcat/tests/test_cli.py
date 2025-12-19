"""Tests for CLI pages mode."""

import pytest
from click.testing import CliRunner
from pdfcat.cli import main


class TestCLIPagesMode:
    """Test cases for --pages option functionality."""

    def test_pages_single_page(self, sample_pdf):
        """Test --pages outputs single specified page."""
        runner = CliRunner()
        result = runner.invoke(main, [sample_pdf, "--pages", "1"])

        assert result.exit_code == 0
        # Should output Kitty graphics protocol data
        assert "\x1b_G" in result.output or "\x1b[" in result.output

    def test_pages_multiple_pages(self, sample_pdf):
        """Test --pages outputs multiple specified pages."""
        runner = CliRunner()
        result = runner.invoke(main, [sample_pdf, "--pages", "1,3"])

        assert result.exit_code == 0

    def test_pages_page_range(self, sample_pdf):
        """Test --pages supports page range notation."""
        runner = CliRunner()
        result = runner.invoke(main, [sample_pdf, "--pages", "1-3"])

        assert result.exit_code == 0

    def test_pages_mixed_notation(self, sample_pdf):
        """Test --pages supports mixed page notation (e.g., 1,3-5)."""
        runner = CliRunner()
        result = runner.invoke(main, [sample_pdf, "--pages", "1,2-3"])

        assert result.exit_code == 0

    def test_pages_invalid_page(self, sample_pdf):
        """Test --pages with invalid page number shows error."""
        runner = CliRunner()
        result = runner.invoke(main, [sample_pdf, "--pages", "999"])

        assert result.exit_code != 0

    def test_pages_negative_page(self, sample_pdf):
        """Test --pages with negative page number shows error."""
        runner = CliRunner()
        result = runner.invoke(main, [sample_pdf, "--pages", "-1"])

        assert result.exit_code != 0

    def test_pages_short_option(self, sample_pdf):
        """Test -P short option for pages."""
        runner = CliRunner()
        result = runner.invoke(main, [sample_pdf, "-P", "1"])

        assert result.exit_code == 0


class TestParsePages:
    """Test cases for page parsing utility."""

    def test_parse_single_page(self):
        """Test parsing single page number."""
        from pdfcat.cli import parse_pages

        assert parse_pages("1", 10) == [1]
        assert parse_pages("5", 10) == [5]

    def test_parse_multiple_pages(self):
        """Test parsing comma-separated pages."""
        from pdfcat.cli import parse_pages

        assert parse_pages("1,3,5", 10) == [1, 3, 5]

    def test_parse_page_range(self):
        """Test parsing page range."""
        from pdfcat.cli import parse_pages

        assert parse_pages("1-3", 10) == [1, 2, 3]
        assert parse_pages("5-7", 10) == [5, 6, 7]

    def test_parse_mixed_notation(self):
        """Test parsing mixed notation."""
        from pdfcat.cli import parse_pages

        assert parse_pages("1,3-5,7", 10) == [1, 3, 4, 5, 7]

    def test_parse_removes_duplicates(self):
        """Test parsing removes duplicate pages."""
        from pdfcat.cli import parse_pages

        result = parse_pages("1,1,2-3,2", 10)
        assert result == [1, 2, 3]

    def test_parse_sorts_pages(self):
        """Test parsing sorts pages in ascending order."""
        from pdfcat.cli import parse_pages

        result = parse_pages("5,2,1,3", 10)
        assert result == [1, 2, 3, 5]

    def test_parse_invalid_range(self):
        """Test parsing invalid range raises error."""
        from pdfcat.cli import parse_pages

        with pytest.raises(ValueError):
            parse_pages("5-3", 10)  # End before start

    def test_parse_out_of_range(self):
        """Test parsing out-of-range page raises error."""
        from pdfcat.cli import parse_pages

        with pytest.raises(ValueError):
            parse_pages("15", 10)

        with pytest.raises(ValueError):
            parse_pages("0", 10)

    def test_parse_invalid_format(self):
        """Test parsing invalid format raises error."""
        from pdfcat.cli import parse_pages

        with pytest.raises(ValueError):
            parse_pages("abc", 10)
