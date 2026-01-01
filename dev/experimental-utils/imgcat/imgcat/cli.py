"""Command-line interface for imgcat.

This module provides the CLI entry point and interactive controls
with vim-style keybindings and animation support.
"""

import sys
import select
import shutil
import click
import termios
import tty
from pathlib import Path
from typing import Optional

from .viewer import ImageViewer
from .discovery import discover_images_from_args
from .clipboard import copy_image_to_clipboard


def get_terminal_pixel_size() -> tuple[int, int]:
    """Get terminal size in pixels using TIOCGWINSZ ioctl.

    Returns:
        Tuple of (width, height) in pixels, or estimated size if unavailable
    """
    try:
        import fcntl
        import struct

        # TIOCGWINSZ returns: rows, cols, xpixel, ypixel
        result = fcntl.ioctl(
            sys.stdout.fileno(),
            termios.TIOCGWINSZ,
            b"\x00" * 8,
        )
        rows, cols, xpixel, ypixel = struct.unpack("HHHH", result)

        if xpixel > 0 and ypixel > 0:
            return (xpixel, ypixel)
    except Exception:
        pass

    # Fallback: estimate based on character cell size (assume ~10x20 pixels per cell)
    term_size = shutil.get_terminal_size()
    return (term_size.columns * 10, term_size.lines * 20)


def calculate_fit_size(target_ratio: float = 0.85) -> tuple[int, int]:
    """Calculate the size to fit within target_ratio of terminal.

    Args:
        target_ratio: Ratio of terminal to fill (0.0 to 1.0)

    Returns:
        Tuple of (max_width, max_height) in pixels
    """
    width, height = get_terminal_pixel_size()
    return (int(width * target_ratio), int(height * target_ratio))


def get_keypress() -> str:
    """Get a single keypress from terminal.

    Returns:
        Single character or special key name
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)

        # Handle escape sequences for arrow keys
        if ch == "\x1b":
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
            return "\x1b"  # ESC alone
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def get_keypress_nonblocking(timeout: float = 0.01) -> Optional[str]:
    """Get a keypress without blocking.

    Args:
        timeout: Timeout in seconds

    Returns:
        Key pressed, or None if no key pressed within timeout
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            ch = sys.stdin.read(1)

            # Handle escape sequences for arrow keys
            if ch == "\x1b":
                # Check if more data available
                rlist2, _, _ = select.select([sys.stdin], [], [], 0.01)
                if rlist2:
                    ch2 = sys.stdin.read(1)
                    if ch2 == "[":
                        rlist3, _, _ = select.select([sys.stdin], [], [], 0.01)
                        if rlist3:
                            ch3 = sys.stdin.read(1)
                            if ch3 == "A":
                                return "UP"
                            elif ch3 == "B":
                                return "DOWN"
                            elif ch3 == "C":
                                return "RIGHT"
                            elif ch3 == "D":
                                return "LEFT"
                return "\x1b"
            return ch
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def read_line_with_escape() -> Optional[str]:
    """Read a line of input, allowing ESC to cancel.

    Returns:
        The input string, or None if cancelled with ESC
    """
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


