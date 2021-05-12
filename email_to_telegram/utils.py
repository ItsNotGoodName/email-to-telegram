import os
import logging
import mailbox
import pathlib
import mailparser


def get_emails(mail_path):
    mbox = mailbox.mbox(mail_path)
    parsed_emails = []
    try:
        mbox.lock()
    except mailbox.ExternalClashError:
        logging.error(
            "Mailbox not consumed, it is being access by another program"
        )
        return parsed_emails, 0

    keys = mbox.keys()
    for key in keys:
        email = mbox.pop(key)
        parsed_emails.append(mailparser.parse_from_string(str(email)))

    mbox.flush()
    mbox.unlock()
    mbox.close()
    return parsed_emails, 1


def get_attachments_paths(email, attachment_folder):
    email.write_attachments(attachment_folder)
    paths = []
    for attachment in email.attachments:
        paths.append(attachment_folder / pathlib.Path(attachment["filename"]))
    return paths

def clear_attachments(attachment_folder):
    try:
        for f in os.listdir(attachment_folder):
            os.remove(os.path.join(attachment_folder, f))
    except Exception as e:
        logging.error(e)

def should_skip_address(email, transfer, address):
    if transfer[address + "_address"] is None:
        logging.debug("%s : %s is None", transfer["name"], address)
        return False

    for check_address in email.mail[address]:
        if check_address[1] == transfer[address + "_address"]:
            logging.debug("%s : %s matches", transfer["name"], address)
            return False

    logging.debug(
        "%s : skipping since %s does not match", transfer["name"], address
    )
    return True
