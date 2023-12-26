# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Contains commands related to mega auth


from pyrogram import filters
from pyrogram.types import Message

from cryptography.fernet import Fernet

from megadl import MeganzClient


@MeganzClient.on_message(filters.command("login"))
@MeganzClient.handle_checks
async def mega_logger(client: MeganzClient, msg: Message):
    user_id = msg.chat.id
    email = await client.ask(user_id, "Enter your Mega.nz email:")
    password = await client.ask(user_id, "Enter your Mega.nz password:")

    # if user doesn't reply
    if None in (email, password):
        return await msg.reply(
            "You must send your Mega.nz email and password in order to login"
        )

    # encrypt the email and password for security
    email = client.cipher.encrypt(email.text.encode())
    password = client.cipher.encrypt(password.text.encode())

    await client.database.mega_login(user_id, email, password)

    await msg.reply("Successfully logged in!")
