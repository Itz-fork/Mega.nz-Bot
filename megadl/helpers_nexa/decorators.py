# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

from pyrogram import Client
from pyrogram.types import Message
from typing import Callable

from megadl.data import get_buttons
from config import Config


def is_public(func: Callable) -> Callable:
    async def deco(megabot: Client, message: Message):
        try:
            if not Config.IS_PUBLIC_BOT:
                if message.from_user.id not in Config.AUTH_USERS:
                    return await message.reply_text(
                        "**Sorry this bot isn't a Public Bot 🥺! But You can make your own bot ☺️, Click on Below Button!**",
                        reply_markup=await get_buttons("github"))
            return await func(megabot, message)
        except Exception as e:
            await message.reply(f"**Error:** \n`{e}`")
    return deco
