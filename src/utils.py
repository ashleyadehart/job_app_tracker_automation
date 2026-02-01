from __future__ import annotations

import logging
from pathlib import Path


def ensure_dirs(dirnames: list[str]) -> None:
    for d in dirnames:
        Path(d).mkdir(parents=True, exist_ok=True)


def get_logger(log_path: str) -> logging.Logger:
    """
    Create a logger that writes to both console and a log file.
    Avoid duplicate handlers if called multiple times.
    """
    logger = logging.getLogger("job_tracker")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    fh = logging.FileHandler(log_path, encoding="utf-8")
    ch = logging.StreamHandler()

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger