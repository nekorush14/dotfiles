"""Command-line interface for videocat.

This module provides the CLI entry point and interactive controls.
Video is displayed in an external mpv window, while the terminal
provides vim-like controls.
"""

import os
import sys
import click
import termios
import tty
from pathlib import Path
from typing import Optional

from . import __version__


def format_time(seconds: float) -> str:
    """Format seconds as human-readable time string."""
    seconds = int(seconds) if seconds is not None else 0
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def format_status(
    mode: str,
    position: float,
    duration: float,
    volume: int,
    paused: bool,
    muted: bool,
    loop: bool = False,
    zoom: float = 0.0,
) -> str:
    """Format status bar string."""
    pos_str = format_time(position)
    dur_str = format_time(duration) if duration else "?"

    state = "||" if paused else ">"

    if muted:
        vol_str = "MUTE"
    else:
        vol_str = f"{volume}%"

    # Build status parts
    parts = [f"-- {mode} --", f"{state} {pos_str}/{dur_str}", f"Vol: {vol_str}"]

    # Add loop indicator
    if loop:
        parts.append("LOOP")

    # Add zoom indicator if not default
    if abs(zoom) > 0.01:
        zoom_pct = int((2 ** zoom) * 100)
        parts.append(f"Zoom: {zoom_pct}%")

    return " | ".join(parts)


def get_help_text() -> str:
    """Get help text with keybindings."""
    return """
╔═══════════════════════════════════════════════════════════╗
║                  videocat - Video Player                  ║
╠═══════════════════════════════════════════════════════════╣
║  Playback:                                                ║
║    Space,p,k : Toggle pause                               ║
║    q, :q     : Quit                                       ║
║    r         : Toggle loop/repeat                         ║
║                                                           ║
║  Navigation:                                              ║
║    j, h, ←   : Seek backward 5 seconds                    ║
║    l, →      : Seek forward 5 seconds                     ║
║    J, H      : Seek backward 30 seconds                   ║
║    L         : Seek forward 30 seconds                    ║
║    ,         : Step backward one frame                    ║
║    .         : Step forward one frame                     ║
║    gg        : Go to beginning                            ║
║    G         : Go to end                                  ║
║    [n]G      : Go to n% of video                          ║
║                                                           ║
║  Volume:                                                  ║
║    =, +      : Volume up                                  ║
║    -, _      : Volume down                                ║
║    m         : Toggle mute                                ║
║                                                           ║
║  Zoom:                                                    ║
║    z         : Zoom in                                    ║
║    Z         : Zoom out                                   ║
║    R         : Reset zoom                                 ║
║                                                           ║
║  Other:                                                   ║
║    ?         : Show this help                             ║
║    Ctrl-L    : Refresh status                             ║
╚═══════════════════════════════════════════════════════════╝

Press any key to continue...
"""


def get_keypress() -> str:
    """Get a single keypress from terminal.

    Note: Terminal should already be in cbreak mode.
    """
    ch = sys.stdin.read(1)

    if ch == "\x1b":
        # Check for escape sequence
        import select
        more, _, _ = select.select([sys.stdin], [], [], 0.05)
        if more:
            ch2 = sys.stdin.read(1)
            if ch2 == "[":
                ch3 = sys.stdin.read(1)
                if ch3 == "A":
                    return "UP"
                elif ch3 == "B":
                    return "DOWN"
                elif ch3 == "C":
                    return "RIGHT"
                elif ch3 == "D":
                    return "LEFT"
            return "ESC"
        return "ESC"
    return ch


