import logging
import mailbox
import re
import pathlib
import mailparser


def get_attachments_paths(parsed_email, attachment_folder):
    parsed_email.write_attachments(attachment_folder)
    paths = []
    for attachment in parsed_email.attachments:
        paths.append(attachment_folder / pathlib.Path(attachment["filename"]))
    return paths


def get_emails(mail_path):
    mbox = mailbox.mbox(mail_path)
    parsed_emails = []
    try:
        mbox.lock()
    except mailbox.ExternalClashError:
        logging.error("Mailbox not consumed, it is being access by another program")
        return parsed_emails

    keys = mbox.keys()
    for key in keys:
        email = mbox.pop(key)
        parsed_emails.append(mailparser.parse_from_string(str(email)))

    mbox.flush()
    mbox.unlock()
    mbox.close()
    return parsed_emails
