import sys
import pathlib
import logging
import configparser

# Required variables
MAIL_FOLDER = MAIL_FILE = MAIL_PATH = TOKEN = TRANSFERS = None

# Optional variables
ENV = "production"
CONFIG_PATHS = ["/etc/email-to-telegram/config.ini", "config.ini"]
ATTACHMENTS_FOLDER = "/tmp/telegram-attachments_folder"
MESSAGE_TIMEOUT = 3


def load_config(config_path):
    global MAIL_FOLDER, MAIL_FILE, MAIL_PATH, ATTACHMENTS_FOLDER, MESSAGE_TIMEOUT, TOKEN, ENV, TRANSFERS

    config = configparser.ConfigParser()
    config.read(config_path)

    # Required variables
    TOKEN = config["DEFAULT"]["token"]
    MAIL_PATH = pathlib.Path((config["DEFAULT"]["mail_path"]))
    MAIL_FOLDER = MAIL_PATH.parent
    MAIL_FILE = MAIL_PATH.name

    # Optional variables
    MESSAGE_TIMEOUT = int(config["DEFAULT"].get("message_timeout", MESSAGE_TIMEOUT))
    ATTACHMENTS_FOLDER = config["DEFAULT"].get("attachments_folder", ATTACHMENTS_FOLDER)
    ENV = config["DEFAULT"].get("env", ENV)

    # Email to telegram transfers
    TRANSFERS = []
    for section in config.sections():
        # Required variables
        chat_id = config[section]["chat_id"]

        # Optional variables
        to_address = config[section].get("to_address")
        from_address = config[section].get("from_address")

        TRANSFERS.append(
            {"chat_id": chat_id, "to_address": to_address, "from_address": from_address}
        )


for i in CONFIG_PATHS:
    path = pathlib.Path(i)
    if path.exists():
        load_config(path)
        break
else:
    logging.error("No valid 'config.ini' found")
    sys.exit()
