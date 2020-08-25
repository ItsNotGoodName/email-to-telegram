import base64
from os import path, getcwd, makedirs
from tgram import send_photos, send_message
import mailbox
from constants import PICTURE_PATH, MAILBOX_PATH

if not path.exists(PICTURE_PATH):
    makedirs(PICTURE_PATH)

def extractattachements(message, ext='jpg'):
    attachments = []
    if message.get_content_maintype() == 'multipart':
        for part in message.walk():
            if part.get_content_maintype() == 'multipart': continue
            if part.get('Content-Disposition') is None: continue
            filename = part.get_filename()
            attachments.append(path.join(PICTURE_PATH, filename))
            fb = open(path.join(PICTURE_PATH, filename),'wb') # TODO: Add catch here
            fb.write(part.get_payload(decode=True))
            fb.close()
    return attachments

def handle_motion_message(message):
    paths = extractattachements(message)

def main():
    for message in mailbox.mbox(MAILBOX_PATH):
        handle_motion_message(message)
        break

if __name__ == "__main__":
    main()
