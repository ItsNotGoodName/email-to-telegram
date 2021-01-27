from email_to_telegram.mailaccess import MailAccess
from email_to_telegram.telegram_bot import TelegramBot
from email_to_telegram.constants import TOKEN, MESSAGE_TIMEOUT, MAIL_FOLDER, ATTACHMENTS_FOLDER, MAIL_FILE, MAIL_PATH

telegram_bot = TelegramBot(TOKEN, MESSAGE_TIMEOUT)
mail_access = MailAccess(MAIL_FOLDER, MAIL_FILE, MAIL_PATH,  ATTACHMENTS_FOLDER)
