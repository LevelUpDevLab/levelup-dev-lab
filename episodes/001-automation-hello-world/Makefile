# Episode 001 — Python (standard library only)
PY := python3
VENV := .venv
BIN := $(VENV)/bin

.PHONY: setup run test clean

setup:
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --quiet --upgrade pip pytest

# Demo: scan this episode folder itself and write ./report.md
run:
	$(PY) -m automation_hello_world . -v

test:
	@if [ -x "$(BIN)/pytest" ]; then $(BIN)/pytest -q tests; else $(PY) -m pytest -q tests; fi

clean:
	rm -rf $(VENV) .pytest_cache tests/__pycache__ automation_hello_world/__pycache__ report.md
