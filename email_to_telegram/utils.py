import logging
import mailbox
import re
import mailparser


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
