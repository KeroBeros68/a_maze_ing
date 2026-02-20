"""Non-blocking keyboard input handling for terminal applications.

This module provides terminal state management and non-blocking keyboard
input functionality for Unix/Linux systems. It handles terminal
configuration and restoration with signal handling for clean shutdown.

Classes:
    KeyControlError: Exception for keyboard control errors
    TerminalManager: Manages terminal state configuration
    KeyControl: Non-blocking keyboard input handler
"""

import sys
import signal
import termios
import tty
import select
import os
import atexit
from typing import Any, Optional

# ANSI escape codes
CURSOR_SHOW = "\33[?25h"
COLOR_RESET = "\33[48;2;0;0;0m\33[37m"
RESET_FORMATTING = "\33[0m"


class KeyControlError(Exception):
    """Exception raised during keyboard control errors."""

    pass


class TerminalManager:
    """
    Manages terminal state configuration and restoration.

    Single Responsibility: Handle all terminal state operations.
    Responsible for saving, applying, and restoring terminal settings.
    Ensures proper cleanup even in case of program crash via atexit.
    """

    def __init__(self) -> None:
        self.fd: Optional[int] = None
        self.old: Optional[list] = None
        # Register cleanup to run on program exit (crash, exception, etc.)
        atexit.register(self.cleanup)

    def setup(self) -> None:
        """
        Configure terminal for raw keyboard input.

        Switches to cbreak mode for immediate key availability.

        Raises:
            KeyControlError: If terminal configuration fails.
        """
        try:
            self.fd = sys.stdin.fileno()
            self.old = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
        except (termios.error, OSError) as e:
            raise KeyControlError(f"Unable to configure terminal: {e}") from e

    def restore(self) -> None:
        """
        Restore terminal to original state.

        Raises:
            KeyControlError: If restoration fails.
        """
        if self.fd is None or self.old is None:
            raise KeyControlError("Invalid terminal state")

        try:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)
        except termios.error as e:
            raise KeyControlError(
                f"Error during terminal restoration: {e}"
            ) from e

    def cleanup(self) -> None:
        """
        Forcefully clean the terminal state.

        Fallback method when termios restoration isn't available.
        Shows cursor and resets formatting.
        Called automatically via atexit on program termination.
        """
        try:
            # Restore via termios if possible (cleaner approach)
            if self.old is not None and self.fd is not None:
                termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)
        except (termios.error, OSError):
            # Fallback: use stty as last resort
            os.system("stty sane")

        # Show cursor and reset formatting
        sys.stdout.write(f"{CURSOR_SHOW}{COLOR_RESET}{RESET_FORMATTING}\n")
        sys.stdout.flush()


class KeyControl:
    """
    Non-blocking keyboard input handler for Unix/Linux terminals.

    Allows reading pressed keys in real-time without blocking program
    execution.
    Manages keyboard input while delegating terminal state management to
    TerminalManager.

    Single Responsibility: Handle keyboard input only.

    Can be used as a context manager:
        terminal_mgr = TerminalManager()
        with KeyControl(terminal_mgr) as control:
            while True:
                key = control.poll()
    """

    def __init__(self, terminal_manager: TerminalManager) -> None:
        self.terminal = terminal_manager
        self.enabled: bool = False
        self._setup_signal_handlers()

    def _setup_signal_handlers(self) -> None:
        """Configure signal handlers for clean program termination."""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum: int, frame: Any) -> None:
        """Signal handler for clean program shutdown."""
        self.exit_program()

    def start(self) -> None:
        """
        Enable non-blocking keyboard input mode.

        Delegates terminal setup to TerminalManager.

        Raises:
            KeyControlError: If terminal setup fails.
        """
        if self.enabled:
            return

        self.terminal.setup()
        self.enabled = True

    def stop(self) -> None:
        """
        Disable keyboard input mode and restore terminal.

        Delegates terminal restoration to TerminalManager.

        Raises:
            KeyControlError: If restoration fails.
        """
        if not self.enabled:
            return

        self.terminal.restore()
        self.enabled = False

    def poll(self) -> Optional[str]:
        """
        Check if a key is pressed without blocking.

        Returns:
            The pressed character, or None if no input is available.

        Raises:
            KeyControlError: If control is not enabled.
        """
        if not self.enabled:
            raise KeyControlError(
                "KeyControl is not enabled. Call start() first."
            )

        try:
            r, _, _ = select.select([sys.stdin], [], [], 0)
            if r:
                return sys.stdin.read(1)
            return None
        except (OSError, select.error) as e:
            raise KeyControlError(f"Error during read: {e}") from e

    def exit_program(self, code: int = 0) -> None:
        """
        Exit the program cleanly by restoring the terminal.

        Args:
            code: Exit code (default: 0).
        """
        try:
            self.stop()
        finally:
            self.terminal.cleanup()
            sys.exit(code)

    def __enter__(self) -> "KeyControl":
        """Enter the context manager."""
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the context manager."""
        try:
            self.stop()
        finally:
            self.terminal.cleanup()


if __name__ == "__main__":
    """Test script for KeyControl."""
    import time

    print("KeyControl Test - Press keys (q to quit)")
    print("Timeout: 10 seconds\n")

    # Create terminal manager and pass it to KeyControl
    terminal_manager = TerminalManager()
    control = KeyControl(terminal_manager)

    try:
        control.start()
        print("✓ Keyboard input mode enabled")
        print("Press any key...\n")

        start_time = time.time()
        timeout = 10

        while time.time() - start_time < timeout:
            key = control.poll()

            if key is not None:
                if key == "q":
                    print("Quit requested")
                    break
                elif key == "\x03":  # Ctrl+C
                    print("\nCtrl+C detected")
                    break
                elif ord(key) == 27:  # Escape
                    print("Escape detected")
                    break
                else:
                    print(f"Key pressed: '{key}' (code: {ord(key)})")

            time.sleep(0.05)  # Small delay to prevent tight loop

        print("\n✓ Test completed")

    except KeyControlError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        terminal_manager.cleanup()
        print("✓ Terminal restored")
