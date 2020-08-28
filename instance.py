from constants import TOKEN, SECONDS_BETWEEN_MESSAGES, CHAT_ID, MAILBOX_NAME, MAILBOX_FOLDER, MAILBOX_PATH, PICTURE_PATH
from telegram_bot import TelegramBot
from mailaccess import MailAccess

telegram_bot = TelegramBot(TOKEN, SECONDS_BETWEEN_MESSAGES, CHAT_ID)
mail_access = MailAccess(MAILBOX_NAME, MAILBOX_FOLDER, MAILBOX_PATH, PICTURE_PATH)