def read_command_with_completion() -> Optional[str]:
    """Read a command line with tab completion for :e command.

    Supports tab completion when input is 'e' or starts with 'e '.
    Tab cycles through completions, Shift+Tab cycles backwards.
    No completion list is displayed - just inline replacement (like vim).

    Returns:
        The command string, or None if cancelled with ESC
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    buffer = ""
    completion_index = -1
    completions: list[str] = []
    original_prefix = ""  # Store the original typed prefix

    def redraw_line():
        """Redraw the command line."""
        sys.stdout.write(f"\r\x1b[K:{buffer}")
        sys.stdout.flush()

    def get_path_from_buffer(buf: str) -> str:
        """Extract path portion from 'e <path>' buffer."""
        if buf.startswith("e "):
            return buf[2:]
        elif buf == "e":
            return ""
        return ""

    def set_path_in_buffer(path: str) -> str:
        """Create buffer with 'e <path>' format."""
        return f"e {path}"

    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)

            if ch == "\x1b":  # ESC or escape sequence
                rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
                if rlist:
                    ch2 = sys.stdin.read(1)
                    if ch2 == "[":
                        rlist2, _, _ = select.select([sys.stdin], [], [], 0.05)
                        if rlist2:
                            ch3 = sys.stdin.read(1)
                            # Shift+Tab is ESC [ Z
                            if ch3 == "Z":
                                if completions:
                                    completion_index = (
                                        completion_index - 1
                                    ) % len(completions)
                                    buffer = set_path_in_buffer(
                                        completions[completion_index]
                                    )
                                    redraw_line()
                                continue
                            elif ch3 in ("A", "B", "C", "D"):
                                # Arrow keys - ignore
                                continue
                        continue
                    continue
                # Plain ESC - cancel
                return None

            elif ch in ("\r", "\n"):  # Enter
                return buffer

            elif ch == "\x7f" or ch == "\x08":  # Backspace
                if buffer:
                    buffer = buffer[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                # Reset completions when user types
                completions = []
                completion_index = -1

            elif ch == "\x03":  # Ctrl-C
                return None

            elif ch == "\t":  # Tab - completion
                # Complete if buffer is "e" or starts with "e "
                if buffer == "e" or buffer.startswith("e "):
                    if not completions:
                        # First Tab: get completions
                        original_prefix = get_path_from_buffer(buffer)
                        completions = get_path_completions(original_prefix)
                        completion_index = -1

                    if not completions:
                        continue

                    # Cycle to next completion
                    completion_index = (completion_index + 1) % len(completions)
                    buffer = set_path_in_buffer(completions[completion_index])
                    redraw_line()

            elif ch.isprintable():
                buffer += ch
                sys.stdout.write(ch)
                sys.stdout.flush()
                # Reset completions when user types
                completions = []
                completion_index = -1

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def get_path_completions(prefix: str) -> list[str]:
    """Get path completions for the given prefix.

    Args:
        prefix: The path prefix to complete

    Returns:
        List of completion candidates (directories and image files)
    """
    from .renderer import SUPPORTED_FORMATS

    if not prefix:
        # Empty prefix: list current directory
        base_dir = Path.cwd()
        prefix_part = ""
    elif prefix.startswith("~"):
        # Expand home directory
        expanded = Path(prefix).expanduser()
        if expanded.is_dir():
            base_dir = expanded
            prefix_part = ""
        else:
            base_dir = expanded.parent
            prefix_part = expanded.name
    else:
        path = Path(prefix)
        if path.is_dir():
            base_dir = path
            prefix_part = ""
        else:
            base_dir = path.parent if path.parent.exists() else Path.cwd()
            prefix_part = path.name

    completions = []
    try:
        for entry in base_dir.iterdir():
            name = entry.name
            if prefix_part and not name.lower().startswith(prefix_part.lower()):
                continue

            if entry.is_dir():
                # Add directories with trailing slash
                completions.append(str(entry) + "/")
            elif entry.suffix.lower() in SUPPORTED_FORMATS:
                # Add image files
                completions.append(str(entry))
    except PermissionError:
        pass

    return sorted(completions, key=lambda x: x.lower())


def clear_screen():
    """Clear terminal screen."""
    print("\x1b[2J\x1b[H", end="", flush=True)


def show_help():
    """Display help message with keybindings."""
    help_text = """
+---------------------------------------------------------------+
|                   imgcat - Image Viewer                       |
+---------------------------------------------------------------+
|  Navigation:                                                  |
|    j, n, DOWN     : Next file                                 |
|    k, p, UP       : Previous file                             |
|    gg             : Go to first file                          |
|    G              : Go to last file                           |
|    [n]G           : Go to file n (type number, then G)        |
|                                                               |
|  Animation (GIF):                                             |
|    Space          : Play/Pause animation                      |
|    h, LEFT        : Previous frame (manual)                   |
|    l, RIGHT       : Next frame (manual)                       |
|                                                               |
|  Zoom:                                                        |
|    =              : Zoom in (5%)                              |
|    +              : Zoom in (10%)                             |
|    -              : Zoom out (5%)                             |
|    _              : Zoom out (10%)                            |
|    0              : Reset zoom to 100%                        |
|                                                               |
|  Clipboard:                                                   |
|    yy             : Copy image to clipboard                   |
|                                                               |
|  Other:                                                       |
|    Ctrl-L         : Refresh display                           |
|    ?              : Show this help                            |
|                                                               |
|  Commands (type ':' to enter COMMAND mode):                   |
|    :q, :quit      : Quit                                      |
|    :h, :help      : Show help                                 |
|    :r, :refresh   : Refresh display                           |
|    :e <path>      : Open file/directory (Tab to complete)     |
|    :[n]           : Go to file n                              |
+---------------------------------------------------------------+

