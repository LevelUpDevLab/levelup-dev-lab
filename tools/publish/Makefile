# tools/publish — internal publishing CLI
PY := python3
VENV := .venv
BIN := $(VENV)/bin

.PHONY: setup test run clean

setup:
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --quiet --upgrade pip
	$(BIN)/pip install --quiet -e ".[dev]"

test:
	@if [ -x "$(BIN)/pytest" ]; then $(BIN)/pytest -q; else $(PY) -m pytest -q; fi

# Example: make run ARGS="check 001"
run:
	$(BIN)/publish $(ARGS)

clean:
	rm -rf $(VENV) .pytest_cache **/__pycache__ *.egg-info
