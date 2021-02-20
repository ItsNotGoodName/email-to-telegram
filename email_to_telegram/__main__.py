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
from .utils import get_emails, get_attachments_paths, should_skip_address


def consume_emails(emails, bot):
    for email in emails:
        attachment_paths = get_attachments_paths(email, ATTACHMENTS_FOLDER)
        for transfer in TRANSFERS:
            # Skip if from_address or to_address matches or is None
            if should_skip_address(
                email, transfer, "to_address"
            ) or should_skip_address(email, transfer, "from_address"):
                continue

            # Send text or send photo if not disabled
            if len(attachment_paths) > 0:
                if not transfer["disable_photo"]:
                    bot.send_photo(
                        transfer["chat_id"],
                        attachment_paths,
                        email.subject + "\n" + email.body,
                    )
                else:
                    logging.debug("%s : photos are disabled", transfer["name"])
            else:
                if not transfer["disable_text"]:
                    bot.send_text(
                        transfer["chat_id"], email.subject + "\n" + email.body
                    )
                else:
                    logging.debug("%s : text is disabled", transfer["name"])


def main():
    if ENV != "production":
        logging.basicConfig(level=logging.DEBUG)
    logging.info("Entered main")
    bot = TelegramBot(TOKEN, MESSAGE_TIMEOUT)
    emails = get_emails(MAIL_PATH)
    consume_emails(emails, bot)


if __name__ == "__main__":
    main()