Press any key to continue...
"""
    print(help_text, flush=True)


def show_status(viewer: ImageViewer, mode: str = "NORMAL", newline: bool = True):
    """Show status bar with file and animation info.

    Args:
        viewer: ImageViewer instance
        mode: Current mode (NORMAL, COMMAND, etc.)
        newline: If True, prepend newline and end with newline (default).
                 If False, output status without leading/trailing newlines.
    """
    info = viewer.get_info()

    status_parts = [
        f"-- {mode} --",
        f"File {info['current_file']}/{info['total_files']}",
        f"[{info['filename']}]",
        f"Zoom: {info['zoom']:.0%}",
    ]

    if info["is_animated"]:
        play_status = ">" if info["is_playing"] else "||"
        status_parts.append(
            f"Frame {info['current_frame']}/{info['total_frames']} {play_status}"
        )

    status = " | ".join(status_parts)
    if newline:
        print(f"\n{status}", flush=True)
    else:
        sys.stdout.write(status)
        sys.stdout.flush()


@click.command()
@click.argument("image_files", nargs=-1, type=click.Path(exists=True), required=False)
@click.option(
    "--zoom",
    "-z",
    default=1.0,
    type=float,
    help="Initial zoom level (default: 1.0)",
)
@click.option(
    "--fit",
    "-f",
    default=0.90,
    type=float,
    help="Fit to terminal ratio (0.0-1.0, default: 0.90)",
)
@click.option(
    "--max-width",
    "-w",
    type=int,
    help="Maximum display width in pixels",
)
def main(image_files: tuple[str, ...], zoom: float, fit: float, max_width: int):
    """Display images in terminal using Kitty graphics protocol.

    IMAGE_FILES: One or more image files or directories to display.
                 If not specified, discovers images in current directory.
    """
    # Discover image files
    try:
        image_paths = discover_images_from_args(image_files)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if not image_paths:
        click.echo("Error: No image files found", err=True)
        sys.exit(1)

    # Calculate display size
    if max_width is None:
        calc_max_width, calc_max_height = calculate_fit_size(fit)
    else:
        calc_max_width = max_width
        calc_max_height = None

    # Initialize viewer
    try:
        viewer = ImageViewer(
            image_paths,
            initial_zoom=zoom,
            max_width=calc_max_width,
            max_height=calc_max_height,
        )
    except Exception as e:
        click.echo(f"Error opening image: {e}", err=True)
        sys.exit(1)

    # Display first image
    clear_screen()
    print(viewer.display_current(), end="", flush=True)
    show_status(viewer)

    # Interactive loop
    num_buffer = ""
    has_animation = viewer.get_info()["is_animated"]

    try:
        while True:
            # Use non-blocking input for animated GIFs
            if has_animation and viewer.get_info().get("is_playing", False):
                key = get_keypress_nonblocking(timeout=0.016)  # ~60fps check rate

                # Update animation
                if viewer.update_animation():
                    clear_screen()
                    print(viewer.display_current(), end="", flush=True)
                    show_status(viewer)
            else:
                key = get_keypress()

            if key is None:
                continue

            # Accumulate number prefix for vim commands like [n]G
            if key.isdigit() and num_buffer != "":
                num_buffer += key
                continue
            elif key.isdigit() and key != "0":
                num_buffer = key
                continue

            # Navigation - Next file
            if key in ("j", "n", "DOWN"):
                num_buffer = ""
                if viewer.next_file():
                    has_animation = viewer.get_info()["is_animated"]
                    clear_screen()
                    print(viewer.display_current(), end="", flush=True)
                    show_status(viewer)

            # Navigation - Previous file
            elif key in ("k", "p", "UP"):
                num_buffer = ""
                if viewer.previous_file():
                    has_animation = viewer.get_info()["is_animated"]
                    clear_screen()
                    print(viewer.display_current(), end="", flush=True)
                    show_status(viewer)

            # Animation - Next frame (manual)
            elif key in ("l", "RIGHT"):
                num_buffer = ""
                if has_animation:
                    viewer.next_frame()
                    clear_screen()
                    print(viewer.display_current(), end="", flush=True)
                    show_status(viewer)

            # Animation - Previous frame (manual)
            elif key in ("h", "LEFT"):
                num_buffer = ""
                if has_animation:
                    viewer.prev_frame()
                    clear_screen()
                    print(viewer.display_current(), end="", flush=True)
                    show_status(viewer)

            # Toggle animation play/pause
            elif key == " ":
                num_buffer = ""
                if has_animation:
                    viewer.toggle_animation()
                    show_status(viewer)

            # vim: G - go to last file, or [n]G to go to file n
            elif key == "G":
                if num_buffer:
                    try:
                        file_num = int(num_buffer)
                        viewer.go_to_file(file_num)
                        has_animation = viewer.get_info()["is_animated"]
                        clear_screen()
                        print(viewer.display_current(), end="", flush=True)
                        show_status(viewer)
                    except ValueError:
                        pass
                else:
                    viewer.go_to_last_file()
                    has_animation = viewer.get_info()["is_animated"]
                    clear_screen()
                    print(viewer.display_current(), end="", flush=True)
                    show_status(viewer)
                num_buffer = ""

            # vim: gg - go to first file
            elif key == "g":
                next_key = get_keypress()
                if next_key == "g":
                    viewer.go_to_first_file()
                    has_animation = viewer.get_info()["is_animated"]
                    clear_screen()
                    print(viewer.display_current(), end="", flush=True)
                    show_status(viewer)
                num_buffer = ""

            # vim: yy - copy image to clipboard
            elif key == "y":
                next_key = get_keypress()
                if next_key == "y":
                    info = viewer.get_info()
                    current_path = str(
                        viewer.image_paths[viewer.current_file_index]
                    )
                    if copy_image_to_clipboard(current_path):
                        print(f"\nCopied to clipboard: {info['filename']}", flush=True)
                    else:
                        print("\nFailed to copy to clipboard", flush=True)
                num_buffer = ""

            # vim-style : command mode
            elif key == ":":
                num_buffer = ""
                # Update only the status line (avoid full screen redraw to prevent flicker)
                # Move cursor up one line, clear line, show COMMAND mode status
                sys.stdout.write("\x1b[A")  # Move cursor up
                sys.stdout.write("\r\x1b[K")  # Go to line start and clear line
                show_status(viewer, "COMMAND", newline=False)
                sys.stdout.write("\n:")
                sys.stdout.flush()

                cmd_input = read_command_with_completion()

                if cmd_input is None:
                    # ESC pressed - restore NORMAL mode status
                    sys.stdout.write("\r\x1b[K")  # Clear command line
                    sys.stdout.write("\x1b[A")  # Move cursor up
                    sys.stdout.write("\r\x1b[K")  # Clear status line
                    show_status(viewer, newline=False)
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                elif cmd_input == "":
                    # Empty command - restore NORMAL mode status
                    sys.stdout.write("\r\x1b[K")  # Clear command line
                    sys.stdout.write("\x1b[A")  # Move cursor up
                    sys.stdout.write("\r\x1b[K")  # Clear status line
                    show_status(viewer, newline=False)
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                elif cmd_input in ("q", "quit"):
                    break
                elif cmd_input in ("h", "help"):
                    clear_screen()
                    show_help()
                    get_keypress()
                    clear_screen()
                    print(viewer.display_current(), end="", flush=True)
                    show_status(viewer)
                elif cmd_input in ("r", "refresh"):
                    clear_screen()
                    print(viewer.display_current(), end="", flush=True)
                    show_status(viewer)
                elif cmd_input.startswith("e "):
                    # :e <path> command - open file/directory
                    file_path = cmd_input[2:].strip()  # Remove "e " prefix
                    if file_path:
                        # Expand ~ to home directory
                        if file_path.startswith("~"):
                            file_path = str(Path(file_path).expanduser())
                        # Remove trailing slash if present
                        file_path = file_path.rstrip("/")

                        path = Path(file_path)
                        if path.exists():
                            if path.is_dir():
                                # Directory: discover images and switch
                                from .discovery import discover_images
                                dir_images = discover_images(path)
                                if dir_images:
                                    viewer.image_paths = [Path(p) for p in dir_images]
                                    viewer.current_file_index = 0
                                    viewer.total_files = len(dir_images)
                                    viewer._load_current_file()
                                    has_animation = viewer.get_info()["is_animated"]
                                    clear_screen()
                                    print(viewer.display_current(), end="", flush=True)
                                    show_status(viewer)
                                else:
                                    print(f"\nNo images found in: {file_path}", flush=True)
                            else:
                                # File: expand to directory and open
                                from .discovery import expand_to_directory
                                try:
                                    new_paths = expand_to_directory(file_path)
                                    viewer.image_paths = [Path(p) for p in new_paths]
                                    viewer.current_file_index = 0
                                    viewer.total_files = len(new_paths)
                                    viewer._load_current_file()
                                    has_animation = viewer.get_info()["is_animated"]
                                    clear_screen()
                                    print(viewer.display_current(), end="", flush=True)
                                    show_status(viewer)
                                except Exception as e:
                                    print(f"\nError opening file: {e}", flush=True)
                        else:
                            print(f"\nFile not found: {file_path}", flush=True)
                    else:
                        # :e without path - restore display
                        sys.stdout.write("\r\x1b[K")
                        sys.stdout.write("\x1b[A")
                        sys.stdout.write("\r\x1b[K")
                        show_status(viewer, newline=False)
                        sys.stdout.write("\n")
                        sys.stdout.flush()
                else:
                    try:
                        file_num = int(cmd_input)
                        viewer.go_to_file(file_num)
                        has_animation = viewer.get_info()["is_animated"]
                        clear_screen()
                        print(viewer.display_current(), end="", flush=True)
                        show_status(viewer)
                    except ValueError:
                        print(f"\nUnknown command: {cmd_input}", flush=True)

            # Zoom in (= for 5%, + for 10%)
            elif key == "=":
                num_buffer = ""
                if viewer.zoom_in(large=False):
                    clear_screen()
                    print(viewer.display_current(), end="", flush=True)
                    show_status(viewer)

            elif key == "+":
                num_buffer = ""
                if viewer.zoom_in(large=True):
                    clear_screen()
                    print(viewer.display_current(), end="", flush=True)
                    show_status(viewer)

            # Zoom out (- for 5%, _ for 10%)
            elif key == "-":
                num_buffer = ""
                if viewer.zoom_out(large=False):
                    clear_screen()
                    print(viewer.display_current(), end="", flush=True)
                    show_status(viewer)

            elif key == "_":
                num_buffer = ""
                if viewer.zoom_out(large=True):
                    clear_screen()
                    print(viewer.display_current(), end="", flush=True)
                    show_status(viewer)

            # Reset zoom
            elif key == "0" and num_buffer == "":
                viewer.reset_zoom()
                clear_screen()
                print(viewer.display_current(), end="", flush=True)
                show_status(viewer)

            # Help
            elif key == "?":
                num_buffer = ""
                clear_screen()
                show_help()
                get_keypress()
                clear_screen()
                print(viewer.display_current(), end="", flush=True)
                show_status(viewer)

            # Refresh (Ctrl-L only, r is removed from normal mode)
            elif key == "\x0c":  # Ctrl-L
                num_buffer = ""
                clear_screen()
                print(viewer.display_current(), end="", flush=True)
                show_status(viewer)

            # ESC - clear buffer
            elif key == "\x1b":
                num_buffer = ""

            else:
                num_buffer = ""

    except KeyboardInterrupt:
        pass
    finally:
        clear_screen()
        print(viewer.clear_display(), end="", flush=True)
        viewer.close()


if __name__ == "__main__":
    main()
