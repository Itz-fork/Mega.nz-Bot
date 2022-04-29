# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

from pyrogram import Client
from config import Config

meganzbot = Client(
        name="MegaBot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins=dict(root="megadl/modules"),
        sleep_threshold=10
    )