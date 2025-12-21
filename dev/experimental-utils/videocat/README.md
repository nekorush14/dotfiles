# videocat

A terminal-controlled video player using mpv.

Video is displayed in an external mpv window, while the terminal provides vim-like controls (similar to pdfcat).

## Requirements

- Python 3.10+
- mpv (media player)

### Install mpv

```bash
# macOS
brew install mpv

# Ubuntu/Debian
sudo apt install mpv libmpv-dev

# Arch Linux
sudo pacman -S mpv
```

## Installation

```bash
# Install from source
pip install -e .

# With dev dependencies
pip install -e ".[dev]"
```

## Usage

```bash
# Play a video
videocat video.mp4

# With custom volume
videocat -v 50 video.mp4
```

## Keybindings

| Key | Action |
|-----|--------|
| `Space`, `p`, `k` | Toggle pause |
| `q`, `:q` | Quit |
| `r` | Toggle loop/repeat |
| `j`, `h`, `←` | Seek backward 5s |
| `l`, `→` | Seek forward 5s |
| `J`, `H` | Seek backward 30s |
| `L` | Seek forward 30s |
| `,` | Step backward one frame |
| `.` | Step forward one frame |
| `gg` | Go to beginning |
| `G` | Go to end |
| `[n]G` | Go to n% of video |
| `0` | Go to beginning |
| `=`, `+` | Volume up |
| `-`, `_` | Volume down |
| `m` | Toggle mute |
| `z` | Zoom in |
| `Z` | Zoom out |
| `R` | Reset zoom |
| `?` | Show help |
| `:h` | Show help |

## Architecture

```
videocat/
├── cli.py      # Terminal interface with vim-like controls
├── player.py   # mpv wrapper
└── viewer.py   # Playback controller
```

## Development

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=videocat
```

## License

MIT
