"""Episode 004 — logging and timing instead of print()."""

import logging
import time
from contextlib import contextmanager
from typing import Iterator

logger = logging.getLogger("levelup.observe")


def configure_logging(level: int = logging.INFO) -> None:
    """Send timestamped, levelled logs to stderr."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
    )


@contextmanager
def timed(label: str) -> Iterator[dict]:
    """Measure how long a block takes. Yields a dict that gets a 'seconds' key."""
    result: dict = {}
    start = time.perf_counter()
    logger.debug("starting %s", label)
    try:
        yield result
    finally:
        result["seconds"] = time.perf_counter() - start
        logger.info("%s took %.4fs", label, result["seconds"])


def sum_of_squares(n: int) -> int:
    """A trivial 'workload' worth measuring."""
    return sum(i * i for i in range(n))


def main() -> None:
    configure_logging(logging.DEBUG)
    with timed("sum_of_squares"):
        total = sum_of_squares(100_000)
    logger.info("result = %d", total)


if __name__ == "__main__":
    main()
