import pyinotify
from constants import MAILBOX_PATH, MAILBOX_FOLDER, MAILBOX_NAME
from time import sleep, time
from main import consume_mailbox, init
import logging

class OnWriteHandler(pyinotify.ProcessEvent):
    def my_init(self):
        self.modifications = 0

    def process_IN_DELETE(self, event):
        if(event.name == f"{MAILBOX_NAME}.lock" and self.modifications <= 0):
            consume_mailbox()
            logging.debug("CONSUMED")
            self.modifications = 3
        self.modifications -= 1

def main():
    init()
    wm = pyinotify.WatchManager()
    wm.add_watch(MAILBOX_FOLDER, pyinotify.ALL_EVENTS)
    notifier = pyinotify.Notifier(wm, OnWriteHandler())
    notifier.loop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Started")
    main()