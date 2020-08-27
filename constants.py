import os
import secrets

PICTURE_PATH=os.path.join(os.getcwd(), "attachments")
MAILBOX_PATH=f"{secrets.MAILBOX_FOLDER}{secrets.MAILBOX_NAME}"
SECONDS_BETWEEN_MESSAGES=5

MAILBOX_FOLDER=secrets.MAILBOX_FOLDER
MAILBOX_NAME=secrets.MAILBOX_NAME
CHAT_ID=secrets.CHAT_ID
TOKEN=secrets.TOKEN
