"""Command-line interface for pdfcat.

This module provides the CLI entry point and interactive controls.
"""

import sys
import os
import shutil
import click
import termios
import tty
from pathlib import Path
from .viewer import PDFViewer


def parse_pages(page_spec: str, total_pages: int) -> list[int]:
    """Parse page specification string into a list of page numbers.

    Supports:
    - Single pages: "1", "5"
    - Multiple pages: "1,3,5"
    - Page ranges: "1-3", "5-10"
    - Mixed notation: "1,3-5,7"

    Args:
        page_spec: Page specification string
        total_pages: Total number of pages in the PDF

    Returns:
        Sorted list of unique page numbers (1-indexed)

    Raises:
        ValueError: If page specification is invalid or out of range
    """
    pages = set()
    parts = page_spec.split(",")

    for part in parts:
        part = part.strip()
        if not part:
            continue

        if "-" in part:
            # Page range
            try:
                start_str, end_str = part.split("-", 1)
                start = int(start_str.strip())
                end = int(end_str.strip())
            except ValueError:
                raise ValueError(f"Invalid page range: {part}")

            if start > end:
                raise ValueError(f"Invalid page range: {part} (start > end)")

            if start < 1 or end > total_pages:
                raise ValueError(
                    f"Page range {part} out of bounds (1-{total_pages})"
                )

            pages.update(range(start, end + 1))
        else:
            # Single page
            try:
                page = int(part)
            except ValueError:
                raise ValueError(f"Invalid page number: {part}")

            if page < 1 or page > total_pages:
                raise ValueError(
                    f"Page {page} out of bounds (1-{total_pages})"
                )

            pages.add(page)

    if not pages:
        raise ValueError("No valid pages specified")

    return sorted(pages)


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


def calculate_fit_size(
    target_ratio: float = 0.90,
) -> tuple[int, int]:
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
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def clear_screen():
    """Clear terminal screen."""
    print("\x1b[2J\x1b[H", end="", flush=True)


def read_line_with_escape() -> str | None:
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
                    # Erase character on screen
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
║                    pdfcat - PDF Viewer                    ║
╠═══════════════════════════════════════════════════════════╣
║  Navigation (NORMAL mode):                                ║
║    j, n, ↓, → : Next page                                 ║
║    k, p, ↑, ← : Previous page                             ║
║    gg         : Go to first page                          ║
║    G          : Go to last page                           ║
║    [n]G       : Go to page n (type number, then G)        ║
║                                                           ║
║  Zoom (NORMAL mode):                                      ║
║    =          : Zoom in (5%)                              ║
║    +          : Zoom in (10%)                             ║
║    -          : Zoom out (5%)                             ║
║    _          : Zoom out (10%)                            ║
║    0          : Reset zoom to 100%                        ║
║                                                           ║
║  Other (NORMAL mode):                                     ║
║    Ctrl-L     : Refresh current page                      ║
║    Esc        : Return to normal mode                     ║
║                                                           ║
║  Commands (type ':' to enter COMMAND mode):               ║
║    :h, :help  : Show this help                            ║
║    :r, :refresh : Refresh current page                    ║
║    :q, :quit  : Quit                                      ║
║    :[n]       : Go to page n                              ║
╚═══════════════════════════════════════════════════════════╝

