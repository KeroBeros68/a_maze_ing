*This project has been created as part of the 42 curriculum by kebertra.*

# A-Maze-ing

## Description

A-Maze-ing is a procedural maze generator written in Python 3.13. It generates random mazes from a configuration file, renders them visually in the terminal, and writes the result — including the shortest path — to an output file in hexadecimal format.

The project features:
- Two generation algorithms: **Recursive Backtracking (DFS)** and **Prim's algorithm**
- Support for **perfect mazes** (single path between entry and exit) and **imperfect mazes** (multiple paths)
- Embedded **"42" logo** carved directly into the maze structure
- **Animated generation** with live terminal rendering
- **Interactive TTY mode**: show/hide path, change colors, control speed, play through the maze
- A fully reusable `mazegen` module, ready to be packaged and installed via pip

---

## Instructions

### Requirements

- Python 3.13 or higher
- [Poetry](https://python-poetry.org/) (recommended) or pip

### Installation

```bash
make install
```

This sets up a virtual environment and installs all dependencies via Poetry.

### Running

```bash
make run
```

Or directly:

```bash
python3 a_maze_ing.py config.txt
```

### Debug mode

```bash
make debug
```

### Linting

```bash
make lint         # flake8 + mypy (standard flags)
make lint-strict  # flake8 + mypy --strict
```

### Cleanup

```bash
make clean
```

---

## Configuration File Format

The program takes a single argument: the path to a configuration file.

```
python3 a_maze_ing.py config.txt
```

**Mandatory keys:**

| Key           | Description                              | Example              |
|---------------|------------------------------------------|----------------------|
| `WIDTH`       | Maze width in cells                      | `WIDTH=60`           |
| `HEIGHT`      | Maze height in cells                     | `HEIGHT=25`          |
| `ENTRY`       | Entry coordinates (x, y)                | `ENTRY=[1, 1]`       |
| `EXIT`        | Exit coordinates (x, y)                 | `EXIT=[59, 24]`      |
| `OUTPUT_FILE` | Output filename                          | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | Generate a perfect maze (true/false)     | `PERFECT=true`       |

**Optional keys:**

| Key            | Description                                            | Default         |
|----------------|--------------------------------------------------------|-----------------|
| `ALGORITHM`    | Generation algorithm (`backtracking` or `prim`)        | `backtracking`  |
| `SEED`         | Reproducibility seed (any string)                      | Random          |
| `MODE_GEN`     | Generation mode (`static` or `animated`)               | `static`        |
| `DISPLAY_MODE` | Display mode (`basic` or `tty`)                        | `basic`         |
| `STAMP_TYPE`   | Logo stamp to embed (`42vanilla` or `42custom`)        | `42vanilla`     |

Lines starting with `#` are treated as comments and ignored.

**Example `config.txt`:**

```
WIDTH=60
HEIGHT=25
ENTRY=[1, 1]
EXIT=[59, 24]
OUTPUT_FILE=maze.txt
PERFECT=false
ALGORITHM=prim
SEED=MYREPRODUCIBLESEED
MODE_GEN=animated
DISPLAY_MODE=tty
STAMP_TYPE=42vanilla
```

---

## Output File Format

Each cell is encoded as one hexadecimal digit representing its closed walls:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1       | East  |
| 2       | South |
| 3       | West  |

The file is structured as follows:

```
<hex grid, one row per line>

<entry x,y>
<exit x,y>
<shortest path: sequence of N/E/S/W>
```

---

## Visual Representation & User Interactions

### Basic mode (`DISPLAY_MODE=basic`)
Simple ASCII rendering of the maze.

### TTY mode (`DISPLAY_MODE=tty`)
Advanced terminal rendering with ANSI colors, lighting effects, and full interactivity.

**Key bindings (TTY mode):**

| Key       | Action                                      |
|-----------|---------------------------------------------|
| `R`       | Regenerate maze with new random seed        |
| `E`       | Regenerate maze with new computed seed      |
| `F`       | Show / Hide shortest path                   |
| `C` / `V` | Cycle wall colors                           |
| `P` / Space | Pause / Resume animation                  |
| `+` / `-` | Increase / Decrease animation speed         |
| `G`       | Toggle interactive game mode                |
| `W/A/S/D` | Move player through the maze (game mode)   |
| `ESC`     | Quit                                        |

---

## Algorithm Choice

### Recursive Backtracking (DFS)

A depth-first search algorithm that carves passages by pushing/popping cells on a stack. It creates mazes with long, winding corridors and a single solution path when run in perfect mode.

**Why:** Simple to implement, reliably produces perfect mazes, easy to animate step by step.

### Prim's Algorithm

A minimum spanning tree approach using a frontier set. It picks random frontier cells and connects them to the visited area. Produces more "open" mazes with shorter, wider corridors.

**Why:** Produces better distributed mazes (more balanced than DFS), good contrast for visual comparison.

Both algorithms support the **UnPerfect** pass: after generating a perfect maze, a configurable number of walls are removed to introduce loops (`PERFECT=false`).

---

## Reusable Module: `mazegen`

The `mazegen` package is a standalone maze generation module with no dependency on the view layer.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage

```python
from mazegen.model import ConfigModel
from mazegen.MazeGenerator import MazeGenerator

config = ConfigModel(
    WIDTH=60,
    HEIGHT=25,
    ENTRY=(1, 1),
    EXIT=(59, 24),
    OUTPUT_FILE="maze.txt",
    PERFECT=True,
    ALGORITHM="prim",
    SEED="myseed",
    STAMP_TYPE="42vanilla"
)

generator = MazeGenerator(config)
maze = generator.generate_maze()

print(maze)                   # Hex grid as string
print(maze.shortest_path)     # e.g. "EESSWWN..."
```

### Animated (generator-based)

```python
for partial_maze in generator.generate_maze_animated():
    print(partial_maze)   # Each step of the generation
```

### Accessing the maze structure

```python
cell = maze.maze_grid[y][x]
print(cell.view_cell())   # Hex digit for that cell
print(cell.north)         # True if north wall is closed
print(cell.is_entry)      # True if entry cell
```

### Custom algorithms

```python
from mazegen.algorithms.algorithm import MazeAlgorithm
from mazegen.algorithms.factory import AlgorithmFactory

class MyAlgorithm(MazeAlgorithm):
    def generate(self, maze):
        pass  # Implement here

AlgorithmFactory.register("mine", MyAlgorithm)
```

### Custom stamps

```python
from mazegen.stamp.stamp_design import StampDesign
from mazegen.stamp.stamp_factory import StampFactory

class MyStamp(StampDesign):
    def get_logo(self, size):
        return ["XXX", "XXX", "XXX"]
    def get_available_sizes(self):
        return [3]

StampFactory.register("mystamp", MyStamp)
```

### Building the package

```bash
poetry build
# Generates mazegen-*.whl and mazegen-*.tar.gz in dist/
```

---

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracker (DFS)](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search)
- [Prim's algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [Python typing module](https://docs.python.org/3/library/typing.html)

**AI usage:**
GitHub Copilot (Claude Sonnet) was used during development for:
- Generating and updating English docstrings across all files
- Refactoring the Stamp class to a factory pattern
- Migrating MazeGenerator from individual parameters to a single ConfigModel
- Suggesting fixes for import paths after directory restructuring
- Code reviews and feedback on architecture

---

## Team & Project Management

**Team:** Solo project — kebertra (Kevin Bertrand)

**Roles:** Full-stack — architecture, generation algorithms, TTY view, configuration, packaging

**Planning evolution:**
- Week 1: Core maze structure (Cell, Maze), backtracking algorithm, hex output
- Week 2: Prim's algorithm, PERFECT flag, pathfinder (BFS), "42" stamp
- Week 3: TTY view, animations, interactive controls, factory patterns
- Week 4: Refactoring, Pydantic config, reusable mazegen module, documentation

**What worked well:**
- Factory pattern for algorithms and stamps: easy to extend
- Pydantic for configuration validation: catches errors early with clear messages
- Generator-based animation: decouples rendering from generation cleanly

**What could be improved:**
- MLX graphical view was not implemented
- Unit tests are absent (verified manually)
- Border validation for entry/exit could be more explicit

**Tools used:**
- VS Code + GitHub Copilot (AI pair programming)
- Poetry for dependency management and packaging
- mypy + flake8 for static analysis
- Git for version control
