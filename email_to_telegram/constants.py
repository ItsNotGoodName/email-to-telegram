import os
import sys
import pathlib
import logging

import configparser

MAIL_FOLDER = MAIL_FILE = MAIL_PATH = ATTACHMENTS_FOLDER = MESSAGE_TIMEOUT = TOKEN = ENV = TRANSFERS = None

def load_config(file_name):
    global MAIL_FOLDER , MAIL_FILE , MAIL_PATH , ATTACHMENTS_FOLDER , MESSAGE_TIMEOUT , TOKEN , ENV , TRANSFERS

    config = configparser.ConfigParser()
    config.read(file_name)

    MAIL_FOLDER         = config['DEFAULT']['mail_folder']
    MAIL_FILE           = config['DEFAULT']['mail_file']
    MAIL_PATH           = os.path.join(MAIL_FOLDER, MAIL_FILE)
    ATTACHMENTS_FOLDER  = config['DEFAULT']['attachments_folder']
    MESSAGE_TIMEOUT     = int(config['DEFAULT']['message_timeout'])
    TOKEN               = config['DEFAULT']['token']
    ENV                 = config['DEFAULT']['env']

    TRANSFERS = []
    for section in config.sections():
        chat_id = config[section]["chat_id"]
        from_address = config[section]["from_address"]
        TRANSFERS.append({"chat_id": chat_id, "from_address": from_address})
    print(ENV)

system_config = pathlib.Path("/etc/email-to-telegram/config.ini")
if system_config.exists ():
    load_config(_system_config)
else:
    local_config = pathlib.Path("config.ini")
    if local_config.exists():
        load_config('config.ini')
    else:
        logging.error(f"No valid 'config.ini' file")
        sys.exit()
