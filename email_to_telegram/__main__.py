import logging

from .constants import (
    ENV,
)


def main():
    if ENV != "production":
        logging.basicConfig(level=logging.DEBUG)
    logging.debug("Entered main")


if __name__ == "__main__":
    main()
