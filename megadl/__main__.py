# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: __main__.py


from os import getenv
from dotenv import load_dotenv
from pyrogram import Client, idle

# .env
print("Loading env...")
load_dotenv()

# Pyrogram client
meganzbot = Client(
    name="MegaBot",
    bot_token=getenv("BOT_TOKEN"),
    api_id=getenv("APP_ID"),
    api_hash=getenv("API_HASH"),
    plugins=dict(root="megadl/modules"),
    sleep_threshold=10,
)

# Run the bot
if __name__ == "__main__":
    print("Mega.nz Bot is running...")
    meganzbot.start()
    idle()
