from constants import TOKEN, MESSAGE_TIMEOUT, MAIL_FOLDER, ATTACHMENTS_FOLDER, MAIL_FILE, MAIL_PATH
from telegram_bot import TelegramBot
from mailaccess import MailAccess

telegram_bot = TelegramBot(TOKEN, MESSAGE_TIMEOUT)
mail_access = MailAccess(MAIL_FOLDER, MAIL_FILE, MAIL_PATH,  ATTACHMENTS_FOLDER)