Press any key to continue...
"""
    print(help_text, flush=True)


def show_status(viewer: PDFViewer, mode: str = "NORMAL", newline: bool = True):
    """Show status bar with page info.

    Args:
        viewer: PDFViewer instance
        mode: Current mode (NORMAL, COMMAND, etc.)
        newline: If True, print with leading newline (default for after page display)
    """
    info = viewer.get_page_info()
    status = (
        f"-- {mode} -- | "
        f"Page {info['current']}/{info['total']} | "
        f"Zoom: {info['zoom']:.0%}"
    )
    if newline:
        print(f"\n{status}", flush=True)
    else:
        sys.stdout.write(status)
        sys.stdout.flush()


@click.command()
@click.argument("pdf_file", type=click.Path(exists=True))
@click.option(
    "--zoom",
    "-z",
    default=1.0,
    type=float,
    help="Initial zoom level (default: 1.0)",
)
@click.option(
    "--page",
    "-p",
    default=1,
    type=int,
    help="Start at specific page (default: 1)",
)
@click.option(
    "--max-width",
    "-w",
    type=int,
    help="Maximum display width in pixels (default: 85%% of terminal)",
)
@click.option(
    "--fit",
    "-f",
    default=0.90,
    type=float,
    help="Fit to terminal ratio (0.0-1.0, default: 0.90)",
)
@click.option(
    "--pages",
    "-P",
    type=str,
    help="Output specified pages and exit (e.g., '1', '1,3,5', '1-5', '1,3-5')",
)
def main(
    pdf_file: str,
    zoom: float,
    page: int,
    max_width: int,
    fit: float,
    pages: str,
):
    """Display PDF files in terminal using Kitty graphics protocol.

    PDF_FILE: Path to the PDF file to display
    """
    # Validate PDF file
    pdf_path = Path(pdf_file)
    if not pdf_path.exists():
        click.echo(f"Error: File not found: {pdf_file}", err=True)
        sys.exit(1)

    if pdf_path.suffix.lower() != ".pdf":
        click.echo(f"Error: Not a PDF file: {pdf_file}", err=True)
        sys.exit(1)

    # Calculate display size
    if max_width is None:
        # Use terminal size with fit ratio
        calc_max_width, calc_max_height = calculate_fit_size(fit)
    else:
        calc_max_width = max_width
        calc_max_height = None

    # Initialize viewer
    try:
        viewer = PDFViewer(
            str(pdf_path),
            initial_zoom=zoom,
            max_width=calc_max_width,
            max_height=calc_max_height,
        )
    except Exception as e:
        click.echo(f"Error opening PDF: {e}", err=True)
        sys.exit(1)

    # Pages mode: output specified pages and exit (no interactive UI)
    if pages:
        try:
            page_list = parse_pages(pages, viewer.total_pages)
        except ValueError as e:
            click.echo(f"Error: {e}", err=True)
            viewer.close()
            sys.exit(1)

        try:
            for page_num in page_list:
                viewer.go_to_page(page_num)
                print(viewer.display_current_page(), end="", flush=True)
        finally:
            viewer.close()
        return

    # Set initial page
    if page > 1:
        try:
            viewer.go_to_page(page)
        except ValueError as e:
            click.echo(f"Warning: {e}. Starting at page 1.", err=True)

    # Display first page
    clear_screen()
    print(viewer.display_current_page(), end="", flush=True)
    show_status(viewer)

    # Interactive loop
    # Buffer for vim-style number prefix (e.g., "12G" to go to page 12)
    num_buffer = ""

    try:
        while True:
            key = get_keypress()

            # Accumulate number prefix for vim commands like [n]G
            if key.isdigit() and num_buffer != "":
                num_buffer += key
                continue
            elif key.isdigit() and key != "0":
                # Start accumulating number (0 alone is reset zoom)
                num_buffer = key
                continue

            # Navigation - Next page (vim: j, also n, arrows)
            if key in ("j", "n", "RIGHT", "DOWN"):
                num_buffer = ""
                if viewer.next_page():
                    clear_screen()
                    print(viewer.display_current_page(), end="", flush=True)
                    show_status(viewer)

            # Navigation - Previous page (vim: k, also p, arrows)
            elif key in ("k", "p", "LEFT", "UP"):
                num_buffer = ""
                if viewer.previous_page():
                    clear_screen()
                    print(viewer.display_current_page(), end="", flush=True)
                    show_status(viewer)

            # vim: G - go to last page, or [n]G to go to page n
            elif key == "G":
                if num_buffer:
                    # [n]G - go to page n
                    try:
                        page_num = int(num_buffer)
                        viewer.go_to_page(page_num)
                        clear_screen()
                        print(viewer.display_current_page(), end="", flush=True)
                        show_status(viewer)
                    except ValueError as e:
                        print(f"\nError: {e}", flush=True)
                else:
                    # G alone - go to last page
                    viewer.go_to_page(viewer.total_pages)
                    clear_screen()
                    print(viewer.display_current_page(), end="", flush=True)
                    show_status(viewer)
                num_buffer = ""

            # vim: gg - go to first page
            elif key == "g":
                # Wait for second 'g'
                next_key = get_keypress()
                if next_key == "g":
                    viewer.go_to_page(1)
                    clear_screen()
                    print(viewer.display_current_page(), end="", flush=True)
                    show_status(viewer)
                num_buffer = ""

            # vim-style : command mode
            elif key == ":":
                num_buffer = ""
                # Update status to COMMAND mode and show prompt
                # Move up to status line, clear it, rewrite status, then show prompt below
                sys.stdout.write("\x1b[A\r\x1b[K")  # Move up and clear status line
                show_status(viewer, "COMMAND", newline=False)
                sys.stdout.write("\n:")  # New line for command prompt
                sys.stdout.flush()

                cmd_input = read_line_with_escape()

                if cmd_input is None:
                    # Cancelled with ESC - restore status to NORMAL
                    sys.stdout.write("\r\x1b[K")  # Clear prompt line
                    sys.stdout.write("\x1b[A\r\x1b[K")  # Move up and clear status line
                    show_status(viewer, "NORMAL", newline=False)
                    sys.stdout.write("\n")  # Keep cursor below status
                    sys.stdout.flush()
                elif cmd_input == "":
                    # Empty input - restore status to NORMAL
                    sys.stdout.write("\r\x1b[K")  # Clear prompt line
                    sys.stdout.write("\x1b[A\r\x1b[K")  # Move up and clear status line
                    show_status(viewer, "NORMAL", newline=False)
                    sys.stdout.write("\n")  # Keep cursor below status
                    sys.stdout.flush()
                elif cmd_input in ("q", "quit"):
                    # Quit command
                    break
                elif cmd_input in ("h", "help"):
                    # Help command
                    clear_screen()
                    show_help()
                    get_keypress()
                    clear_screen()
                    print(viewer.display_current_page(), end="", flush=True)
                    show_status(viewer)
                elif cmd_input in ("r", "refresh"):
                    # Refresh command
                    clear_screen()
                    print(viewer.display_current_page(), end="", flush=True)
                    show_status(viewer)
                else:
                    # Try to parse as page number
                    try:
                        page_num = int(cmd_input)
                        viewer.go_to_page(page_num)
                        clear_screen()
                        print(viewer.display_current_page(), end="", flush=True)
                        show_status(viewer)
                    except ValueError:
                        print(f"\nUnknown command: {cmd_input}", flush=True)
                    except Exception as e:
                        print(f"\nError: {e}", flush=True)

            # Zoom in (= for 5%, + for 10%)
            elif key == "=":
                num_buffer = ""
                if viewer.zoom_in(large=False):
                    clear_screen()
                    print(viewer.display_current_page(), end="", flush=True)
                    show_status(viewer)

            elif key == "+":
                num_buffer = ""
                if viewer.zoom_in(large=True):
                    clear_screen()
                    print(viewer.display_current_page(), end="", flush=True)
                    show_status(viewer)

            # Zoom out (- for 5%, _ for 10%)
            elif key == "-":
                num_buffer = ""
                if viewer.zoom_out(large=False):
                    clear_screen()
                    print(viewer.display_current_page(), end="", flush=True)
                    show_status(viewer)

            elif key == "_":
                num_buffer = ""
                if viewer.zoom_out(large=True):
                    clear_screen()
                    print(viewer.display_current_page(), end="", flush=True)
                    show_status(viewer)

            # Reset zoom to 100% (vim-style 0 when no number buffer)
            elif key == "0" and num_buffer == "":
                viewer.set_zoom(1.0)
                clear_screen()
                print(viewer.display_current_page(), end="", flush=True)
                show_status(viewer)

            # Refresh (Ctrl-L only in normal mode, vim-style)
            elif key == "\x0c":  # \x0c is Ctrl-L
                num_buffer = ""
                clear_screen()
                print(viewer.display_current_page(), end="", flush=True)
                show_status(viewer)

            # ESC in normal mode - do nothing (stay in normal mode)
            elif key == "\x1b":
                pass

            else:
                # Unknown key, clear buffer
                num_buffer = ""

    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        clear_screen()
        print(viewer.clear_display(), end="", flush=True)
        viewer.close()


if __name__ == "__main__":
    main()
