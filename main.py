import mailbox
import os
import logging
import pyinotify

from constants import MAILBOX_PATH, PICTURE_PATH, MAILBOX_FOLDER
from mailaccess import MAILACCESS

def main():
    if not os.path.exists(PICTURE_PATH):
        os.makedirs(PICTURE_PATH)

    # Invoke check on startup
    MAILACCESS.invoke_callback()
    MAILACCESS.modifications = 0

    # Setup watchers on the root folder where the mail file is stored
    wm = pyinotify.WatchManager()
    wm.add_watch(MAILBOX_FOLDER, pyinotify.ALL_EVENTS)
    notifier = pyinotify.Notifier(wm, MAILACCESS.change_handler)

    notifier.loop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Started")
    main()