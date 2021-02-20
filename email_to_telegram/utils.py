import logging
import mailbox
import re
import pathlib
import mailparser


def get_attachments_paths(email, attachment_folder):
    email.write_attachments(attachment_folder)
    paths = []
    for attachment in email.attachments:
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


def should_skip_address(email, transfer, address):
    if transfer[address] is not None:
        for to in email.to:
            if to[1] == transfer[address]:
                logging.debug("%s : %s matches", transfer["name"], address)
                return False
        else:
            logging.debug(
                "%s : skipping since %s does not match", transfer["name"], address
            )
            return True
    else:
        logging.debug("%s : %s is None", transfer["name"], address)
        return False
