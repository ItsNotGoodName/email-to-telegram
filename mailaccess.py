import pyinotify
import logging
import mailbox

from utils import extract_email

class _OnChangeHandler(pyinotify.ProcessEvent):
    def my_init(self,**kargs):
        self.parent = kargs["parent"]
        self.mailbox_name = kargs["mailbox_name"]

    def process_IN_DELETE(self, event):
        logging.debug(f"IN_DELETE Executed Event: {event}")
        if event.name == f"{self.mailbox_name}.lock":
            if self.parent.modifications == 0:
                logging.debug("Starting mailbox consumption")
                self.parent.invoke_callback()
                logging.debug("Mailbox consumption finished")
            if self.parent.modifications > 0:
                self.parent.modifications -= 1

class MailAccess():
    def __init__(self, mailbox_name, mailbox_path, attachment_folder, callback=None):
        self.mailbox_name = mailbox_name
        self.mailbox_path = mailbox_path
        self.attachment_folder = attachment_folder
        self._callback = callback

        self.modifications = 0
        self.on_change_handler = _OnChangeHandler(parent=self, mailbox_name=mailbox_name)

    def set_callback(self, callback):
        self._callback = callback

    def invoke_callback(self):
        if(self._callback==None):
            logging.error("No callback setup")
            return
        self._callback(self)

    def parse_emails(self):
        mbox = mailbox.mbox(self.mailbox_path)
        parsed_emails = [] 
        try:
            mbox.lock()
        except mailbox.ExternalClashError:
            logging.error("Mailbox not consumed, it is being access by another program")
        else:
            keys = mbox.keys()
            for key in keys:
                email = mbox.pop(key)
                parsed_emails.append(extract_email(email, self.attachment_folder))

            mbox.flush()
            mbox.unlock()
            self.modifications += 3
        finally:
            return parsed_emails

    def clear_emails(self):
        mbox = mailbox.mbox(self.mailbox_path)
        try:
            mbox.lock()
        except mailbox.ExternalClashError:
            logging.error("Mailbox not cleared, it is being access by another program")
        else:
            mbox.clear()
            mbox.flush()
            mbox.unlock()
            self.modifications += 3 