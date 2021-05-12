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
DISABLE_TEXT = False
DISABLE_PHOTO = False


def load_config(config_path):
    global MAIL_FOLDER, MAIL_FILE, MAIL_PATH, ATTACHMENTS_FOLDER, MESSAGE_TIMEOUT, TOKEN, ENV, TRANSFERS, DISABLE_TEXT, DISABLE_PHOTO

    config = configparser.ConfigParser()
    config.read(config_path)

    # Required variables
    TOKEN = config["DEFAULT"]["token"]
    MAIL_PATH = pathlib.Path((config["DEFAULT"]["mail_path"]))
    MAIL_FOLDER = MAIL_PATH.parent
    MAIL_FILE = MAIL_PATH.name

    # Optional variables
    MESSAGE_TIMEOUT = config["DEFAULT"].getint("message_timeout", MESSAGE_TIMEOUT)
 
    ATTACHMENTS_FOLDER = config["DEFAULT"].get(
        "attachments_folder", ATTACHMENTS_FOLDER
    )
    ENV = config["DEFAULT"].get("env", ENV)
    DISABLE_TEXT = config["DEFAULT"].getboolean("disable_text", DISABLE_TEXT)
    DISABLE_PHOTO = config["DEFAULT"].getboolean("disable_photo", DISABLE_PHOTO)

    # Email to telegram transfers
    TRANSFERS = []
    for section in config.sections():
        # Required variables
        chat_id = config[section]["chat_id"]

        # Optional variables
        to_address = config[section].get("to_address")
        from_address = config[section].get("from_address")
        disable_text = config[section].getboolean("disable_text", DISABLE_TEXT)
        disable_photo = config[section].getboolean("disable_photo", DISABLE_PHOTO)
        caption_chat_id = config[section].get("caption_chat_id", None)

        TRANSFERS.append(
            {
                "chat_id": chat_id,
                "to_address": to_address,
                "from_address": from_address,
                "name": section,
                "disable_text": disable_text,
                "disable_photo": disable_photo,
                "caption_chat_id": caption_chat_id,
            }
        )


for i in CONFIG_PATHS:
    path = pathlib.Path(i)
    if path.exists():
        load_config(path)
        break
else:
    logging.error("No valid 'config.ini' found")
    sys.exit()
