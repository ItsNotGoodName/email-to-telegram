import pyinotify
import logging
import mailbox

from utils import extract_message, dispatch_telegram
from constants import MAILBOX_NAME, MAILBOX_PATH

class _OnChangeHandler(pyinotify.ProcessEvent):
    def my_init(self,**kargs):
        self.callback = kargs["callback"]
        self.parent = kargs["parent"]
        self.mailbox_name = kargs["mailbox_name"]

    def process_IN_DELETE(self, event):
        logging.debug(f"IN_DELETE Executed Event: {event}")
        if event.name == f"{self.mailbox_name}.lock":
            if self.parent.modifications == 0:
                logging.debug("Starting mailbox consumption")
                self.callback(self.parent)
                logging.debug("Mailbox consumption finished")
            if self.parent.modifications > 0:
                self.parent.modifications -= 1

class _MailAccess():
    def __init__(self, mailbox_name, mailbox_path, callback):
        self.mailbox_name = mailbox_name
        self.mailbox_path = mailbox_path
        self.modifications = 0
        self.callback = callback
        self.change_handler = _OnChangeHandler(parent=self, callback=callback, mailbox_name=mailbox_name)

    def invoke_callback(self):
        self.callback(self)

    def mailbox_parse_messages(self):
        mbox = mailbox.mbox(self.mailbox_path)
        parsed_messages = [] 
        try:
            mbox.lock()
        except mailbox.ExternalClashError:
            logging.error("Mailbox not consumed, it is being access by another program")
        else:
            keys = mbox.keys()
            for key in keys:
                message = mbox.pop(key)
                parsed_messages.append(extract_message(message))

            mbox.flush()
            mbox.unlock()
            self.modifications += 3
        finally:
            return parsed_messages

    def mailbox_clear_messages(self):
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

def consume_mailbox(mail_access):
    parsed_messages = mail_access.mailbox_parse_messages()
    dispatch_telegram(parsed_messages)

MAILACCESS = _MailAccess(MAILBOX_NAME, MAILBOX_PATH, consume_mailbox)