def read_line_with_escape() -> str | None:
    """Read a line of input, allowing ESC to cancel."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    buffer = ""

    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)

            if ch == "\x1b":  # ESC
                return None
            elif ch in ("\r", "\n"):  # Enter
                return buffer
            elif ch == "\x7f" or ch == "\x08":  # Backspace
                if buffer:
                    buffer = buffer[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            elif ch == "\x03":  # Ctrl-C
                return None
            elif ch.isprintable():
                buffer += ch
                sys.stdout.write(ch)
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def clear_line():
    """Clear current line."""
    sys.stdout.write("\r\x1b[K")
    sys.stdout.flush()


def get_terminal_width() -> int:
    """Get terminal width."""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def show_status(status: str):
    """Show status bar on current line."""
    # Truncate status to terminal width to prevent line wrapping
    width = get_terminal_width()
    if len(status) >= width:
        status = status[:width - 1]
    sys.stdout.write(f"\r\x1b[K{status}")
    sys.stdout.flush()


@click.command()
@click.argument("video_file", type=click.Path(exists=True))
@click.option(
    "--volume",
    "-v",
    default=100,
    type=int,
    help="Initial volume (0-100, default: 100)",
)
@click.version_option(version=__version__)
def main(
    video_file: str,
    volume: int,
):
    """Play video files with mpv, controlled from terminal.

    VIDEO_FILE: Path to the video file to play

    Video is displayed in an external mpv window.
    Use vim-like keybindings in terminal to control playback.
    """
    from .viewer import VideoViewer

    video_path = Path(video_file)
    if not video_path.exists():
        click.echo(f"Error: File not found: {video_file}", err=True)
        sys.exit(1)

    try:
        viewer = VideoViewer(str(video_path), volume=volume)
    except Exception as e:
        click.echo(f"Error opening video: {e}", err=True)
        sys.exit(1)

    if not viewer.wait_until_playing(timeout=10.0):
        click.echo("Error: Timeout waiting for video to load", err=True)
        viewer.close()
        sys.exit(1)

    # Show initial status
    info = viewer.get_playback_info()
    status = format_status(
        "NORMAL",
        info["position"],
        info["duration"],
        info["volume"],
        info["paused"],
        info["muted"],
        info.get("loop", False),
        info.get("zoom", 0.0),
    )
    show_status(status)

    import select

    running = True
    num_buffer = ""  # For vim-style [n]G commands

    # Set terminal to cbreak mode for the entire session
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)

        while running:
            # Non-blocking keypress check
            readable, _, _ = select.select([sys.stdin], [], [], 0.1)

            if readable:
                key = get_keypress()

                # Accumulate number prefix for [n]G
                if key.isdigit() and num_buffer != "":
                    num_buffer += key
                    continue
                elif key.isdigit() and key != "0":
                    num_buffer = key
                    continue

                # Quit
                if key in ("q", "\x03"):
                    running = False
                    break

                # Toggle pause
                elif key in (" ", "p", "k"):
                    num_buffer = ""
                    viewer.toggle_pause()

                # Seek forward (5s)
                elif key in ("l", "RIGHT"):
                    num_buffer = ""
                    viewer.seek_forward(5)

                # Seek backward (5s)
                elif key in ("j", "h", "LEFT"):
                    num_buffer = ""
                    viewer.seek_backward(5)

                # Seek forward (30s)
                elif key == "L":
                    num_buffer = ""
                    viewer.seek_forward(30)

                # Seek backward (30s)
                elif key in ("J", "H"):
                    num_buffer = ""
                    viewer.seek_backward(30)

                # Frame step forward
                elif key == ".":
                    num_buffer = ""
                    viewer.frame_step()

                # Frame step backward
                elif key == ",":
                    num_buffer = ""
                    viewer.frame_back_step()

                # Toggle loop/repeat
                elif key == "r":
                    num_buffer = ""
                    viewer.toggle_loop()

                # Zoom in
                elif key == "z":
                    num_buffer = ""
                    viewer.zoom_in(0.1)

                # Zoom out
                elif key == "Z":
                    num_buffer = ""
                    viewer.zoom_out(0.1)

                # Reset zoom
                elif key == "R":
                    num_buffer = ""
                    viewer.reset_zoom()

                # G - go to end, or [n]G to go to n%
                elif key == "G":
                    if num_buffer:
                        percent = int(num_buffer) / 100.0
                        info = viewer.get_playback_info()
                        if info["duration"]:
                            target = info["duration"] * percent
                            viewer.seek_absolute(target)
                    else:
                        info = viewer.get_playback_info()
                        if info["duration"]:
                            viewer.seek_absolute(info["duration"] - 0.1)
                    num_buffer = ""

                # gg - go to beginning
                elif key == "g":
                    next_key = get_keypress()
                    if next_key == "g":
                        viewer.seek_absolute(0)
                    num_buffer = ""

                # Command mode
                elif key == ":":
                    num_buffer = ""
                    show_status(format_status(
                        "COMMAND",
                        info["position"],
                        info["duration"],
                        info["volume"],
                        info["paused"],
                        info["muted"],
                        info.get("loop", False),
                        info.get("zoom", 0.0),
                    ))
                    sys.stdout.write("\n:")
                    sys.stdout.flush()

                    cmd = read_line_with_escape()

                    if cmd is None or cmd == "":
                        pass
                    elif cmd in ("q", "quit"):
                        running = False
                        break
                    elif cmd in ("h", "help"):
                        print("\n" + get_help_text(), flush=True)
                        get_keypress()

                    # Clear command line and continue
                    sys.stdout.write("\x1b[A\r\x1b[K")
                    sys.stdout.flush()

                # Volume up
                elif key in ("=", "+"):
                    num_buffer = ""
                    viewer.volume_up(5)

                # Volume down
                elif key in ("-", "_"):
                    num_buffer = ""
                    viewer.volume_down(5)

                # Toggle mute
                elif key == "m":
                    num_buffer = ""
                    viewer.toggle_mute()

                # Show help
                elif key == "?":
                    num_buffer = ""
                    print("\n" + get_help_text(), flush=True)
                    get_keypress()

                # Refresh (Ctrl-L)
                elif key == "\x0c":
                    num_buffer = ""

                # Reset zoom / percentage seek with 0
                elif key == "0" and num_buffer == "":
                    viewer.seek_absolute(0)

                else:
                    num_buffer = ""

            # Update status
            info = viewer.get_playback_info()
            status = format_status(
                "NORMAL",
                info["position"],
                info["duration"],
                info["volume"],
                info["paused"],
                info["muted"],
                info.get("loop", False),
                info.get("zoom", 0.0),
            )
            show_status(status)

    except KeyboardInterrupt:
        pass
    finally:
        # Restore terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        clear_line()
        viewer.close()


if __name__ == "__main__":
    main()
