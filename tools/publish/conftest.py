# Put tools/publish on sys.path so `import publish` works when running pytest
# from here without an editable install. (Typer still needs to be installed;
# see the Makefile's `make setup`.)
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
