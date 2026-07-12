"""Episode 002 — intention-revealing names (Python)."""

from datetime import date


def days_overdue(due_date: date, returned_date: date) -> int:
    """Return how many days late a book was returned (0 if on time)."""
    late_days = (returned_date - due_date).days
    return max(late_days, 0)


def main() -> None:
    due = date(2026, 7, 1)
    returned = date(2026, 7, 12)
    print(f"Days overdue: {days_overdue(due, returned)}")


if __name__ == "__main__":
    main()
