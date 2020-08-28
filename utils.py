import os
from email.header import decode_header
import logging

def decode_email_subject(subject):
    s = (decode_header(subject)[0][0])
    return str(s, 'utf-8')

def extract_email(email, output_folder):
    picture_paths = extract_attachements(email, output_folder)
    if len(picture_paths) == 0: # It is a normal message
        return {"subject": decode_email_subject(email["subject"]), "body": extract_body(email),"type": "message"}
    return {"subject": decode_email_subject(email["subject"]), "body": extract_body(email), "attachments": picture_paths, "type": "picture"}

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

def extract_body(email):
    if email.is_multipart():
        for part in email.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                return str(part.get_payload(decode=True), 'utf-8')  # decode
    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        return str(email.get_payload(decode=True), 'utf-8')

def cleanup_attachments():
    pass