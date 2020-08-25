import os
from constants import PICTURE_PATH

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