import logging
import sys


def is_word(word: str) -> bool:
    if len(word) == 0:
        return False
    if not any(_.isalpha() for _ in word):
        return False
    if any(_.isdigit() for _ in word):
        return False
    return True


def setup_logging() -> None:
    root_logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stderr)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    if len(root_logger.handlers) == 0:
        root_logger.addHandler(handler)

    root_logger.setLevel(logging.INFO)
