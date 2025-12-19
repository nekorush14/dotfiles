"""Pytest configuration and fixtures."""

import pytest
import fitz  # PyMuPDF
from pathlib import Path


@pytest.fixture(scope="session")
def test_pdf_path(tmp_path_factory):
    """Create a test PDF file for testing.

    Returns:
        Path to the test PDF file
    """
    # Create temporary directory
    tmp_dir = tmp_path_factory.mktemp("test_pdfs")
    pdf_path = tmp_dir / "test.pdf"

    # Create a simple PDF with 3 pages
    doc = fitz.open()

    # Add 3 pages with different colors
    colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]  # Red, Green, Blue

    for i, color in enumerate(colors):
        page = doc.new_page(width=595, height=842)  # A4 size

        # Draw colored rectangle
        rect = fitz.Rect(50, 50, 545, 792)
        page.draw_rect(rect, color=color, fill=color)

        # Add page number text
        text_point = fitz.Point(300, 420)
        page.insert_text(
            text_point,
            f"Page {i + 1}",
            fontsize=48,
            color=(1, 1, 1),  # White text
        )

    # Save PDF
    doc.save(str(pdf_path))
    doc.close()

    return str(pdf_path)


@pytest.fixture
def sample_pdf(test_pdf_path):
    """Provide test PDF path as fixture.

    Returns:
        Path to test PDF file
    """
    return test_pdf_path
