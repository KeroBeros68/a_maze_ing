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

SRC = a_maze_ing.py \
	  env_check.py \
	  model.py \
	  mazegen/utils/utils.py \
	  mazegen/cell/cell.py

# **************************************************************************** #
#									Rules									   #
# **************************************************************************** #

install:
	@bash -c '\
		echo -e "${CYAN}Checking virtual environment...${RESET}"; \
		if [ -z "$$VIRTUAL_ENV" ]; then \
			echo -e "${YELLOW}⚠ No virtual environment detected${RESET}"; \
			echo -n -e "${CYAN}Creating virtual environment '\''matrix_env'\''...${RESET} "; \
			if python3 -m venv matrix_env > /dev/null 2>&1; then \
				echo -e "${GREEN}✓${RESET}"; \
			else \
				echo -e "${RED}✗${RESET}"; \
				echo -e "${RED}Failed to create virtual environment${RESET}"; \
				exit 1; \
			fi; \
		else \
			echo -e "${GREEN}✓ Virtual environment active: $$VIRTUAL_ENV${RESET}"; \
		fi; \
		. matrix_env/bin/activate; \
		echo -n -e "${CYAN}Checking Poetry...${RESET} "; \
		if command -v poetry > /dev/null 2>&1; then \
			echo -e "${GREEN}✓ Poetry is installed${RESET}"; \
		else \
			echo -e "${YELLOW}⚠ Poetry not found${RESET}"; \
			echo -n -e "${CYAN}Installing Poetry...${RESET} "; \
			if pip install poetry > /dev/null 2>&1; then \
				echo -e "${GREEN}✓${RESET}"; \
			else \
				echo -e "${RED}✗${RESET}"; \
				echo -e "${RED}Failed to install Poetry${RESET}"; \
				exit 1; \
			fi; \
		fi; \
		echo -n -e "${CYAN}Installing dependencies with Poetry...${RESET} "; \
		if poetry install > /dev/null 2>&1; then \
			echo -e "${GREEN}✓${RESET}"; \
		else \
			echo -e "${RED}✗$${RESET}"; \
			poetry install; \
		fi; \
		echo -e "${GREEN}✓ Installation complete${RESET}"; \
	'

run:
	python3 a_maze_ing.py

debug:

lint:
	python3 -m flake8 --exclude=matrix_env
	python3 -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude=matrix_env $(SRC)

lint-strict:
	python3 -m flake8 --exclude=matrix_env
	python3 -m mypy --strict --exclude=matrix_env $(SRC)

clean:
	printf "$(CYAN)Suppression de __pycache__...$(RESET) "
	if [ -d "__pycache__" ]; then \
		rm -rf __pycache__ && \
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