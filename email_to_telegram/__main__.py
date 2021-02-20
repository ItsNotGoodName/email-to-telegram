import logging
import mailparser

from .constants import (
    ENV,
    MESSAGE_TIMEOUT,
    TOKEN,
    TRANSFERS,
    MAIL_PATH,
    ATTACHMENTS_FOLDER,
)
from .telegram_bot import TelegramBot
from .utils import get_emails, get_attachments_paths


def transfer(emails, bot):
    for email in emails:
        paths = get_attachments_paths(email, ATTACHMENTS_FOLDER)
        for transfer in TRANSFERS:
            # Check if from_address matches or is None
            if transfer["from_address"] is not None:
                for from_ in email.from_:
                    if from_[1] == transfer["from_address"]:
                        logging.debug("%s : from_address matches", transfer["name"])
                        break
                else:
                    logging.debug(
                        "%s : skipping since from_address does not match",
                        transfer["name"],
                    )
                    continue
            else:
                logging.debug("%s : from_address is None", transfer["name"])

            # Check if to_address matches or is None
            if transfer["to_address"] is not None:
                for to in email.to:
                    if to[1] == transfer["to_address"]:
                        logging.debug("%s : to_address matches", transfer["name"])
                        break
                else:
                    logging.debug(
                        "%s : skipping since to_address does not match",
                        transfer["name"],
                    )
                    continue
            else:
                logging.debug("%s : to_address is None", transfer["name"])

            # Send message or send photo
            if len(paths) > 0:
                bot.send_photos(
                    transfer["chat_id"], paths, email.subject + "\n" + email.body
                )
            else:
                bot.send_message(transfer["chat_id"], email.subject + "\n" + email.body)


def main():
    if ENV != "production":
        logging.basicConfig(level=logging.DEBUG)
    logging.info("Entered main")
    bot = TelegramBot(TOKEN, MESSAGE_TIMEOUT)
    emails = get_emails(MAIL_PATH)
    transfer(emails, bot)


if __name__ == "__main__":
    main()
