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
        self.__generator: MazeGenerator = MazeGenerator(config.WIDTH,
                                                        config.HEIGHT,
                                                        config.ENTRY,
                                                        config.EXIT,
                                                        config.OUTPUT_FILE,
                                                        config.SEED,
                                                        config.ALGORITHM)
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
                        self.__maze = self.__generator.generate_maze()
                        print(self.__maze)
                    elif key == "\x1b":  # Escape
                        print("\nProgram stopped.")
                        break

                time.sleep(0.01)  # Small delay to prevent tight loop
        finally:
            self.__control.stop()

    def __enter__(self):
        self.__maze = self.__generator.generate_maze()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__terminal_manager.cleanup()
        self.__generator.create_output_file()
