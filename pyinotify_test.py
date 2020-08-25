import pyinotify
from constants import MAILBOX_PATH, MAILBOX_FOLDER, MAILBOX_NAME
from time import sleep, time
from main import consume_mailbox
import logging

class OnWriteHandler(pyinotify.ProcessEvent):
    def my_init(self):
        self.i_modified = False

    def process_IN_ACCESS(self, event):
        pass

    def process_IN_ATTRIB(self, event):
        pass

    def process_IN_CLOSE_NOWRITE(self, event):
        pass

    def process_IN_CLOSE_WRITE(self, event):
        pass

    def process_IN_CREATE(self, event):
        pass

    def process_IN_DELETE(self, event):
        if(event.name == f"{MAILBOX_NAME}.lock" and not self.i_modified):
            consume_mailbox()
            self.i_modified = True

    def process_IN_MODIFY(self, event):
        pass

    def process_IN_OPEN(self, event):
        pass

def main():
    wm = pyinotify.WatchManager()
    wm.add_watch(MAILBOX_FOLDER, pyinotify.ALL_EVENTS)
    notifier = pyinotify.Notifier(wm, OnWriteHandler())
    notifier.loop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Started")
    main()