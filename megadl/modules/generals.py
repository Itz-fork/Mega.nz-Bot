# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Contains all the general commands of the bot


from pyrogram import filters
from pyrogram.types import Message

from megadl import MeganzClient


@MeganzClient.on_message(filters.command("start"))
@MeganzClient.handle_checks
async def start_msg(_: MeganzClient, msg: Message):
    await msg.reply_text(
        f"""
    Hi `{msg.from_user.first_name}`, this is your personal Mega.nz bot!
    """
    )
