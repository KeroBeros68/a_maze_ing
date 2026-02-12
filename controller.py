import time
import sys
from mazegen.MazeGenerator import MazeGenerator
from keycontrol import KeyControl, TerminalManager
from model import ConfigModel
from view import ViewFactory
from view.basic import BasicView
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
        self.__display: View = BasicView()
        self.__display_name = config.DISPLAY_MODE
        self.__maze = None
        self.__pause = False

    def process(self):
        """Start listening to keyboard input via non-blocking poll."""
        try:
            self.__display = ViewFactory.create(self.__display_name)
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
        key = self.__control.poll()
        if key is not None:
            if key in ("r", "R"):  # Regenerate
                print("Regenerating maze...")
                self.generate_and_display_maze()
            if key in ("e", "E"):  # Regenerate
                self.__generator.generate_new_seed()
                self.generate_and_display_maze()
            if key in ("p", "P", " "):
                self.__pause = not self.__pause
            if key in ("+"):
                self.more_speed()
            if key in ("-"):
                self.less_speed()
            elif key in ("\x1b", "q", "Q"):  # Escape
                print("\nProgram stopped.")
                self.__control.stop()
                sys.exit(0)

    def generate_and_display_maze(self):
        """Generate maze and handle animation if in animated mode."""
        result = self.__generator.generate_maze()

        # Check if result is a generator (animated mode)
        if hasattr(result, "__iter__") and hasattr(result, "__next__"):
            # Animated mode: iterate through generator and display each step
            # Check for keyboard interrupts during animation
            for maze_state in result:
                # Check for keyboard input during animation
                self.key_control()
                while self.__pause:
                    self.key_control()
                    time.sleep(TIME_PAUSE)
                self.__maze = maze_state
                self.__display.render(self.__maze, self.__animation_speed)
                time.sleep(1 / self.__animation_speed)
        else:
            # Normal mode: just store and display final maze
            self.__maze = result
            self.__display.render(self.__maze, self.__animation_speed)

    def more_speed(self) -> None:
        if self.__animation_speed == MAX_FPS:
            return
        if self.__animation_speed < 1:
            self.__animation_speed += 0.1
        else:
            self.__animation_speed += 1

    def less_speed(self) -> None:
        if self.__animation_speed == MIN_FPS:
            return
        self.__animation_speed -= 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__terminal_manager.cleanup()
        self.__generator.create_output_file()
