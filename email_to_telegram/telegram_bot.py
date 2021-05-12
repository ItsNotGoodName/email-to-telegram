import logging

from time import time, sleep
from telegram import InputMediaPhoto
from telegram.ext import Updater, CommandHandler
from telegram.error import TelegramError


def api_interaction(func):
    def decorator(*args, **kwargs):
        self = args[0]
        if time() - self.last_message_time < self.message_timeout:
            logging.info("Sleeping for %s", self.message_timeout)
            sleep(self.message_timeout)

        try:
            func(*args, **kwargs)
        except TelegramError as error:
            logging.error(error)

        self.last_message_time = time()

    return decorator


class TelegramBot:
    def __init__(self, token, message_timeout):
        self.last_message_time = 0
        self.message_timeout = message_timeout
        self.updater = Updater(token=token, use_context=True)
        self.updater.dispatcher.add_handler(CommandHandler("ping", self._ping))
        self.updater.start_polling()

    def _ping(self, update, context):
        update.message.reply_text("pong")
        logging.debug("Replied to ping")

    @api_interaction
    def send_text(self, chat_id, text, disable_notification=False):
        self.updater.bot.sendMessage(
            chat_id=chat_id,
            text=text,
            disable_notification=disable_notification,
        )

    @api_interaction
    def send_photo(self, chat_id, paths, caption=None):
        length = len(paths)
        if length == 1:
            self.updater.bot.send_photo(
                chat_id=chat_id, photo=open(paths[0], "rb"), caption=caption
            )
        elif 2 <= length <= 10:
            media = []
            for path in paths:
                media.append(InputMediaPhoto(open(path, "rb")))

            media[0].caption = caption
            self.updater.bot.sendMediaGroup(chat_id=chat_id, media=media)
        else:
            logging.error(
                "paths length is too small or too big, length %s", str(length)
            )
