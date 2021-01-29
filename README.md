# Email to Telegram
**Warning: Spaghetti**

Telegram bot that reads a mailbox file and forwards it to the appropriate Telegram chat. It can handle png and jpg attachments. 

This requires postfix to receive emails.

Ansible role: https://github.com/ItsNotGoodName/role-email-to-telegram

# Installation
```
pip3 install .
```

# Configuration
Copy `config.def.ini` to `/etc/email-to-telegram/config.ini` and edit it.

You can get the `chat_id` from the web version of Telegram.

# Example Systemd service file
```
[Unit]
Description=Starts email-to-telegram-bot
After=network.target

[Service]
User=telegram
ExecStart=email-to-telegram
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```
