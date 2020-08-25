from telegram.ext import Updater, CommandHandler
from constants import CHAT_ID, TOKEN

def _start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def send_message(message):
    updater.bot.sendMessage(chat_id=CHAT_ID, text=message)

def send_photos(message, paths):
    for path in paths:
        updater.bot.send_photo(chat_id=CHAT_ID, photo=open(path, 'rb'))

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', _start)
dispatcher.add_handler(start_handler)

# updater.start_polling()