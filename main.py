import mailbox
import os
import logging
import pyinotify

from constants import MAILBOX_PATH, PICTURE_PATH, MAILBOX_FOLDER, ENV
from instance import mail_access, telegram_bot

def consume_mailbox(mail_access):
    parsed_emails = mail_access.parse_emails()
    dispatch_telegram(parsed_emails)

def dispatch_telegram(parsed_emails):
    for p in parsed_emails:
        if(p["type"] == "picture"):
            telegram_bot.send_photos(p['subject'], p['attachments'])
        else:
            telegram_bot.send_message(p["subject"], disable_notification=True)

def main():
    if not os.path.exists(PICTURE_PATH):
        os.makedirs(PICTURE_PATH)

    mail_access.set_callback(consume_mailbox)
    # Invoke check on startup
    mail_access.invoke_callback()
    mail_access.modifications = 0

    # Setup watchers on the root folder where the mail file is stored
    wm = pyinotify.WatchManager()
    wm.add_watch(MAILBOX_FOLDER, pyinotify.ALL_EVENTS)
    notifier = pyinotify.Notifier(wm, mail_access.on_change_handler)

    logging.debug(f"Watching {MAILBOX_PATH}")
    notifier.loop()


if __name__ == "__main__":
    if ENV != "production":
        logging.basicConfig(level=logging.DEBUG)

    main()