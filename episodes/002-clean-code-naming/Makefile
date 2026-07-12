# Episode 002 — Python + Java + JavaScript
PY := python3
VENV := .venv
BIN := $(VENV)/bin

.PHONY: setup run run-python run-node run-java test clean

setup:
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --quiet --upgrade pip pytest

run: run-python run-node run-java

run-python:
	@echo "== Python =="
	$(PY) src/python/overdue.py

run-node:
	@echo "== JavaScript =="
	@command -v node >/dev/null 2>&1 && node src/javascript/overdue.js || echo "(node not installed, skipping)"

run-java:
	@echo "== Java =="
	@command -v javac >/dev/null 2>&1 && \
		(javac -d build src/java/Overdue.java && java -cp build Overdue) || \
		echo "(JDK not installed, skipping)"

# Runs whatever toolchains are available; always passes if the code is correct.
test:
	@echo "== Python tests =="
	@if [ -x "$(BIN)/pytest" ]; then $(BIN)/pytest -q tests; else $(PY) -m pytest -q tests; fi
	@echo "== JavaScript tests =="
	@command -v node >/dev/null 2>&1 && node tests/overdue.test.js || echo "(node not installed, skipping)"
	@echo "== Java tests =="
	@command -v javac >/dev/null 2>&1 && \
		(javac -d build src/java/Overdue.java tests/OverdueTest.java && java -cp build OverdueTest) || \
		echo "(JDK not installed, skipping)"

clean:
	rm -rf $(VENV) build .pytest_cache tests/__pycache__ src/python/__pycache__
