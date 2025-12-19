"""PDF rendering functionality using PyMuPDF.

This module handles PDF file loading and rendering pages to PIL Images.
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import Optional
from PIL import Image


class PDFRenderer:
    """Render PDF pages to images using PyMuPDF."""

    def __init__(self, pdf_path: str):
        """Initialize PDF renderer with a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Raises:
            FileNotFoundError: If PDF file doesn't exist
        """
        self.pdf_path = pdf_path
        # Initialize _doc to None first to avoid AttributeError in __del__
        self._doc: Optional[fitz.Document] = None
        self._closed = False

        # Check if file exists
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    @property
    def doc(self) -> fitz.Document:
        """Get or open the PDF document.

        Returns:
            PyMuPDF Document object

        Raises:
            RuntimeError: If document has been closed
        """
        if self._doc is None:
            if self._closed:
                raise RuntimeError("PDF document has been closed")
            self._doc = fitz.open(self.pdf_path)
        return self._doc

    def get_page_count(self) -> int:
        """Get total number of pages in the PDF.

        Returns:
            Total page count
        """
        return len(self.doc)

    def get_page_size(self, page_num: int) -> tuple[float, float]:
        """Get the size of a page in points (72 DPI).

        Args:
            page_num: Page number (0-indexed)

        Returns:
            Tuple of (width, height) in points
        """
        page = self.doc[page_num]
        rect = page.rect
        return (rect.width, rect.height)

    def render_page(
        self,
        page_num: int,
        zoom: float = 1.0,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
    ) -> Image.Image:
        """Render a specific page to PIL Image.

        Args:
            page_num: Page number (0-indexed)
            zoom: Zoom factor (1.0 = 100%, 2.0 = 200%, etc.)
            max_width: Maximum width in pixels (will fit to this width)
            max_height: Maximum height in pixels (will fit to this height)

        Returns:
            PIL Image of the rendered page

        Raises:
            IndexError: If page number is invalid
            ValueError: If page number is negative
        """
        if page_num < 0:
            raise ValueError(f"Page number must be non-negative: {page_num}")

        if page_num >= self.get_page_count():
            raise IndexError(
                f"Page {page_num} out of range (0-{self.get_page_count() - 1})"
            )

        # Get the page
        page = self.doc[page_num]
        page_width, page_height = page.rect.width, page.rect.height

        # Calculate the effective zoom to fit within max_width/max_height
        effective_zoom = zoom

        if max_width or max_height:
            # Calculate zoom needed to fit within constraints
            if max_width:
                width_zoom = max_width / page_width
            else:
                width_zoom = float("inf")

            if max_height:
                height_zoom = max_height / page_height
            else:
                height_zoom = float("inf")

            # Use the smaller zoom to fit within both constraints
            fit_zoom = min(width_zoom, height_zoom)

            # Apply user zoom on top of fit zoom
            effective_zoom = fit_zoom * zoom

        # Create transformation matrix for zoom
        # 72 DPI is default, so zoom of 2.0 = 144 DPI
        matrix = fitz.Matrix(effective_zoom, effective_zoom)

        # Render page to pixmap
        pix = page.get_pixmap(matrix=matrix)

        # Convert pixmap to PIL Image
        # Use raw samples (RGB bytes without header)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

        return img

    def close(self):
        """Close the PDF document and free resources."""
        if self._doc is not None:
            self._doc.close()
            self._doc = None
        self._closed = True

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def __del__(self):
        """Destructor to ensure document is closed."""
        self.close()
