# Email to Telegram Group Bot

This watches an email folder and forwards it's emails to a Telegram group.

It handles plain text email body and also jpg and png attachments.

Use something like postfix to receive emails and edit the secrets file to point to the mail folder. Make sure the mail folder which stores the mail file is writeable by the program. Example mail folder is `/var/spool/mail` and an example mail file is `/var/spool/mail/telegrambot`.