from telegram.ext import Updater, CommandHandler
from telegram import InputMediaPhoto
from constants import CHAT_ID, TOKEN
import logging

updater = Updater(token=TOKEN, use_context=True)

def send_message(message):
    updater.bot.sendMessage(chat_id=CHAT_ID, text=message)

def send_photos(caption, paths):
    num_paths = len(paths)
    if(num_paths == 1):
        updater.bot.send_photo(chat_id=CHAT_ID, photo=open(paths[0], 'rb'), caption=caption)
    elif(num_paths >= 2 and num_paths <= 10):
        media = []
        for path in paths:
            media.append(InputMediaPhoto(open(path, "rb")))

        media[0].caption = caption
        updater.bot.sendMediaGroup(chat_id=CHAT_ID, media=media)
    else:
        logging.error(f"paths length is too small or too big, length {str(num_paths)}")