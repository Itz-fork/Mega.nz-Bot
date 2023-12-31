# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Authorize mega account of users


from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message

from megadl import CypherClient


@CypherClient.on_message(filters.command("login"))
@CypherClient.run_checks
async def mega_logger(client: CypherClient, msg: Message):
    if msg.chat.type != ChatType.PRIVATE:
        return await msg.reply("`You can only login in private chats for obivious reasons`")
    user_id = msg.chat.id

    email = await client.ask(user_id, "`Enter your Mega.nz email:`")
    if not email:
        return await msg.reply("You` **must** `send your Mega.nz email in order to login")
    password = await client.ask(user_id, "`Enter your Mega.nz password:`")
    if not password:
        return await msg.reply("`You` **must** `send your Mega.nz password in order to login`")

    # encrypt the email and password for security
    email = client.cipher.encrypt(email.text.encode())
    password = client.cipher.encrypt(password.text.encode())

    await client.database.mega_login(user_id, email, password)
    await msg.reply("`Successfully logged in ✅`")


@CypherClient.on_message(filters.command("logout"))
@CypherClient.run_checks
async def mega_logoutter(client: CypherClient, msg: Message):
    really = await client.ask(msg.chat.id, "Are you sure you want to logout? (y/n)")
    if really.text.lower() == "y":
        await client.database.mega_logout(msg.chat.id)
        await msg.reply("`Successfully logged out ✅`")
    else:
        await msg.reply("`Logout cancelled ❌`")
