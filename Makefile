PYTHON		= python3
MAIN		= a_maze_ing.py
CONFIG		= config.txt
VENV		= .venv
PIP			= $(VENV)/bin/pip
FLAKE8		= $(VENV)/bin/flake8
MYPY		= $(VENV)/bin/mypy
PY			= $(VENV)/bin/python

MYPY_FLAGS	= --warn-return-any \
			  --warn-unused-ignores \
			  --ignore-missing-imports \
			  --disallow-untyped-defs \
			  --check-untyped-defs

.PHONY: all install run debug lint clean fclean

all: install

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(MAKE) -C mlx_CLXV
	$(PY) $(MAIN) $(CONFIG)

debug:
	$(PY) -m pdb $(MAIN) $(CONFIG)

lint:
	$(FLAKE8) .
	$(MYPY) . $(MYPY_FLAGS)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

fclean: clean
	rm -rf $(VENV)