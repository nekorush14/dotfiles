# webcat

A CLI web browser for Kitty/Ghostty terminals using Kitty graphics protocol.

## Features

- Text and image rendering in terminal
- Kitty graphics protocol for inline images
- Vim-style keybindings
- Link navigation
- Readability extraction for clean article viewing

## Installation

```bash
pip install -e .
```

## Usage

```bash
# View a webpage
webcat https://example.com

# Dump mode (non-interactive)
webcat -d https://example.com

# Raw HTML (no readability extraction)
webcat -r https://example.com

# Without images
webcat -I https://example.com
```

## Keybindings

| Key | Action |
|-----|--------|
| `j`/`k`, arrows | Scroll |
| `d`/`u` | Half-page scroll |
| `gg`/`G` | Top/bottom |
| `f` | Link selection mode |
| `Tab` | Next link |
| `Enter` | Follow link |
| `o` | Open URL |
| `b`/`B` | History back/forward |
| `/` | Search |
| `i` | Toggle images |
| `:q` | Quit |

## Requirements

- Python 3.10+
- Kitty or Ghostty terminal (for image support)
