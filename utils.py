import os
from email.header import decode_header
import logging

from telegram_bindings import telegram_bot
from constants import PICTURE_PATH

def decode_email_subject(subject):
    s = (decode_header(subject)[0][0])
    return str(s, 'utf-8')

def extract_message(message):
    picture_paths = extract_attachements(message)
    if len(picture_paths) == 0: # It is a normal message
        return {"subject": decode_email_subject(message["subject"]), "type": "message"}
    return {"subject": decode_email_subject(message["subject"]), "attachments": picture_paths, "type": "picture"}

def dispatch_telegram(parsed_messages):
    for p in parsed_messages:
        if(p["type"] == "picture"):
            telegram_bot.send_photos(p['subject'], p['attachments'])
        else:
            telegram_bot.send_message(p["subject"])

def extract_attachements(message):
    attachments = []
    if message.get_content_maintype() == 'multipart':
        for part in message.walk():
            if part.get_content_maintype() == 'multipart': continue
            if part.get('Content-Disposition') is None: continue

            filename = part.get_filename()

            if filename.endswith("jpg") or filename.endswith("jpeg") or filename.endswith("png"):
                attachments.append(os.path.join(PICTURE_PATH, filename))
                fb = open(os.path.join(PICTURE_PATH, filename),'wb') # TODO: Add catch here
                fb.write(part.get_payload(decode=True))
                fb.close()
    return attachments

def cleanup_attachments():
    pass