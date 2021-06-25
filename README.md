# Email to Telegram

Telegram bot that reads a mail file and forwards to Telegram chat(s).
Requires [Postfix](https://en.wikipedia.org/wiki/Postfix_(software)) to receive emails.
Can handle forwarding image attachments that are `PNG` or `JPG`.  An Ansible role is [available](https://github.com/ItsNotGoodName/ansible-role-email-to-telegram).

# Installation

```
pip install email-to-telegram
```

# Configuration

Copy `config.def.ini` to one of the following locations.

- `config.ini`
- `/etc/email-to-telegram/config.ini`

You can get the [`chat_id`](https://stackoverflow.com/a/45577773) from the web version of Telegram.

## Service File

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
