# Mazegen - Maze Generation Library

A powerful, modular Python library for procedural maze generation with support for multiple algorithms, customizable stamp designs, and reproducible generation.

## Features

- **Multiple Algorithms**: Backtracking and Prim's algorithm for maze generation
- **Perfect & Imperfect Mazes**: Generate perfect mazes (no loops) or mazes with cycles
- **Stamp Designs**: Embed logos into mazes (42 with vanilla/custom variants)
- **Reproducible Generation**: Use seeds for consistent maze generation
- **Configurable**: Full control over maze dimensions, entry/exit points, and generation parameters
- **Extensible**: Factory pattern allows adding custom algorithms and stamp designs

## Installation

### Requirements
- Python 3.10 or higher
- pydantic >= 2.0
- pydantic-settings >= 2.0

### Setup

```bash
pip install pydantic pydantic-settings
```

## Quick Start

### Basic Usage

```python
from mazegen.model import ConfigModel
from mazegen.MazeGenerator import MazeGenerator

# Create configuration
config = ConfigModel(
    WIDTH=60,
    HEIGHT=25,
    ENTRY=(1, 1),
    EXIT=(59, 24),
    OUTPUT_FILE="maze.txt",
    ALGORITHM="prim",
    STAMP_TYPE="42vanilla",
    PERFECT=True,
    SEED="my_seed"
)

# Generate maze
generator = MazeGenerator(config)
maze = generator.generate_maze()
print(maze)
```

### Configuration Parameters

- **WIDTH** (int, 2-200): Maze width in cells
- **HEIGHT** (int, 2-200): Maze height in cells
- **ENTRY** (tuple[int, int]): Entry point coordinates (x, y)
- **EXIT** (tuple[int, int]): Exit point coordinates (x, y)
- **OUTPUT_FILE** (str): Output filename for the maze
- **ALGORITHM** (str): Algorithm to use ("backtracking" or "prim")
- **STAMP_TYPE** (str): Logo stamp design ("42vanilla" or "42custom", default: "42vanilla")
- **PERFECT** (bool): Generate perfect maze without loops (default: True)
- **MODE_GEN** (str): Generation mode ("static" or "animated", default: "static")
- **DISPLAY_MODE** (str): Display mode ("basic", "tty", or "mlx", default: "basic")
- **SEED** (str, optional): Random seed for reproducible generation

## Core Classes

### MazeGenerator

Main class for orchestrating maze generation.

```python
from mazegen.MazeGenerator import MazeGenerator
from mazegen.model import ConfigModel

generator = MazeGenerator(config)
maze = generator.generate_maze()
```

### Maze

Represents the maze grid structure with cells and walls.

```python
from mazegen.maze import Maze
maze = Maze(width=60, height=25)
```

### AlgorithmFactory

Factory for creating maze generation algorithms and registering new algorithms..

```python
from mazegen.algorithms.factory import AlgorithmFactory

algo = AlgorithmFactory.create("prim")
```

### StampFactory

Factory for creating and registering stamp designs.

```python
from mazegen.stamp.stamp_factory import StampFactory

# Create a stamp design
design = StampFactory.create("42vanilla")

# Register custom stamp
class CustomStamp(StampDesign):
    def get_logo(self, size):
        return [["X", "X"], ["X", "X"]]
    def get_available_sizes(self):
        return [2]

StampFactory.register("custom", CustomStamp)
```

## Available Stamp Designs

### 42 Logo Variants
- **42vanilla**: 42 logo using the built-in vanilla style
- **42custom**: 42 logo using a custom user-defined style

## Available Algorithms

- **backtracking**: Recursive backtracking algorithm (good for creating mazes with long paths)
- **prim**: Prim's algorithm (creates well-balanced mazes with good distribution)

## Architecture

