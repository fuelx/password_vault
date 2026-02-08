import logging
import os
from pathlib import Path

APP_NAME = "password-vault"

def get_logger(name: str = "vault") -> logging.Logger:
    log_dir = Path.home() / ".config" / APP_NAME
    log_file = log_dir / "vault.log"

    log_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(log_dir, 0o700)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger  # prevent duplicate handlers

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)

    try:
        os.chmod(log_file, 0o600)
    except PermissionError:
        pass

    return logger
