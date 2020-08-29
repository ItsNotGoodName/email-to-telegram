import pyinotify
import logging
import mailbox

from utils import extract_email

class _OnChangeHandler(pyinotify.ProcessEvent):
    def my_init(self,**kargs):
        self.parent = kargs["parent"]
        self.mailbox_name = kargs["mailbox_name"]

    def process_IN_DELETE(self, event):
        logging.debug(f"IN_DELETE Executed Event: {event} with modifications={self.parent.modifications}")
        if event.name == f"{self.mailbox_name}.lock":
            if self.parent.modifications == 0:
                logging.debug("Starting mailbox consumption")
                self.parent.invoke_callback()
                logging.debug("Mailbox consumption finished")
            if self.parent.modifications > 0:
                self.parent.modifications -= 1

class MailAccess():
    def __init__(self, mail_folder, mail_file, mail_path, attachments_folder, callback=None):
        self.mail_file = mail_file
        self.mail_path = mail_path
        self.attachments_folder = attachments_folder
        self._callback = callback

        self.modifications = 0
        self.on_change_handler = _OnChangeHandler(parent=self, mailbox_name=mail_file)

        # Setup watchers on the root folder where the mail file is stored
        wm = pyinotify.WatchManager()
        wm.add_watch(mail_folder, pyinotify.ALL_EVENTS)
        self.notifier = pyinotify.Notifier(wm, self.on_change_handler)

    def set_callback(self, callback, andExecute=False):
        self._callback = callback
        if andExecute:
            self.invoke_callback()
            self.modifications = 0

    def invoke_callback(self):
        if(self._callback==None):
            logging.error("No callback setup")
            return
        self._callback(self)

    def parse_emails(self):
        mbox = mailbox.mbox(self.mail_path)
        parsed_emails = [] 
        try:
            mbox.lock()
        except mailbox.ExternalClashError:
            logging.error("Mailbox not consumed, it is being access by another program")
        else:
            keys = mbox.keys()
            for key in keys:
                email = mbox.pop(key)
                parsed_emails.append(extract_email(email, self.attachments_folder))

            mbox.flush()
            mbox.unlock()
            self.modifications += 2
        finally:
            return parsed_emails

    def clear_emails(self):
        mbox = mailbox.mbox(self.mail_path)
        try:
            mbox.lock()
        except mailbox.ExternalClashError:
            logging.error("Mailbox not cleared, it is being access by another program")
        else:
            mbox.clear()
            mbox.flush()
            mbox.unlock()
            self.modifications += 2