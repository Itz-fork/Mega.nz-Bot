# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

from pyrogram import Client
from config import Config


MeganzBot = Client(
    "Meganz Bot",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="megadl")
)
MeganzBot.run()
