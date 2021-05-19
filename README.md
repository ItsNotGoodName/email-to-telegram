# Email to Telegram

Telegram bot that reads a mail file and forwards to Telegram chat.
It has to be paired up with a mail server such as [Postfix](<https://en.wikipedia.org/wiki/Postfix_(software)>).
It can handle forwarding image attachments that are PNG or JPG.

An Ansible role is available.
https://github.com/ItsNotGoodName/ansible-role-email-to-telegram

# Installation

```
pip install email-to-telegram
```

# Configuration

Copy and edit `config.def.ini` to one of the following paths.

- `/etc/email-to-telegram/config.ini`
- `config.ini`

You can get the `chat_id` from the web version of Telegram.
https://stackoverflow.com/a/45577773

# Example systemd service file

```
[Unit]
Description=Starts email-to-telegram
After=network.target

[Service]
User=telegram
ExecStart=email-to-telegram
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```