```
mazegen/
├── algorithms/          # Maze generation algorithms
│   ├── algorithm.py    # Abstract base class
│   ├── backtracking.py # Backtracking implementation
│   ├── prim.py         # Prim's algorithm
│   └── factory.py      # Algorithm factory
├── cell/               # Cell structure
├── error/              # Exception classes
│   └── MazeError.py    # MazeError and StampError
├── maze/               # Maze grid management
├── model/              # Configuration model (Pydantic)
├── pathfinder/         # Pathfinding utilities
├── stamp/              # Logo stamping system
│   ├── stamp_design.py # Abstract stamp base
│   ├── forty_two_stamp.py  # 42 logo implementation
│   └── stamp_factory.py    # Stamp factory
├── utils/              # Utility functions
└── MazeGenerator.py    # Main generator class
```

## Error Handling

The package exposes two exception classes for fine-grained error handling:

- **`MazeError`**: Base exception for all mazegen errors
- **`StampError`**: Raised for stamp-related failures (invalid dimensions, unsupported format, etc.)

```python
from mazegen import MazeError, StampError

try:
    generator = MazeGenerator(config)
except StampError as e:
    print(f"Stamp error: {e}")
except MazeError as e:
    print(f"Maze error: {e}")
except RuntimeError as e:
    print(f"Failed to initialize: {e}")
```

## Creating Custom Stamp Designs

```python
from mazegen.stamp.stamp_design import StampDesign
from mazegen.stamp.stamp_factory import StampFactory

class MyStamp(StampDesign):
    def get_logo(self, size: int) -> list[str]:
        if size <= 5:
            return ["XXX", "XXX", "XXX"]
        else:
            return ["XXXXX", "XXXXX", "XXXXX", "XXXXX", "XXXXX"]
    
    def get_available_sizes(self) -> list[int]:
        return [3, 5]

# Register the custom stamp
StampFactory.register("mystamp", MyStamp)

# Use it in configuration
config.STAMP_TYPE = "mystamp"
```

## Creating Custom Algorithms

```python
from mazegen.algorithms.algorithm import MazeAlgorithm
from mazegen.algorithms.factory import AlgorithmFactory
from mazegen.maze import Maze
from mazegen.cell import Cell

class MyAlgorithm(MazeAlgorithm):
    def generate(self, maze: Maze) -> None:
        """Implement your custom maze generation algorithm."""
        # Your algorithm implementation here
        pass

# Register the custom algorithm
AlgorithmFactory.register("myalgo", MyAlgorithm)

# Use it in configuration
config = ConfigModel(
    WIDTH=60,
    HEIGHT=25,
    ENTRY=(1, 1),
    EXIT=(59, 24),
    OUTPUT_FILE="maze.txt",
    ALGORITHM="myalgo"  # Use your custom algorithm
)
```

## Extensibility

Both `AlgorithmFactory` and `StampFactory` provide registration methods to easily extend the library:

### AlgorithmFactory Methods

- `create(algorithm_name)`: Create an algorithm instance by name
- `register(name, algorithm_class)`: Register a custom algorithm
- `get_available_algorithms()`: Get list of available algorithm names

### StampFactory Methods

- `create(design_name)`: Create a stamp design instance by name
- `register(name, design_class)`: Register a custom stamp design
- `get_available_designs()`: Get list of available stamp design names

## Configuration File (config.txt)

The library can load configuration from a `config.txt` file:

```
WIDTH=60
HEIGHT=25
ENTRY=[1, 1]
EXIT=[59, 24]
OUTPUT_FILE=maze.txt
PERFECT=true
ALGORITHM=prim
STAMP_TYPE=42vanilla
MODE_GEN=static
DISPLAY_MODE=tty
SEED=my_seed
```

Then load with:

```python
from mazegen.model import ConfigModel
config = ConfigModel(_env_file="config.txt")
```

## Performance Notes

- **Prim's Algorithm**: Generally faster, produces well-distributed mazes
- **Backtracking**: Slightly slower, creates mazes with longer paths
- **Seed Generation**: Reproducible results with the same seed
- **Stamp Placement**: Uses dynamic programming for optimal placement

## License

Part of the A Maze'ing project (42 School curriculum)

## Author

Orobert Kebertra
