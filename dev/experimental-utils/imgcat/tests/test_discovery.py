"""Tests for imgcat.discovery module."""

import pytest
from pathlib import Path
from PIL import Image


class TestDiscoverImages:
    """Tests for discover_images function."""

    def test_discover_in_directory_with_images(self, tmp_path: Path):
        """Test discovering images in a directory."""
        from imgcat.discovery import discover_images

        # Setup: create multiple image files
        for i, ext in enumerate([".png", ".jpg", ".gif"]):
            img = Image.new("RGB", (10, 10), color="red")
            img.save(tmp_path / f"image{i}{ext}")

        # Also create a non-image file
        (tmp_path / "readme.txt").write_text("not an image")

        result = discover_images(tmp_path)

        assert len(result) == 3
        assert all(
            Path(p).suffix.lower() in {".png", ".jpg", ".gif"} for p in result
        )

    def test_discover_in_empty_directory(self, tmp_path: Path):
        """Test discovering in directory with no images."""
        from imgcat.discovery import discover_images

        (tmp_path / "readme.txt").write_text("not an image")

        result = discover_images(tmp_path)

        assert result == []

    def test_discover_returns_sorted_list(self, tmp_path: Path):
        """Test that discovered images are sorted alphabetically."""
        from imgcat.discovery import discover_images

        for name in ["zebra.png", "apple.png", "mango.png"]:
            img = Image.new("RGB", (10, 10), color="red")
            img.save(tmp_path / name)

        result = discover_images(tmp_path)

        assert Path(result[0]).name == "apple.png"
        assert Path(result[1]).name == "mango.png"
        assert Path(result[2]).name == "zebra.png"

    def test_discover_with_nonexistent_directory(self):
        """Test with nonexistent directory raises FileNotFoundError."""
        from imgcat.discovery import discover_images

        with pytest.raises(FileNotFoundError):
            discover_images(Path("/nonexistent/path"))

    def test_discover_all_supported_formats(self, tmp_path: Path):
        """Test that all SUPPORTED_FORMATS are discovered."""
        from imgcat.discovery import discover_images
        from imgcat.renderer import SUPPORTED_FORMATS

        for i, ext in enumerate(SUPPORTED_FORMATS):
            if ext == ".svg":
                # SVG needs different handling
                (tmp_path / f"image{i}{ext}").write_text(
                    '<svg xmlns="http://www.w3.org/2000/svg"></svg>'
                )
            else:
                img = Image.new("RGB", (10, 10), color="red")
                img.save(tmp_path / f"image{i}{ext}")

        result = discover_images(tmp_path)

        assert len(result) == len(SUPPORTED_FORMATS)


class TestExpandToDirectory:
    """Tests for expand_to_directory function."""

    def test_expand_single_file_includes_siblings(self, tmp_path: Path):
        """Test that single file expands to include sibling images."""
        from imgcat.discovery import expand_to_directory

        # Create 3 images
        paths = []
        for i in range(3):
            img = Image.new("RGB", (10, 10), color="red")
            path = tmp_path / f"image{i}.png"
            img.save(path)
            paths.append(str(path))

        # Call with just the second file
        result = expand_to_directory(paths[1])

        assert len(result) == 3
        # Original file should be first
        assert result[0] == paths[1]

    def test_expand_with_current_file_first(self, tmp_path: Path):
        """Test that the specified file is first in result."""
        from imgcat.discovery import expand_to_directory

        for name in ["a.png", "b.png", "c.png"]:
            img = Image.new("RGB", (10, 10), color="red")
            img.save(tmp_path / name)

        target = str(tmp_path / "b.png")
        result = expand_to_directory(target)

        assert result[0] == target
        assert len(result) == 3

    def test_expand_nonexistent_file(self):
        """Test with nonexistent file raises FileNotFoundError."""
        from imgcat.discovery import expand_to_directory

        with pytest.raises(FileNotFoundError):
            expand_to_directory("/nonexistent/file.png")


class TestDiscoverImagesFromArgs:
    """Tests for CLI argument processing."""

    def test_no_args_uses_current_directory(self, tmp_path: Path, monkeypatch):
        """Test that no args discovers from current directory."""
        from imgcat.discovery import discover_images_from_args

        # Setup
        for i in range(2):
            img = Image.new("RGB", (10, 10), color="red")
            img.save(tmp_path / f"image{i}.png")

        monkeypatch.chdir(tmp_path)

        result = discover_images_from_args(())

        assert len(result) == 2

    def test_no_args_empty_directory_raises_error(
        self, tmp_path: Path, monkeypatch
    ):
        """Test that no args in empty directory raises FileNotFoundError."""
        from imgcat.discovery import discover_images_from_args

        monkeypatch.chdir(tmp_path)

        with pytest.raises(FileNotFoundError):
            discover_images_from_args(())

    def test_with_file_args_expands_directory(self, tmp_path: Path):
        """Test that file args expand to include siblings."""
        from imgcat.discovery import discover_images_from_args

        for i in range(3):
            img = Image.new("RGB", (10, 10), color="red")
            img.save(tmp_path / f"image{i}.png")

        target = str(tmp_path / "image1.png")
        result = discover_images_from_args((target,))

        assert len(result) == 3
        assert result[0] == target

    def test_with_multiple_file_args(self, tmp_path: Path):
        """Test with multiple explicit file args."""
        from imgcat.discovery import discover_images_from_args

        paths = []
        for i in range(3):
            img = Image.new("RGB", (10, 10), color="red")
            path = tmp_path / f"image{i}.png"
            img.save(path)
            paths.append(str(path))

        # Explicit multiple args should include siblings
        result = discover_images_from_args((paths[0], paths[2]))

        # Should include all 3 (siblings discovered)
        assert len(result) == 3

    def test_with_directory_arg(self, tmp_path: Path):
        """Test that directory argument discovers images in that directory."""
        from imgcat.discovery import discover_images_from_args

        for i in range(3):
            img = Image.new("RGB", (10, 10), color="red")
            img.save(tmp_path / f"image{i}.png")

        result = discover_images_from_args((str(tmp_path),))

        assert len(result) == 3

    def test_with_empty_directory_arg(self, tmp_path: Path):
        """Test that empty directory argument raises FileNotFoundError."""
        from imgcat.discovery import discover_images_from_args

        with pytest.raises(FileNotFoundError):
            discover_images_from_args((str(tmp_path),))

    def test_with_mixed_file_and_directory_args(self, tmp_path: Path):
        """Test with mixed file and directory arguments."""
        from imgcat.discovery import discover_images_from_args

        # Create images in tmp_path
        for i in range(2):
            img = Image.new("RGB", (10, 10), color="red")
            img.save(tmp_path / f"image{i}.png")

        # Create a subdirectory with more images
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        for i in range(2):
            img = Image.new("RGB", (10, 10), color="blue")
            img.save(subdir / f"sub_image{i}.png")

        # Pass a file from tmp_path and the subdirectory
        file_arg = str(tmp_path / "image0.png")
        dir_arg = str(subdir)

        result = discover_images_from_args((file_arg, dir_arg))

        # Should include images from both locations
        assert len(result) == 4
