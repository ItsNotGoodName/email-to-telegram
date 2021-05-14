# Email to Telegram

A telegram bot that reads a mailbox file and forwards it to a Telegram chat.
This can be paired up with a mail server such as [Postfix](https://en.wikipedia.org/wiki/Postfix_(software)).
It can handle forwarding image attachments that are PNG or JPG.

An Ansible role is available:
https://github.com/ItsNotGoodName/role-email-to-telegram

# Installation
```
pip3 install .
```

# Configuration
Copy `config.def.ini` to `/etc/email-to-telegram/config.ini` and edit it.

You can get the `chat_id` from the web version of Telegram.  
https://stackoverflow.com/a/45577773

# Example systemd service file
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
