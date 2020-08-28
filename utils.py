import os
from email.header import decode_header
import logging

def decode_email_subject(subject):
    s = (decode_header(subject)[0][0])
    return str(s, 'utf-8')

def extract_email(message, output_folder):
    picture_paths = extract_attachements(message, output_folder)
    if len(picture_paths) == 0: # It is a normal message
        return {"subject": decode_email_subject(message["subject"]), "type": "message"}
    return {"subject": decode_email_subject(message["subject"]), "attachments": picture_paths, "type": "picture"}

def extract_attachements(email, output_folder):
    attachments = []
    if email.get_content_maintype() == 'multipart':
        for part in email.walk():
            if part.get_content_maintype() == 'multipart': continue
            if part.get('Content-Disposition') is None: continue

            filename = part.get_filename()

            if filename.endswith("jpg") or filename.endswith("jpeg") or filename.endswith("png"):
                attachments.append(os.path.join(output_folder, filename))
                fb = open(os.path.join(output_folder, filename),'wb') # TODO: Add catch here
                fb.write(part.get_payload(decode=True))
                fb.close()
    return attachments

def cleanup_attachments():
    pass