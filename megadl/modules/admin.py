# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Admin functions

from pyrogram import filters
from pyrogram.types import Message

from megadl import MeganzClient


@MeganzClient.on_message(filters.command("ban"))
@MeganzClient.handle_checks
async def admin_ban_user(client: MeganzClient, msg: Message):
    sender = msg.from_user.id
    if sender not in client.auth_users:
        return await msg.reply("Banning users can only be done by admins!")
    buid = None
    try:
        buid = int(msg.text.split(None, 1)[1])
    except:
        pass
    if not buid or not buid.isnumeric():
        return await msg.reply("Provide a user id to ban \n\nEx: `/ban 12345`")

    await client.database.ban_user(buid)
    await msg.reply(f"Banned user `{buid}`")


@MeganzClient.on_message(filters.command("unban"))
@MeganzClient.handle_checks
async def admin_unban_user(client: MeganzClient, msg: Message):
    sender = msg.from_user.id
    if sender not in client.auth_users:
        return await msg.reply("Unbanning users can only be done by admins!")
    buid = None
    try:
        buid = int(msg.text.split(None, 1)[1])
    except:
        pass
    if not buid or not buid.isnumeric():
        return await msg.reply("Provide a user id to unban \n\nEx: `/ban 12345`")

    await client.database.unban_user(buid)
    await msg.reply(f"Unbanned user `{buid}`")
