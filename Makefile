.SILENT:

# **************************************************************************** #
#                                   COLORS                                     #
# **************************************************************************** #

GREEN   = \033[0;32m
RED     = \033[0;31m
YELLOW  = \033[0;33m
BLUE    = \033[0;34m
MAGENTA = \033[0;35m
CYAN    = \033[0;36m
RESET   = \033[0m

# **************************************************************************** #
#                                  VARIABLES                                   #
# **************************************************************************** #

SRC_MYPY = a_maze_ing.py \
	   controller.py \
	   utils/env_check.py \
	   keycontrol/KeyControl.py \
	   mazegen/MazeGenerator.py \
	   mazegen/algorithms/algorithm.py \
	   mazegen/algorithms/backtracking.py \
	   mazegen/algorithms/factory.py \
	   mazegen/cell/cell.py \
	   mazegen/maze/maze.py \
	   mazegen/stamp/Stamp.py \
	   mazegen/stamp/StampConsts.py \
	   mazegen/utils/utils.py \
	   model/Model.py \
	   view/View.py \
	   view/ViewFactory.py \
	   view/basic/BasicView.py \
	   view/tty/TtyView.py \
	   view/tty/TtyConsts.py \
	   view/tty/TtyUtils.py

# **************************************************************************** #
#									Rules									   #
# **************************************************************************** #

install:
	echo "${CYAN}Checking virtual environment...${RESET}"; \
	if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "${YELLOW}⚠ No virtual environment detected${RESET}"; \
		echo -n "${CYAN}Creating virtual environment '\''matrix_env'\''...${RESET} "; \
		if python3 -m venv matrix_env > /dev/null 2>&1; then \
			echo "${GREEN}✓${RESET}"; \
		else \
			echo "${RED}✗${RESET}"; \
			echo "${RED}Failed to create virtual environment${RESET}"; \
			exit 1; \
		fi; \
	else \
		echo "${GREEN}✓ Virtual environment active: $$VIRTUAL_ENV${RESET}"; \
	fi; \
	. matrix_env/bin/activate; \
	echo -n "${CYAN}Checking Poetry...${RESET} "; \
	if command -v poetry > /dev/null 2>&1; then \
		echo "${GREEN}✓ Poetry is installed${RESET}"; \
	else \
		echo "${YELLOW}⚠ Poetry not found${RESET}"; \
		echo -n "${CYAN}Installing Poetry...${RESET} "; \
		if pip install poetry > /dev/null 2>&1; then \
			echo "${GREEN}✓${RESET}"; \
		else \
			echo "${RED}✗${RESET}"; \
			echo "${RED}Failed to install Poetry${RESET}"; \
			exit 1; \
		fi; \
	fi; \
	echo -n "${CYAN}Installing dependencies with Poetry...${RESET} "; \
	if poetry install > /dev/null 2>&1; then \
		echo "${GREEN}✓${RESET}"; \
	else \
		echo "${RED}✗$${RESET}"; \
		poetry install; \
	fi; \
	echo "${GREEN}✓ Installation complete${RESET}"; \

run:
	python3 a_maze_ing.py

debug:
	python3 -m pdb a_maze_ing.py

lint:
	echo "${CYAN}Running flake8...${RESET}"; \
	python3 -m flake8 --exclude=matrix_env; \
	echo "${CYAN}Running mypy...${RESET}"; \
	python3 -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude=matrix_env $(SRC_MYPY)

lint-strict:
	python3 -m flake8 --exclude=matrix_env
	python3 -m mypy --strict --exclude=matrix_env $(SRC_MYPY)

clean:
	printf "$(CYAN)Suppression de __pycache__...$(RESET) "
	if [ -d "__pycache__" ]; then \
		rm -r -f __pycache__ && \
		echo "$(GREEN)✓ Dossier __pycache__ supprimés$(RESET)"; \
	else \
		echo "$(YELLOW)⚠ Rien à nettoyer$(RESET)"; \
	fi
	printf "$(CYAN)Suppression de .mypy_cache...$(RESET) "
	if [ -d ".mypy_cache" ]; then \
		rm -rf .mypy_cache && \
		echo "$(GREEN)✓ Dossier .mypy_cache supprimés$(RESET)"; \
	else \
		echo "$(YELLOW)⚠ Rien à nettoyer$(RESET)"; \
	fi

.PHONY: install clean 