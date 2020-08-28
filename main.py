import mailbox
import os
import logging

from constants import MAILBOX_PATH, PICTURE_PATH, MAILBOX_FOLDER, ENV
from instance import mail_access, telegram_bot

def consume_mailbox(mail_access):
    parsed_emails = mail_access.parse_emails()
    dispatch_telegram(parsed_emails)

def dispatch_telegram(parsed_emails):
    for p in parsed_emails:
        message = "Subject: " + p['subject'] + '\n' + p['body']
        if(p["type"] == "picture"):
            telegram_bot.send_photos(message, p['attachments'])
        else:
            telegram_bot.send_message(message, disable_notification=True)

def main():
    if not os.path.exists(PICTURE_PATH):
        os.makedirs(PICTURE_PATH)

    mail_access.set_callback(consume_mailbox, andExecute=True)

    logging.debug(f"Watching {MAILBOX_PATH}")
    mail_access.notifier.loop()

if __name__ == "__main__":
    if ENV != "production":
        logging.basicConfig(level=logging.DEBUG)

    main()