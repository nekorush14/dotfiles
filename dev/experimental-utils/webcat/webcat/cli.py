"""Command-line interface for webcat.

This module provides the CLI entry point and interactive controls.
"""

import sys
import shutil
import click
import termios
import tty
from typing import Optional

from . import __version__
from .viewer import WebViewer


def get_keypress() -> str:
    """Get a single keypress from terminal.

    Returns:
        Single character representing the key pressed
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
                elif ch3 == "Z":
                    return "SHIFT_TAB"
            return "ESC"
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def clear_screen():
    """Clear terminal screen."""
    print("\x1b[2J\x1b[H", end="", flush=True)


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


def show_help():
    """Display help message with keybindings."""
    help_text = """
╔═══════════════════════════════════════════════════════════╗
║                   webcat - Web Browser                    ║
╠═══════════════════════════════════════════════════════════╣
║  Cursor (w3m-style):                                      ║
║    h, ←       : Go back in history                        ║
║    j, ↓       : Scroll down                               ║
║    k, ↑       : Scroll up                                 ║
║    l, →       : Go forward / Follow link                  ║
║                                                           ║
║  Scrolling:                                               ║
║    d, Ctrl-D  : Half page down                            ║
║    u, Ctrl-U  : Half page up                              ║
║    Ctrl-F     : Full page down                            ║
║    Ctrl-B     : Full page up                              ║
║    gg         : Go to top                                 ║
║    G          : Go to bottom                              ║
║                                                           ║
║  Links:                                                   ║
║    f          : Enter link selection mode                 ║
║    Tab        : Select next link                          ║
║    Shift-Tab  : Select previous link                      ║
║    Enter      : Follow selected link                      ║
║    [n]        : Follow link by number                     ║
║                                                           ║
║  History:                                                 ║
║    b, H       : Go back                                   ║
║    B, L       : Go forward                                ║
║                                                           ║
║  Other:                                                   ║
║    o          : Open URL                                  ║
║    O          : Open in default browser                   ║
║    r          : Reload page                               ║
║    i          : Toggle images                             ║
║    Ctrl-L     : Refresh screen                            ║
║    ?          : Show this help                            ║
║                                                           ║
║  Commands (type ':' to enter):                            ║
║    :h, :help  : Show help                                 ║
║    :q, :quit  : Quit                                      ║
║    :o URL     : Open URL                                  ║
║    :browser   : Open in default browser                   ║
╚═══════════════════════════════════════════════════════════╝

