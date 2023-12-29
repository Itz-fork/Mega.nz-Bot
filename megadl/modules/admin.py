# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Admin functions

from pyrogram import filters
from pyrogram.types import Message

from megadl import MegaCypher


@MegaCypher.on_message(filters.command("info"))
@MegaCypher.run_checks
async def admin_user_info(client: MegaCypher, msg: Message):
    if client.auth_users == "*" or msg.from_user.id not in client.auth_users:
        return await msg.reply("Getting user info can only be done by admins!")

    buid = None
    try:
        buid = int(msg.text.split(None, 1)[1])
    except:
        pass
    if not buid or not isinstance(buid, int):
        return await msg.reply("Provide a user id to get info \n\nEx: `/info 12345`")

    _user = await client.database.is_there(buid)
    if not _user:
        return await msg.reply("Unable to find user in the database 🔎")

    status = _user["status"]
    is_ban = status["banned"]
    ban_rsn = status["reason"]
    dl_count = _user["total_downloads"]
    up_count = _user["total_uploads"]

    ban_status = (
        f"`Banned`\n      ↳ `{ban_rsn}`"
        if is_ban
        else "Admin"
        if buid in client.auth_users
        else "`Active`"
    )
    await msg.reply(
        f"""
**User Info**
    ↳ **ID:** `{buid}`
    ↳ **Status:** {ban_status}
    ↳ **Total downloads:** `{dl_count}`
    ↳ **Total uploads:** `{up_count}`


**Detect abuse?**
If you think above total counts are abnormal, you can ban the user with `/ban {buid} abusing`
"""
    )


@MegaCypher.on_message(filters.command("ban"))
@MegaCypher.run_checks
async def admin_ban_user(client: MegaCypher, msg: Message):
    if msg.from_user.id not in client.auth_users:
        return await msg.reply("Banning users can only be done by admins!")

    buid = None
    reason = None
    try:
        _splt = msg.text.split(None, 1)
        buid = int(_splt[1])
        reason = _splt[2] if len(_splt) >= 3 else "No reason given"
    except:
        return await msg.reply("Provide a user id to ban \n\nEx: `/ban 12345 spamming`")

    if buid in client.auth_users:
        return await msg.reply("Why do you want to ban an admin 😶‍🌫️?")

    await client.database.ban_user(buid, reason)
    await msg.reply(f"Banned user `{buid}`")


@MegaCypher.on_message(filters.command("unban"))
@MegaCypher.run_checks
async def admin_unban_user(client: MegaCypher, msg: Message):
    if msg.from_user.id not in client.auth_users:
        return await msg.reply("Unbanning users can only be done by admins!")
    buid = None
    try:
        buid = int(msg.text.split(None, 1)[1])
    except:
        pass
    if not buid or not isinstance(buid, int):
        return await msg.reply("Provide a user id to unban \n\nEx: `/unban 12345`")

    await client.database.unban_user(buid)
    await msg.reply(f"Unbanned user `{buid}`")
