# Email to Telegram Group Bot

Telegram bot that reads a mailbox file and forwards it to a Telegram channel. It can handle png and jpeg attachments. 

# Installation
```
pip3 install --user -r requirements.txt
```

# Configuration
Copy `config.def.ini` to `config.ini` and edit it.

You can get the channel's `chat_id` from the web version of telegram.

# Example service file
```
[Unit]
Description=Starts email to telegram bot

[Service]
User=telegrambot
WorkingDirectory=/path/to/directory
ExecStart=/usr/bin/python3 /path/to/directory/main.py

[Install]
WantedBy=multi-user.target
```