Press any key to continue...
"""
    print(help_text, flush=True)


def show_status(viewer: WebViewer, mode: str = "NORMAL", newline: bool = True):
    """Show status bar with page info.

    Args:
        viewer: WebViewer instance
        mode: Current mode
        newline: If True, print with leading newline
    """
    info = viewer.get_status_info()
    title = info["title"][:30] + "..." if len(info["title"]) > 30 else info["title"]

    status = (
        f"-- {mode} -- | "
        f"{title} | "
        f"Line {info['scroll'] + 1}/{info['total_lines']}"
    )

    if info["selected_link"] >= 0:
        status += f" | Link [{info['selected_link'] + 1}]"

    if newline:
        print(f"\n{status}", flush=True)
    else:
        sys.stdout.write(status)
        sys.stdout.flush()


def render_page(viewer: WebViewer):
    """Render the current page view."""
    lines = viewer.get_lines()
    term_height = shutil.get_terminal_size().lines - 2  # Leave room for status

    start = viewer.scroll_position
    end = min(start + term_height, len(lines))

    for line in lines[start:end]:
        print(line)


@click.command()
@click.argument("url", required=False)
@click.option(
    "--dump",
    "-d",
    is_flag=True,
    help="Dump page content and exit (non-interactive)",
)
@click.option(
    "--raw",
    "-r",
    is_flag=True,
    help="Raw mode (no readability extraction)",
)
@click.option(
    "--no-images",
    "-I",
    is_flag=True,
    help="Disable image display",
)
@click.option(
    "--width",
    "-w",
    type=int,
    default=None,
    help="Output width (default: terminal width)",
)
@click.option(
    "--timeout",
    "-t",
    type=float,
    default=30.0,
    help="Request timeout in seconds (default: 30)",
)
@click.option(
    "--user-agent",
    "-u",
    type=str,
    default="webcat/1.0",
    help="User-Agent header (default: webcat/1.0)",
)
@click.version_option(version=__version__, prog_name="webcat")
def main(
    url: Optional[str],
    dump: bool,
    raw: bool,
    no_images: bool,
    width: Optional[int],
    timeout: float,
    user_agent: str,
):
    """Display web pages in terminal using Kitty graphics protocol.

    URL: Web page URL to display
    """
    if not url:
        if dump:
            click.echo("Error: URL is required in dump mode", err=True)
            sys.exit(1)
        click.echo("Error: URL is required", err=True)
        click.echo("Usage: webcat [OPTIONS] URL", err=True)
        sys.exit(1)

    # Initialize viewer
    try:
        viewer = WebViewer(
            width=width,
            show_images=not no_images,
            use_readability=not raw,
            timeout=timeout,
            user_agent=user_agent,
        )
    except Exception as e:
        click.echo(f"Error initializing viewer: {e}", err=True)
        sys.exit(1)

    # Load URL
    if not viewer.load_url(url):
        click.echo(f"Error: Failed to load URL: {url}", err=True)
        viewer.close()
        sys.exit(1)

    # Dump mode: output and exit
    if dump:
        try:
            print(viewer.display(), end="", flush=True)
        finally:
            viewer.close()
        return

    # Interactive mode
    clear_screen()
    render_page(viewer)
    show_status(viewer)

    # Interactive loop
    num_buffer = ""
    link_mode = False

    try:
        while True:
            key = get_keypress()

            # Accumulate number prefix
            if key.isdigit() and not link_mode:
                num_buffer += key
                continue

            # Link mode: select by number
            if link_mode and key.isdigit():
                num_buffer += key
                continue

            # Scroll down
            if key in ("j", "DOWN"):
                num_buffer = ""
                if viewer.scroll_down():
                    clear_screen()
                    render_page(viewer)
                    show_status(viewer)

            # Scroll up
            elif key in ("k", "UP"):
                num_buffer = ""
                if viewer.scroll_up():
                    clear_screen()
                    render_page(viewer)
                    show_status(viewer)

            # Half page down
            elif key in ("d", "\x04"):  # d or Ctrl-D
                num_buffer = ""
                viewer.scroll_down(viewer.SCROLL_HALF_PAGE)
                clear_screen()
                render_page(viewer)
                show_status(viewer)

            # Half page up
            elif key in ("u", "\x15"):  # u or Ctrl-U
                num_buffer = ""
                viewer.scroll_up(viewer.SCROLL_HALF_PAGE)
                clear_screen()
                render_page(viewer)
                show_status(viewer)

            # Full page down
            elif key == "\x06":  # Ctrl-F
                num_buffer = ""
                viewer.scroll_down(viewer.SCROLL_FULL_PAGE)
                clear_screen()
                render_page(viewer)
                show_status(viewer)

            # Full page up
            elif key == "\x02":  # Ctrl-B
                num_buffer = ""
                viewer.scroll_up(viewer.SCROLL_FULL_PAGE)
                clear_screen()
                render_page(viewer)
                show_status(viewer)

            # Go to bottom (G) or line [n]G
            elif key == "G":
                if num_buffer:
                    try:
                        line = int(num_buffer) - 1
                        viewer.scroll_to_line(line)
                    except ValueError:
                        pass
                else:
                    viewer.scroll_to_bottom()
                num_buffer = ""
                clear_screen()
                render_page(viewer)
                show_status(viewer)

            # Go to top (gg)
            elif key == "g":
                next_key = get_keypress()
                if next_key == "g":
                    viewer.scroll_to_top()
                    clear_screen()
                    render_page(viewer)
                    show_status(viewer)
                num_buffer = ""

            # Link mode
            elif key == "f":
                link_mode = True
                num_buffer = ""
                show_status(viewer, "LINK")

            # Exit link mode or cancel
            elif key == "ESC":
                link_mode = False
                num_buffer = ""
                show_status(viewer)

            # Tab - next link
            elif key == "\t":
                viewer.select_next_link()
                clear_screen()
                render_page(viewer)
                show_status(viewer, "LINK" if link_mode else "NORMAL")

            # Shift-Tab - previous link
            elif key == "SHIFT_TAB":
                viewer.select_previous_link()
                clear_screen()
                render_page(viewer)
                show_status(viewer, "LINK" if link_mode else "NORMAL")

            # Enter - follow link
            elif key in ("\r", "\n"):
                if link_mode and num_buffer:
                    try:
                        link_num = int(num_buffer) - 1
                        link = viewer.get_link_by_index(link_num)
                        if link:
                            viewer.load_url(link.url)
                            clear_screen()
                            render_page(viewer)
                    except ValueError:
                        pass
                elif viewer.selected_link >= 0:
                    viewer.follow_selected_link()
                    clear_screen()
                    render_page(viewer)
                link_mode = False
                num_buffer = ""
                show_status(viewer)

            # Back in history (h, b, H, LEFT)
            elif key in ("h", "b", "H", "LEFT"):
                num_buffer = ""
                if viewer.go_back():
                    clear_screen()
                    render_page(viewer)
                    show_status(viewer)

            # Forward in history or follow link (l, B, L, RIGHT)
            elif key in ("l", "B", "L", "RIGHT"):
                num_buffer = ""
                # If link is selected, follow it
                if viewer.selected_link >= 0:
                    if viewer.follow_selected_link():
                        clear_screen()
                        render_page(viewer)
                        show_status(viewer)
                # Otherwise, go forward in history
                elif viewer.go_forward():
                    clear_screen()
                    render_page(viewer)
                    show_status(viewer)

            # Open URL
            elif key == "o":
                num_buffer = ""
                sys.stdout.write("\nOpen URL: ")
                sys.stdout.flush()
                new_url = read_line_with_escape()
                if new_url:
                    if viewer.load_url(new_url):
                        clear_screen()
                        render_page(viewer)
                        show_status(viewer)
                    else:
                        print(f"\nError loading: {new_url}")
                else:
                    clear_screen()
                    render_page(viewer)
                    show_status(viewer)

            # Reload
            elif key == "r":
                num_buffer = ""
                if viewer.reload():
                    clear_screen()
                    render_page(viewer)
                    show_status(viewer)

            # Toggle images
            elif key == "i":
                num_buffer = ""
                viewer.toggle_images()
                clear_screen()
                render_page(viewer)
                show_status(viewer)

            # Open in default browser
            elif key == "O":
                num_buffer = ""
                if viewer.selected_link >= 0:
                    # Open selected link in browser
                    viewer.open_link_in_browser()
                else:
                    # Open current page in browser
                    viewer.open_in_browser()
                clear_screen()
                render_page(viewer)
                show_status(viewer)

            # Refresh screen
            elif key == "\x0c":  # Ctrl-L
                num_buffer = ""
                clear_screen()
                render_page(viewer)
                show_status(viewer)

            # Help
            elif key == "?":
                num_buffer = ""
                clear_screen()
                show_help()
                get_keypress()
                clear_screen()
                render_page(viewer)
                show_status(viewer)

            # Command mode
            elif key == ":":
                num_buffer = ""
                sys.stdout.write("\n:")
                sys.stdout.flush()

                cmd_input = read_line_with_escape()

                if cmd_input is None:
                    clear_screen()
                    render_page(viewer)
                    show_status(viewer)
                elif cmd_input in ("q", "quit"):
                    break
                elif cmd_input in ("h", "help"):
                    clear_screen()
                    show_help()
                    get_keypress()
                    clear_screen()
                    render_page(viewer)
                    show_status(viewer)
                elif cmd_input.startswith("o "):
                    new_url = cmd_input[2:].strip()
                    if new_url and viewer.load_url(new_url):
                        clear_screen()
                        render_page(viewer)
                        show_status(viewer)
                    else:
                        print(f"\nError loading: {new_url}")
                elif cmd_input == "browser":
                    if viewer.selected_link >= 0:
                        viewer.open_link_in_browser()
                    else:
                        viewer.open_in_browser()
                    clear_screen()
                    render_page(viewer)
                    show_status(viewer)
                else:
                    print(f"\nUnknown command: {cmd_input}")

            # Quit with q
            elif key == "q":
                break

            else:
                num_buffer = ""

    except KeyboardInterrupt:
        pass
    finally:
        clear_screen()
        viewer.close()


if __name__ == "__main__":
    main()
