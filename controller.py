import time
from mazegen.MazeGenerator import MazeGenerator
from KeyControl import KeyControl, TerminalManager
from model import ConfigModel


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
        self.__display = None
        self.__maze = None

    def process(self):
        """Start listening to keyboard input via non-blocking poll."""
        self.__control.start()
        print("\nPress ENTER to display maze, R to regenerate, ESC to exit\n")

        try:
            while True:
                key = self.__control.poll()

                if key is not None:
                    if key == "\r" or key == "\n":  # Enter
                        print(self.__maze)
                    elif key == "r" or key == "R":  # Regenerate
                        print("Regenerating maze...")
                        self.__generator.generate_new_seed()
                        self.__generate_and_display_maze()
                    elif key == "\x1b":  # Escape
                        print("\nProgram stopped.")
                        break

                time.sleep(0.01)
        finally:
            self.__control.stop()

    def __generate_and_display_maze(self):
        """Generate maze and handle animation if in animated mode."""
        result = self.__generator.generate_maze()

        # Check if result is a generator (animated mode)
        if hasattr(result, "__iter__") and hasattr(result, "__next__"):
            # Animated mode: iterate through generator and display each step
            # Check for keyboard interrupts during animation
            self.__control.start()
            try:
                for maze_state in result:
                    # Check for keyboard input during animation
                    key = self.__control.poll()
                    if key == "\x1b":  # ESC to stop animation
                        print("\nAnimation interrupted.")
                        return
                    self.__maze = maze_state
                    print()
                    print(maze_state)
                    time.sleep(0.1)  # Small delay to see animation
            finally:
                self.__control.stop()
        else:
            # Normal mode: just store and display final maze
            self.__maze = result
            print(result)

    def __enter__(self):
        self.__generate_and_display_maze()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__terminal_manager.cleanup()
        self.__generator.create_output_file()
