from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="email-to-telegram",
    version="1.1.1",
    description="Telegram bot that reads a mail file and forwards to Telegram chat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ItsNotGoodName/email-to-telegram",
    author="ItsNotGoodName",
    author_email="gurnaindeol@gmail.com",
    packages=find_packages(exclude="test"),
    python_requires=">=3.6, <4",
    install_requires=["python-telegram-bot>=13.5,<14.0", "watchdog>=2.1.1,<3.0.0", "mail-parser>=3.15.0,<4.0.0"],
    entry_points={
        "console_scripts": [
            "email-to-telegram=email_to_telegram.__main__:main",
        ],
    },
    keywords="bot, telegram",
    project_urls={
        "Source": "https://github.com/ItsNotGoodName/email-to-telegram",
    },
)
