# Episode 005 — Python CLI
PY := python3
VENV := .venv
BIN := $(VENV)/bin

.PHONY: setup run test clean

setup:
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --quiet --upgrade pip pytest

run:
	@printf "the quick brown fox\njumps over\n" | $(PY) src/cli.py

test:
	@if [ -x "$(BIN)/pytest" ]; then $(BIN)/pytest -q tests; else $(PY) -m pytest -q tests; fi

clean:
	rm -rf $(VENV) .pytest_cache tests/__pycache__ src/__pycache__
