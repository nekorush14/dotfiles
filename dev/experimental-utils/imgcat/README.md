# imgcat

Terminal image viewer with vim-style keybindings using Kitty graphics protocol.

## Features

- **Multiple image formats**: PNG, JPEG, GIF, WebP, BMP, TIFF, SVG
- **Animated GIF support**: Play/pause with frame-by-frame navigation
- **Vim-style navigation**: j/k for file navigation, gg/G for first/last
- **Zoom control**: 25% to 400% with keyboard shortcuts
- **Multiple file support**: View multiple images in one session
- **Kitty graphics protocol**: High-quality image rendering in terminal

## Requirements

- Python 3.8+
- Terminal with Kitty graphics protocol support (Kitty, Ghostty, WezTerm, etc.)

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Usage

```bash
# View single image
imgcat image.png

# View multiple images
imgcat *.png

# With initial zoom
imgcat --zoom 1.5 image.png

# Fit to specific terminal ratio (default: 0.90)
imgcat --fit 0.8 image.png

# Specify maximum width in pixels
imgcat --max-width 800 image.png
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--zoom` | `-z` | Initial zoom level (default: 1.0) |
| `--fit` | `-f` | Fit to terminal ratio, 0.0-1.0 (default: 0.90) |
| `--max-width` | `-w` | Maximum display width in pixels |

## Keybindings

### Navigation

| Key | Action |
|-----|--------|
| `j`, `n`, `DOWN` | Next file |
| `k`, `p`, `UP` | Previous file |
| `gg` | Go to first file |
| `G` | Go to last file |
| `[n]G` | Go to file n |

### Animation (GIF)

| Key | Action |
|-----|--------|
| `Space` | Play/Pause |
| `h`, `LEFT` | Previous frame |
| `l`, `RIGHT` | Next frame |

### Zoom

| Key | Action |
|-----|--------|
| `=` | Zoom in (5%) |
| `+` | Zoom in (10%) |
| `-` | Zoom out (5%) |
| `_` | Zoom out (10%) |
| `0` | Reset zoom (100%) |

### Other

| Key | Action |
|-----|--------|
| `Ctrl-L` | Refresh display |
| `?` | Show help |
| `:` | Enter command mode |
| `ESC` | Clear input buffer |

### Command Mode

| Command | Action |
|---------|--------|
| `:q`, `:quit` | Quit |
| `:h`, `:help` | Show help |
| `:r`, `:refresh` | Refresh display |
| `:[n]` | Go to file n |

## Supported Formats

- **Static images**: PNG, JPEG, GIF (static), WebP, BMP, TIFF
- **Animated**: GIF (with frame timing)
- **Vector**: SVG (rasterized via CairoSVG)

## Development

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=imgcat
```

## License

MIT
