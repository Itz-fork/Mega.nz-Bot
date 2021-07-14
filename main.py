# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

from pyrogram import Client, idle
from config import Config


if __name__ == "__main__" :
    Megadlbot = Client(
        "Nexa MegaDl",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins=dict(root="megadl")
    )
    Megadlbot.start()
    idle()
