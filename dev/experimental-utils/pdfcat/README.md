# pdfcat

A PDF viewer for terminal emulators that support the Kitty graphics protocol (Ghostty, Kitty, etc.).

## Features

- Display PDF files directly in your terminal
- Vim-style keyboard navigation (j/k, G, gg, etc.)
- Command mode with `:` prefix
- Zoom in/out functionality (25% - 400%)
- Automatic terminal size detection for optimal display
- Non-interactive batch mode for outputting specific pages
- Lightweight and fast

## Requirements

- Python 3.8 or higher
- Terminal emulator with Kitty graphics protocol support (Ghostty, Kitty, WezTerm, etc.)

## Installation

### From source

```bash
# Clone or download this repository
cd pdfcat

# Install in development mode
pip install -e .

# Or install for production
pip install .
```

## Usage

### Basic usage

```bash
# Open a PDF file
pdfcat path/to/document.pdf

# Start at a specific page
pdfcat path/to/document.pdf --page 5

# Set initial zoom level
pdfcat path/to/document.pdf --zoom 1.5

# Limit display width
pdfcat path/to/document.pdf --max-width 1200

# Adjust terminal fit ratio (default: 90%)
pdfcat path/to/document.pdf --fit 0.85

# Output specific pages and exit (non-interactive)
pdfcat path/to/document.pdf --pages 1,3,5
pdfcat path/to/document.pdf --pages 1-5
pdfcat path/to/document.pdf --pages 1,3-5,7
```

### Keyboard shortcuts

#### Navigation (NORMAL mode)

| Key | Action |
|-----|--------|
| `j`, `n`, `↓`, `→` | Next page |
| `k`, `p`, `↑`, `←` | Previous page |
| `gg` | Go to first page |
| `G` | Go to last page |
| `[n]G` | Go to page n (type number, then G) |

#### Zoom (NORMAL mode)

| Key | Action |
|-----|--------|
| `=` | Zoom in (5%) |
| `+` | Zoom in (10%) |
| `-` | Zoom out (5%) |
| `_` | Zoom out (10%) |
| `0` | Reset zoom to 100% |

#### Other (NORMAL mode)

| Key | Action |
|-----|--------|
| `Ctrl-L` | Refresh current page |
| `Esc` | Return to normal mode |

#### Commands (COMMAND mode - type `:` to enter)

| Command | Action |
|---------|--------|
| `:h`, `:help` | Show help |
| `:r`, `:refresh` | Refresh current page |
| `:q`, `:quit` | Quit |
| `:[n]` | Go to page n |

## Architecture

The project is organized into the following modules:

- `pdfcat/cli.py` - CLI entry point and interactive controls
- `pdfcat/renderer.py` - PDF to image conversion using PyMuPDF
- `pdfcat/kitty.py` - Kitty graphics protocol implementation
- `pdfcat/viewer.py` - Interactive viewer logic (navigation, zoom)

## Development

### Setup development environment

```bash
# Install with development dependencies
pip install -e ".[dev]"
```

### Run tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pdfcat

# Run specific test file
pytest tests/test_renderer.py
```

### Project structure

```
pdfcat/
├── pdfcat/
│   ├── __init__.py
│   ├── cli.py         # CLI entry point and interactive controls
│   ├── renderer.py    # PDF to image conversion
│   ├── kitty.py       # Kitty graphics protocol
│   └── viewer.py      # Interactive viewer logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py    # Test fixtures
│   ├── test_cli.py
│   ├── test_kitty.py
│   ├── test_renderer.py
│   └── test_viewer.py
├── pyproject.toml
└── README.md
```

## How it works

1. **PDF Rendering**: Uses PyMuPDF (fitz) to render PDF pages to images
2. **Image Encoding**: Converts images to PNG format and encodes as base64
3. **Terminal Display**: Uses Kitty graphics protocol escape sequences to display images in the terminal (supports chunked transmission for large images)
4. **Interactive Controls**: Vim-style keyboard navigation with NORMAL and COMMAND modes

## Kitty Graphics Protocol

The Kitty graphics protocol is a terminal extension that allows applications to display images. The basic format is:

```
ESC _G<control data>;<payload>ESC \
```

This tool implements the protocol to transmit and display PDF pages as images.

## Dependencies

- **PyMuPDF (fitz)**: PDF rendering engine
- **Pillow (PIL)**: Image processing
- **Click**: Command-line interface framework

## License

This project is provided as-is for educational and personal use.

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass (`pytest`)
2. Code follows the existing style
3. New features include tests
4. Documentation is updated

## Troubleshooting

### Images not displaying

- Ensure your terminal supports Kitty graphics protocol
- Test with Ghostty, Kitty, or WezTerm
- Check terminal emulator documentation for graphics protocol support

### Poor image quality

- Increase zoom level with `+` key
- Use `--zoom` flag for initial zoom
- Adjust `--max-width` to fit your terminal size

### Slow performance

- Large PDF files may take time to render
- Consider reducing zoom level
- Close and reopen the viewer to free memory
