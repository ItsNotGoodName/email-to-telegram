import logging
import mailbox

import mailparser
from watchdog.events import FileSystemEventHandler

from .constants import MAIL_PATH, MAIL_FOLDER, MAIL_FILE, ATTACHMENTS_FOLDER, TRANSFERS
from .utils import get_emails, should_skip_address, get_attachments_paths


class MailHandler(FileSystemEventHandler):
    def __init__(self, bot, lock_file, mail_path):
        self.bot = bot
        self.lock_file = lock_file
        self.mail_path = mail_path
        self.counter = 0

    def on_deleted(self, event):
        if event.src_path == self.lock_file:
            if self.counter <= 0:
                emails, delete_count = get_emails(self.mail_path)
                self.counter += delete_count
                consume_emails(emails, self.bot)
            else:
                self.counter -= 1


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
