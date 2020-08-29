from telegram.ext import Updater, CommandHandler
from telegram import InputMediaPhoto
import logging
from time import time, sleep

class TelegramBot():
    def __init__(self, token, seconds_between_messages):
        self.last_message_time = 0
        self.seconds_between_messages = seconds_between_messages
        self.updater = Updater(token=token, use_context=True)
        self.updater.dispatcher.add_handler(CommandHandler("ping", self._ping))
        self.updater.start_polling()

    def _ping(self, update, context):
       update.message.reply_text('pong', disable_notification=True) 

    def send_message(self, message, chat_id, disable_notification=False):
        if(time() - self.last_message_time < self.seconds_between_messages):
            logging.debug(f"Sleeping for {self.seconds_between_messages}")
            sleep(self.seconds_between_messages)

        try:
            self.updater.bot.sendMessage(chat_id=chat_id, text=message, disable_notification=disable_notification)
        except Exception: # TODO: Be specific on on exceptions
            logging.error("Too Much Spam")

        self.last_message_time = time()


    def send_photos(self, caption, paths, chat_id):
        if(time() - self.last_message_time < self.seconds_between_messages):
            logging.debug(f"Sleeping for {self.seconds_between_messages}")
            sleep(self.seconds_between_messages)

        try:
            num_paths = len(paths)
            if(num_paths == 1):
                self.updater.bot.send_photo(chat_id=chat_id, photo=open(paths[0], 'rb'), caption=caption)
            elif(num_paths >= 2 and num_paths <= 10):
                media = []
                for path in paths:
                    media.append(InputMediaPhoto(open(path, "rb")))

                media[0].caption = caption
                self.updater.bot.sendMediaGroup(chat_id=chat_id, media=media)
            else:
                logging.error(f"paths length is too small or too big, length {str(num_paths)}")
        except Exception: # TODO: Be specific on on exceptions
            logging.error("Too Much Spam")

        self.last_message_sent = time()