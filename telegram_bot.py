from telegram.ext import Updater, CommandHandler
from telegram import InputMediaPhoto
import logging
from time import time, sleep

class TelegramBot():
    def __init__(self, token, message_timeout):
        self.last_message_time = 0
        self.message_timeout = message_timeout
        self.updater = Updater(token=token, use_context=True)
        self.updater.dispatcher.add_handler(CommandHandler("ping", self._ping))
        self.updater.start_polling()

    def _ping(self, update, context):
       update.message.reply_text('pong', disable_notification=True) 

    def send_message(self, message, chat_id, disable_notification=False):
        if(time() - self.last_message_time < self.message_timeout):
            logging.debug(f"Sleeping for {self.message_timeout}")
            sleep(self.message_timeout)

        try:
            self.updater.bot.sendMessage(chat_id=chat_id, text=message, disable_notification=disable_notification, parse_mode="html")
        except Exception as e: # TODO: Be specific on on exceptions
            logging.error(e)

        self.last_message_time = time()


    def send_photos(self, caption, paths, chat_id):
        if(time() - self.last_message_time < self.message_timeout):
            logging.debug(f"Sleeping for {self.message_timeout}")
            sleep(self.message_timeout)

        try:
            num_paths = len(paths)
            if(num_paths == 1):
                self.updater.bot.send_photo(chat_id=chat_id, photo=open(paths[0], 'rb'), caption=caption, parse_mode="html")
            elif(num_paths >= 2 and num_paths <= 10):
                media = []
                for path in paths:
                    media.append(InputMediaPhoto(open(path, "rb")))

                media[0].caption = caption
                media[0].parse_mode = "html"
                self.updater.bot.sendMediaGroup(chat_id=chat_id, media=media)
            else:
                logging.error(f"paths length is too small or too big, length {str(num_paths)}")
        except Exception as e: # TODO: Be specific on on exceptions
            logging.error(e)

        self.last_message_sent = time()