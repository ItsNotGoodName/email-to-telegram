import logging

from watchdog.events import FileSystemEventHandler

from .constants import MAIL_PATH, ATTACHMENTS_FOLDER, TRANSFERS
from .utils import get_emails, should_skip_address, get_attachments_paths


class EmailHandler(FileSystemEventHandler):
    def __init__(self, bot, lock_file, mail_path):
        self.bot = bot
        self.lock_file = lock_file
        self.mail_path = mail_path
        self.counter = 0
        logging.debug("Current count %s", self.counter)

    def consume_emails(self):
        emails, delete_count = get_emails(self.mail_path)
        self.counter += delete_count
        consume_emails(emails, self.bot)

    def on_deleted(self, event):
        logging.debug("Current count %s", self.counter)
        if event.src_path == self.lock_file:
            if self.counter <= 0:
                self.consume_emails()
                logging.debug("Current count %s", self.counter)
            else:
                self.counter -= 1
                logging.debug("Current count %s", self.counter)


def consume_emails(emails, bot):
    for email in emails:
        attachment_paths = get_attachments_paths(email, ATTACHMENTS_FOLDER)
        for transfer in TRANSFERS:
            # Skip if from_address or to_address matches or is None
            if should_skip_address(
                email, transfer, "to"
            ) or should_skip_address(email, transfer, "from"):
                continue

            # Send text or send photo if not disabled
            if len(attachment_paths) > 0 and not transfer["disable_photo"]:
                caption = email.subject + "\n" + "".join(email.text_plain)
                if transfer["caption_chat_id"]:
                    bot.send_text(
                        transfer["caption_chat_id"],
                        caption
                    )
                    caption = None
                elif transfer["disable_caption"]:
                    caption = None

                bot.send_photo(
                    transfer["chat_id"],
                    attachment_paths,
                    caption
                )
            elif not transfer["disable_text"]:
                bot.send_text(
                    transfer["chat_id"],
                    email.subject + "\n" + "".join(email.text_plain),
                )
