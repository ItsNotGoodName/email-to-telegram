import mailbox
import os
import logging

from email_to_telegram.constants import (
    MAIL_PATH,
    ATTACHMENTS_FOLDER,
    MAIL_FOLDER,
    ENV,
    TRANSFERS,
)
from email_to_telegram.instance import mail_access, telegram_bot


def consume_mailbox(mail_access):
    parsed_emails = mail_access.parse_emails()
    dispatch_telegram(parsed_emails)


def dispatch_telegram(parsed_emails):
    for email in parsed_emails:
        for transfer in TRANSFERS:
            if email["To"] == transfer["to_address"]:
                message = (
                    f"Subject: {email['Subject']}\nTo: {email['To']}\n{email['Body']}"
                )
                if email["Type"] == "picture":
                    telegram_bot.send_photos(
                        message, email["Attachments"], transfer["chat_id"]
                    )
                else:
                    telegram_bot.send_message(
                        message, transfer["chat_id"], disable_notification=True
                    )


def main():
    if ENV != "production":
        logging.basicConfig(level=logging.DEBUG)

    if not os.path.exists(ATTACHMENTS_FOLDER):
        os.makedirs(ATTACHMENTS_FOLDER)

    mail_access.set_callback(consume_mailbox, andExecute=True)

    logging.debug(f"Watching {MAIL_PATH}")
    mail_access.notifier.loop()
    telegram_bot.updater.stop()
