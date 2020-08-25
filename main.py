import mailbox
import os
from tgram import send_photos,send_message
from utils import extract_attachements, decode_email_subject
from constants import MAILBOX_PATH, PICTURE_PATH
import logging
 
def extract_message(message):
    picture_paths = extract_attachements(message)
    if len(picture_paths) == 0: # It is a normal message
        return {"subject": decode_email_subject(message["subject"]), "type": "message"}
    return {"subject": decode_email_subject(message["subject"]), "attachments": picture_paths, "type": "picture"}

def dispatch_telegram(parsed_messages):
    for p in parsed_messages:
        if(p["type"] == "picture"):
            send_photos(p['subject'], p['attachments'])
        else:
            send_message(p["subject"])

def consume_mailbox():
    mbox = mailbox.mbox(MAILBOX_PATH)
    parsed_messages = [] 
    try:
        mbox.lock()
        pass
    except mailbox.ExternalClashError:
        logging.error("Mailbox not consumed, it is being access by another program")
        return

    keys = mbox.keys()
    for key in keys:
        logging.debug(f"{str(len(parsed_messages))} new messages")
        message = mbox.pop(key)
        parsed_messages.append(extract_message(message))

    mbox.flush()
    mbox.unlock()

    dispatch_telegram(parsed_messages)

def init():
    if not os.path.exists(PICTURE_PATH):
        os.makedirs(PICTURE_PATH)

def main():
    init()
    consume_mailbox()

if __name__ == "__main__":
    main()