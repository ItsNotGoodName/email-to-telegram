import mailbox
import os
from tgram import send_photos
from utils import extract_attachements
from constants import MAILBOX_PATH, PICTURE_PATH

def consume_message(message):
    picture_paths = extract_attachements(message)
    send_photos("CAPTION TEST", picture_paths)
    pass

def consume_mailbox():
    mbox = mailbox.mbox(MAILBOX_PATH)
    keys = mbox.keys()
    for key in keys:
        message = mbox.pop(key)
        consume_message(message)

    # mbox.flush()

def init():
    if not os.path.exists(PICTURE_PATH):
        os.makedirs(PICTURE_PATH)

def main():
    init()
    consume_mailbox()

if __name__ == "__main__":
    main()