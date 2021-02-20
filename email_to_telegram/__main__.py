import time
import logging

from watchdog.observers import Observer

from .constants import ENV, TOKEN, MESSAGE_TIMEOUT, MAIL_PATH, MAIL_FOLDER, MAIL_FILE
from .telegram_bot import TelegramBot
from .email import EmailHandler


def main():
    if ENV != "production":
        logging.basicConfig(level=logging.DEBUG)
    logging.info("Entering main function")
    bot = TelegramBot(
        TOKEN,
        MESSAGE_TIMEOUT,
    )

    # Set handler and observer then start
    event_handler = EmailHandler(
        bot, str((MAIL_FOLDER / (MAIL_FILE + ".lock"))), MAIL_PATH
    )
    observer = Observer()
    observer.schedule(event_handler, path=f"{MAIL_FOLDER}/", recursive=True)
    observer.start()

    # Consume once on startup
    event_handler.consume_emails()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
