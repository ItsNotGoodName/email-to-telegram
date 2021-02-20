import logging
import mailparser
import time
from watchdog.observers import Observer

from .constants import ENV, TOKEN, MESSAGE_TIMEOUT, MAIL_PATH, MAIL_FOLDER, MAIL_FILE
from .telegram_bot import TelegramBot
from .utils import get_emails, get_attachments_paths, should_skip_address
from .mail_handler import MailHandler


def main():
    if ENV != "production":
        logging.basicConfig(level=logging.DEBUG)
    logging.info("Entered main")
    bot = TelegramBot(
        TOKEN,
        MESSAGE_TIMEOUT,
    )

    observer = Observer()
    event_handler = MailHandler(
        bot, str((MAIL_FOLDER / (MAIL_FILE + ".lock"))), MAIL_PATH
    )
    # TODO: Figure out why pathlib paths do not work with watchdog
    observer.schedule(event_handler, path=(str(MAIL_FOLDER) + "/"), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
