"""LevelUp Dev Lab — Episode 001: your first automation."""

from datetime import datetime


def greet(name: str = "World") -> str:
    """Return a friendly greeting. Returning (not printing) keeps it testable."""
    return f"Hello, {name}! Welcome to LevelUp Dev Lab."


def main() -> None:
    print(greet())
    print(f"The time is {datetime.now():%H:%M:%S}.")


if __name__ == "__main__":
    main()
