import logging

from .constants import ENV, MESSAGE_TIMEOUT, TOKEN, TRANSFERS
from .telegram_bot import TelegramBot


def main():
    if ENV != "production":
        logging.basicConfig(level=logging.DEBUG)
    logging.debug("Entered main")
    bot = TelegramBot(TOKEN, MESSAGE_TIMEOUT)


if __name__ == "__main__":
    main()
