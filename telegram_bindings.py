from telegram.ext import Updater, CommandHandler
from telegram import InputMediaPhoto
import threading  
import logging
from time import time, sleep

from constants import CHAT_ID, TOKEN, SECONDS_BETWEEN_MESSAGES

class _telegram_bot():
    def __init__(self):
        self.last_message_time = 0
        self.updater = Updater(token=TOKEN, use_context=True)

    def send_message(self, message):
        if(time() - self.last_message_time < SECONDS_BETWEEN_MESSAGES):
            logging.debug(f"Sleeping for {SECONDS_BETWEEN_MESSAGES}")
            sleep(SECONDS_BETWEEN_MESSAGES)

        try:
            self.updater.bot.sendMessage(chat_id=CHAT_ID, text=message)
        except Exception:
            logging.error("Too Much Spam")

        self.last_message_time = time()


    def send_photos(self, caption, paths):
        if(time() - self.last_message_time < SECONDS_BETWEEN_MESSAGES):
            logging.debug(f"Sleeping for {SECONDS_BETWEEN_MESSAGES}")
            sleep(SECONDS_BETWEEN_MESSAGES)

        try:
            num_paths = len(paths)
            if(num_paths == 1):
                self.updater.bot.send_photo(chat_id=CHAT_ID, photo=open(paths[0], 'rb'), caption=caption)
            elif(num_paths >= 2 and num_paths <= 10):
                media = []
                for path in paths:
                    media.append(InputMediaPhoto(open(path, "rb")))

                media[0].caption = caption
                self.updater.bot.sendMediaGroup(chat_id=CHAT_ID, media=media)
            else:
                logging.error(f"paths length is too small or too big, length {str(num_paths)}")
        except Exception:
            logging.error("Too Much Spam")

        self.last_message_sent = time()

telegram_bot = _telegram_bot()

telegram_bot.updater.start_polling()

def ping(update, context):
   """Send a message when the command /start is issued."""
   update.message.reply_text('pong') 
  
telegram_bot.updater.dispatcher.add_handler(CommandHandler("ping", ping))