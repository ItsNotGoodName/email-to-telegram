import mailbox
import os
from tgram import send_photos
from utils import extract_attachements
from constants import MAILBOX_PATH, PICTURE_PATH
import logging
 
def extract_message(message):
    picture_paths = extract_attachements(message)
    return {"subject": message["subject"], "attachments": picture_paths}

def dispatch_telegram(parsed_messages):
    for p in parsed_messages:
        send_photos(p['subject'], p['attachments'])

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
        parsed_message = extract_message(message)
        if len(parsed_message['attachments']) != 0: # Only add messages that have atleast 1 picture
            parsed_messages.append(parsed_message)
        break

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