"""Main controller for maze generation application.

This module manages the interaction between the user and the maze generation
system, handling keyboard input, animation speed control, and display updates.

Classes:
    Controller: Main controller orchestrating maze generation
    and user interaction
"""

import time
import sys
from mazegen.MazeGenerator import MazeGenerator
from keycontrol import KeyControl, TerminalManager
from mazegen.maze.maze import Maze
from mazegen.pathfinder.pathfinder import PathFinder
from mazegen.model import ConfigModel
from view import ViewFactory
from view.tty import TtyView  # noqa F401
from view.View import View


TIME_PAUSE = 0.05

BASE_FPS = 30
MAX_FPS = 120
MIN_FPS = 1


class Controller:
    """
    Controls the maze generation and user interaction.

    Uses KeyControl for non-blocking keyboard input via select().
    Manages the complete lifecycle of maze generation, display, and user input.
    """

    def __init__(self, config: ConfigModel):
        """Initialize the controller with configuration.

        Args:
            config: ConfigModel with all maze generation settings
        """
        self.__config: ConfigModel = config
        self.__terminal_manager: TerminalManager = TerminalManager()
        self.__control: KeyControl = KeyControl(self.__terminal_manager)
        self.__generator: MazeGenerator = MazeGenerator(config)
        self.__animation_speed = BASE_FPS
        self.__display: View = TtyView(self.__config)
        self.__display_name = config.DISPLAY_MODE
        self.__algorithm = config.ALGORITHM
        self.__pause = False
        self.__restart = False  # to remove later

    def process(self) -> None:
        """Start the main event loop for maze generation and display.

        Initializes the display, starts keyboard input monitoring, generates
        the initial maze, solves it, and enters the main event loop for
        handling user input.
        """
        try:
            self.__display = ViewFactory.create(self.__display_name,
                                                self.__config)
        except ValueError as e:
            sys.stderr.write(f"Error: {e}\n")
            raise
        self.__control.start()
        print("\33[48;2;0;0;0m\33[2J")
        self.pathfinder = PathFinder()
        self.generate_and_display_maze()
        self.solve_path()
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
                self.__maze.gen_step = 0
                self.__restart = True
                self.generate_and_display_maze()
            if key in ("e", "E"):  # Regenerate
                self.__generator.generate_new_seed()
                self.__maze.gen_step = 0
                self.__restart = True
                self.generate_and_display_maze()
                self.pathfinder.solve_shortest_path(self.__maze)
            if key in ("p", "P", " ") and self.__maze.gen_step != 9:
                self.__pause = not self.__pause
                if self.__pause:
                    self.__display.paused = True
                    if self.__config.DISPLAY_MODE == "tty":
                        self.__display.render(self.__maze,
                                              self.__animation_speed,
                                              self.__algorithm,
                                              self.__generator.get_seed(),
                                              count_as_step=0)
                else:
                    self.__display.paused = False
            if key in ("+"):
                self.__more_speed()
            if key in ("-"):
                self.__less_speed()
            if key in ("C", "c"):
                self.__change_color(-1)
            if key in ("V", "v"):
                self.__change_color(1)
            if (key in ("F", "f") and 9 > self.__maze.gen_step >= 3):
                if self.__maze.gen_step == 4 or self.__maze.gen_step == 5:
                    self.__maze.gen_step = 6
                else:
                    self.__maze.gen_step = 4
                self.__display.render(self.__maze, self.__animation_speed,
                                      self.__algorithm,
                                      self.__generator.get_seed(),
                                      count_as_step=0)
            if (key in ("G", "g") and self.__maze.gen_step >= 3):
                if self.__maze.gen_step != 9:
                    self.__maze.gen_step = 9
                else:
                    self.__maze.gen_step = 3
                self.__display.render(self.__maze, self.__animation_speed,
                                      self.__algorithm,
                                      self.__generator.get_seed(),
                                      count_as_step=0, key=None)
            if (key in ("W", "w", "A", "a", "S", "s", "D", "d", "Z", "z",
                        "Q", "q") and self.__maze.gen_step == 9):
                self.__display.render(self.__maze, self.__animation_speed,
                                      self.__algorithm,
                                      self.__generator.get_seed(),
                                      count_as_step=0, key=key.capitalize())
            if key in ("\x1b"):  # Escape
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
            self.__maze: Maze = maze_state
            self.__maze.restart = self.__restart
            self.__display.render(self.__maze, self.__animation_speed,
                                  self.__algorithm,
                                  self.__generator.get_seed())
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
        """Increase animation speed up to maximum FPS."""
        if self.__animation_speed == MAX_FPS:
            return
        self.__animation_speed += 1

    def __less_speed(self) -> None:
        """Decrease animation speed down to minimum FPS."""
        if self.__animation_speed == MIN_FPS:
            return
        self.__animation_speed -= 1

    def __change_color(self, value: int) -> None:
        """Change the maze display color.

        Args:
            value: -1 for previous color, 1 for next color
        """
        self.__display.change_color(value)
        self.__display.render(self.__maze, self.__animation_speed,
                              self.__algorithm,
                              self.__generator.get_seed(), count_as_step=0)

    def solve_path(self) -> None:
        """Find and store the shortest path through the maze."""
        self.pathfinder.solve_shortest_path(self.__maze)

    def __enter__(self) -> "Controller":
        return self

    def __exit__(
        self, exc_type: object, exc_val: object, exc_tb: object
    ) -> None:
        self.__terminal_manager.cleanup()
        self.__generator.create_output_file()
