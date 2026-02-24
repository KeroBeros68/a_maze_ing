*This project has been created as part of the 42 curriculum by kebertra, orobert.*

# A-Maze-ing 🧩🌀

## Description 📌

A-Maze-ing is a procedural maze generator written in **Python 3.13+**. It generates random mazes from a configuration file, renders them in the terminal (basic ASCII or advanced TTY mode), and writes the result — including the **shortest path** — to an output file in **hexadecimal** format.

The project also includes a reusable library, **`mazegen`**, designed to be imported and extended independently from the UI/rendering layer.

### Features (Advanced) ✨

- 🧠 Multiple algorithms: **Recursive Backtracking (DFS)** and **Prim’s algorithm**
- ✅ **Perfect** mazes (single unique path) and 🔁 **Imperfect** mazes (loops)
- 🏷️ Embedded **"42"** logo carved into the maze structure via a stamp system
- 🎞️ **Static** or **Animated** generation
- 🖥️ Two display modes:
  - `basic`: simple ASCII rendering
  - `tty`: advanced rendering with ANSI colors + interactivity (speed, colors, path toggle, game mode)
- 🧭 Shortest-path extraction and export (written to the output file)

---

## Instructions 🛠️

### Requirements 📦

- 🐍 Python **3.13+**
- 📜 [Poetry](https://python-poetry.org/) (recommended) or `pip`

### Installation ⬇️

```bash
make install
```

This creates a virtual environment and installs dependencies (via Poetry).

### Run ▶️

```bash
make run
```

Or directly:

```bash
python3 a_maze_ing.py config.txt
```

### Debug mode 🐛

```bash
make debug
```

### Linting ✅

```bash
make lint         # flake8 + mypy
make lint-strict  # flake8 + mypy --strict
```

### Cleanup 🧹

```bash
make clean
```

---

## Configuration file ⚙️

The program takes **one argument**: the path to a configuration file.

```bash
python3 a_maze_ing.py config.txt
```

Lines starting with `#` are treated as comments and ignored.

### Complete config structure 🧾

#### Mandatory keys (required) 🔒

| Key           | Type              | Description                           | Example                |
|---------------|-------------------|---------------------------------------|------------------------|
| `WIDTH`       | integer           | Maze width in cells                   | `WIDTH=60`             |
| `HEIGHT`      | integer           | Maze height in cells                  | `HEIGHT=25`            |
| `ENTRY`       | `[x, y]` integers | Entry coordinates (x, y)              | `ENTRY=[1, 1]`         |
| `EXIT`        | `[x, y]` integers | Exit coordinates (x, y)               | `EXIT=[59, 24]`        |
| `OUTPUT_FILE` | string            | Output filename                       | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | boolean           | `true` for perfect, `false` for loops | `PERFECT=true`         |

#### Optional keys (advanced) 🧰

| Key            | Type   | Description                                            | Default        |
|----------------|--------|--------------------------------------------------------|----------------|
| `ALGORITHM`    | string | Generation algorithm: `backtracking` or `prim`         | `backtracking` |
| `SEED`         | string | Seed for reproducible generation                       | random         |
| `MODE_GEN`     | string | `static` or `animated`                                 | `static`       |
| `DISPLAY_MODE` | string | `basic` or `tty`                                       | `basic`        |
| `STAMP_TYPE`   | string | Logo stamp: `42vanilla` or `42custom`                  | `42vanilla`    |

### Example `config.txt` 🧪

```ini
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

## Maze generation algorithms 🧬

This project supports **two** classic procedural maze-generation algorithms.

### Recursive Backtracking (DFS) 🕳️➡️

**What it is:**  
A randomized depth-first search that carves passages by walking through unvisited cells and backtracking when stuck.

**Why we chose it:**  
- 👍 Simple and reliable
- ✅ Great fit for **perfect mazes** (one unique solution)
- 🎞️ Very easy to animate step-by-step

### Prim’s algorithm 🌿

**What it is:**  
A randomized Prim-like approach that grows the maze from a visited region by selecting random frontier cells and connecting them back to the visited area.

**Why we chose it:**  
- 🌍 Produces more evenly distributed mazes (different “feel” vs DFS)
- 🎮 Good visual and gameplay contrast with DFS
- 🧱 Often yields a more “open” structure

### Perfect vs Imperfect 🔁

- ✅ `PERFECT=true`: the maze has a **single unique path** between entry and exit.
- 🔁 `PERFECT=false`: the generator starts from a perfect maze, then removes additional walls to introduce **loops** (multiple possible routes).

---

## Output file format 🧾

Each cell is encoded as **one hexadecimal digit** representing which walls are closed.

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1       | East  |
| 2       | South |
| 3       | West  |

File structure:

```text
<hex grid, one row per line>

<entry x,y>
<exit x,y>
<shortest path: sequence of N/E/S/W>
```

---

## Display modes & interactions 🖥️🎛️

### Basic mode (`DISPLAY_MODE=basic`) 🟦
Simple ASCII rendering of the maze.

### TTY mode (`DISPLAY_MODE=tty`) 🌈
Advanced terminal rendering with ANSI colors, lighting effects, and full interactivity.

#### Key bindings (TTY mode) ⌨️

| Key         | Action                                    |
|-------------|-------------------------------------------|
| `R`         | Regenerate with a new random seed         |
| `E`         | Regenerate with a newly computed seed     |
| `F`         | Show / Hide shortest path                 |
| `C` / `V`   | Cycle wall colors                         |
| `P` / Space | Pause / Resume animation                  |
| `+` / `-`   | Increase / Decrease animation speed       |
| `G`         | Toggle interactive game mode              |
| `W/A/S/D`   | Move player (game mode)                   |
| `ESC`       | Quit                                      |

---

## Reusability: the `mazegen` module ♻️

The reusable part of this project is the **`mazegen`** package. It is designed to be independent from rendering (view layer) and can be imported in other Python projects.

- Documentation (internal link): **[`mazegen/README.md`](./mazegen/README.md)**

### Minimal example 🧪

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
    STAMP_TYPE="42vanilla",
)

generator = MazeGenerator(config)
maze = generator.generate_maze()

print(maze)               # Hex grid as string
print(maze.shortest_path) # e.g. "EESSWWN..."
```

---

## Team & project management 👥📅

### Team 👤👤

- **kebertra**
- **orobert**

### Roles 🧑‍💻

**kebertra**
- 🧭 Project lead
- 🏗️ Architecture and core design
- 🕳️ Recursive Backtracking (DFS) algorithm
- 🔎 Code reviews
- 🧼 Enforcing OOP standards and overall code quality

**orobert**
- 🖥️ Rendering layer (basic + TTY)
- 🌿 Prim’s algorithm
- 🔁 Imperfect maze mode (loop creation)
- 🎞️ Animated generation
- 🏷️ Stamp system / patterns (logo embedding)
- 🧭 Shortest path (mini BFS)

### Planning (expected vs actual) 🗺️

**Initial plan (high level):**
1. 🧱 Implement maze data structures and hex output
2. 🧠 Add one generation algorithm + shortest path
3. 🔁 Add perfect/imperfect option + second algorithm
4. 🖥️ Add terminal rendering (basic), then TTY interactions and animation
5. ♻️ Refactor into a reusable library and finalize documentation

**How it evolved:**
- The project split naturally into **application** vs **reusable library** (`mazegen`)
- TTY rendering and interactivity required extra iteration (ANSI quirks, key handling, animation smoothness)
- Factory/pattern-based organization (algorithms/stamps) improved extensibility and maintainability

### What worked well ✅

- Separation between **generation** and **rendering**
- Two algorithms with distinct maze “styles”
- Pattern-based stamp system that can be extended
- Generator-based animation that keeps rendering decoupled from core logic
- Code reviews helped keep consistent OOP practices

### What could be improved 🔧

- Add unit tests (currently validated manually)
- Add CI (lint/tests) to automate checks
- Make entry/exit border validation more explicit
- Add a graphical renderer (MLX) if required later

### Tools used 🧰

- Git for version control
- VS Code
- Poetry for dependency management and packaging
- flake8 + mypy for static analysis
- ANSI/TTY terminal features for rendering and interaction

---

## Resources 📚

### Classic references 🔗

- 🧭 Maze generation algorithms — Wikipedia: https://en.wikipedia.org/wiki/Maze_generation_algorithm
- 🕳️ Randomized DFS (Recursive Backtracker): https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search
- 🌿 Prim’s algorithm: https://en.wikipedia.org/wiki/Prim%27s_algorithm
- 📘 Pydantic documentation: https://docs.pydantic.dev/
- 🎨 ANSI escape codes: https://en.wikipedia.org/wiki/ANSI_escape_code
- 🧩 Python typing module: https://docs.python.org/3/library/typing.html

### AI usage (what, where, why) 🤖

GitHub Copilot (Claude Sonnet) was used during development for:
- 📝 Generating and updating English docstrings across the codebase
- 🏭 Refactoring the stamp system into a factory-based architecture
- 🧱 Migrating `MazeGenerator` from multiple parameters to a single `ConfigModel`
- 🧰 Suggesting fixes for imports after directory restructuring
- 🔎 Code review feedback and architecture suggestions
