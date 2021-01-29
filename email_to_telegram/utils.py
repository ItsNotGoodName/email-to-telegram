import os
import email
from email.header import decode_header
import re
import logging


def extract_email(email, output_folder):
    picture_paths = extract_attachements(email, output_folder)
    e = email.message_from_string(email)
    e["To"] = re.findall("([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)", e["To"])[
        0
    ]
    e["Body"] = extract_body(email)
    if len(picture_paths) == 0:  # It is a normal message
        e["Type"] = "message"
        return e

    e["Type"] = "picture"
    e["Attachments"] = picture_paths
    return e


def extract_attachements(email, output_folder):
    attachments = []
    if email.get_content_maintype() == "multipart":
        for part in email.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get("Content-Disposition") is None:
                continue

            filename = part.get_filename() or ""

            if (
                filename.endswith("jpg")
                or filename.endswith("jpeg")
                or filename.endswith("png")
            ):
                attachments.append(os.path.join(output_folder, filename))
                fb = open(
                    os.path.join(output_folder, filename), "wb"
                )  # TODO: Add catch here
                fb.write(part.get_payload(decode=True))
                fb.close()
            elif filename == None:
                logging.error("Attachment does not have filename")
    return attachments


def extract_body(email):
    if email.is_multipart():
        for part in email.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))

            # skip any text/plain (txt) attachments
            if (
                ctype == "text/plain" or ctype == "text/html"
            ) and "attachment" not in cdispo:
                return str(part.get_payload(decode=True), "utf-8")  # decode
    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        return str(email.get_payload(decode=True), "utf-8")
    return ""


def cleanup_attachments():
    pass
