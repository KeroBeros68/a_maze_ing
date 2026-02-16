"""Main controller for maze generation application.

This module manages the interaction between the user and the maze generation
system, handling keyboard input, animation speed control, and display updates.

Classes:
    Controller: Main controller orchestrating maze generation
    and user interaction
"""

import time
import sys
from typing import Optional
from mazegen.MazeGenerator import MazeGenerator
from keycontrol import KeyControl, TerminalManager
from mazegen.maze.maze import Maze
from model import ConfigModel
from view import ViewFactory
from view.basic import BasicView
from view.tty import TtyView
from view.View import View


TIME_PAUSE = 0.05

BASE_FPS = 30
MAX_FPS = 120
MIN_FPS = 1


class Controller:
    """
    Controls the maze generation and user interaction.

    Uses KeyControl for non-blocking keyboard input via select().
    """

    def __init__(self, config: ConfigModel):
        self.__config: ConfigModel = config
        self.__terminal_manager: TerminalManager = TerminalManager()
        self.__control: KeyControl = KeyControl(self.__terminal_manager)
        self.__generator: MazeGenerator = MazeGenerator(
            config.WIDTH,
            config.HEIGHT,
            config.ENTRY,
            config.EXIT,
            config.OUTPUT_FILE,
            config.SEED,
            config.ALGORITHM,
            config.MODE_GEN,
        )
        self.__animation_speed = BASE_FPS
        self.__display: View =  TtyView(self.__config)
        self.__display_name = config.DISPLAY_MODE
        self.__maze: Optional[Maze] = None
        self.__pause = False
        self.__restart = False  # to remove later

    def process(self) -> None:
        """Start listening to keyboard input via non-blocking poll."""
        try:
            self.__display = ViewFactory.create(self.__display_name, self.__config)
        except ValueError as e:
            sys.stderr.write(f"Error: {e}\n")
            raise
        self.__control.start()
        print("\33[2J")
        self.generate_and_display_maze()
        while True:
            self.key_control()
            time.sleep(0.01)

    def key_control(self) -> None:
        """Handle keyboard input for maze control.

        Processes keyboard commands:
        - r: Regenerate maze
        - e: Generate new seed
        - p/space: Pause/unpause animation
        - +: Increase animation speed
        - -: Decrease animation speed
        - q/esc: Quit application
        """
        key = self.__control.poll()
        if key is not None:
            if key in ("r", "R"):  # Regenerate
#                print("Regenerating maze...")
                self.__maze.done_gen = False
                self.__restart = True
                self.generate_and_display_maze()
            if key in ("e", "E"):  # Regenerate
                self.__generator.generate_new_seed()
                self.__maze.done_gen = False
                self.__restart = True
                self.generate_and_display_maze()
            if key in ("p", "P", " "):
                self.__pause = not self.__pause
                if self.__pause:
                    self.__display.paused = 1
                    if self.__config.DISPLAY_MODE == "tty":
                        self.__display.render(self.__maze, self.__animation_speed, count_as_step = 0)
                else:
                    self.__display.paused = 0
            if key in ("+"):
                self.__more_speed()
            if key in ("-"):
                self.__less_speed()
            if key in ("C", "c"):
                self.__change_color(-1)
            if key in ("V", "v"):
                self.__change_color(1)
            elif key in ("\x1b", "q", "Q"):  # Escape
                if self.__config.DISPLAY_MODE != "tty":
                    print("\nProgram stopped.")
                self.__control.stop()
                sys.exit(0)

    def generate_and_display_maze(self) -> None:
        """Generate and display the maze with animation.

        Orchestrates maze generation and rendering, supporting both
        animated and non-animated modes with pause capability.
        Handles keyboard input during animation for speed/pause control.
        """
        result = self.__generator.generate_maze()

        # Always iterate through the generator
        for maze_state in result:
            # Check for keyboard input during animation
            self.key_control()
            while self.__pause:
                self.key_control()
                time.sleep(TIME_PAUSE)
            self.__maze = maze_state
            self.__maze.restart = self.__restart
            self.__display.render(self.__maze, self.__animation_speed)
            self.__restart = False
            animation_speed = 1 / self.__animation_speed
            self.__reactive_sleep(animation_speed)

    def __reactive_sleep(self, duration: float) -> None:
        """Sleep while remaining responsive to keyboard input.

        Provides a non-blocking sleep that periodically checks for keyboard
        input to ensure responsiveness during animation delays.

        Args:
            duration: Duration to sleep in seconds
        """
        start_time = time.time()
        while time.time() - start_time < duration:
            self.key_control()
            time.sleep(0.01)

    def __more_speed(self) -> None:
        """Increase animation speed (up to MAX_FPS)."""
        if self.__animation_speed == MAX_FPS:
            return
        self.__animation_speed += 1

    def __less_speed(self) -> None:
        """Decrease animation speed (down to MIN_FPS)."""
        if self.__animation_speed == MIN_FPS:
            return
        self.__animation_speed -= 1

    def __change_color(self, value: int) -> None:
        self.__display.change_color(value)
        self.__display.render(self.__maze, self.__animation_speed, count_as_step = 0)

    def __enter__(self) -> "Controller":
        return self

    def __exit__(
        self, exc_type: object, exc_val: object, exc_tb: object
    ) -> None:
        self.__terminal_manager.cleanup()
        self.__generator.create_output_file()
