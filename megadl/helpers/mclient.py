# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Custom pyrogram client useful methods

import os
import asyncio
import logging
import functools

from typing import Callable
from asyncio import sleep as xsleep
from cryptography.fernet import Fernet

from pyrogram.types import Message
from pyrogram import Client, errors
from pyrogram.handlers import MessageHandler

from .database import Users
from .files import send_as_guessed, fs_cleanup, splitit, listfiles


_emsg = """
##### Mega.nz-Bot Error Handler #####

Version: {}
Module: {}
Error:
{}

"""


class MeganzClient(Client):
    """
    Custom pyrogram client for Mega.nz-Bot
    """

    version = "cypher-1.0"
    dl_loc = None
    tmp_loc = None
    database = Users() if os.getenv("MONGO_URI") else None
    auth_users = (
        set(map(int, os.getenv("AUTH_USERS").split()))
        if os.getenv("AUTH_USERS") and os.getenv("AUTH_USERS") != "*"
        else "*"
    )

    def __init__(self):
        # set DOWNLOAD_LOCATION variable
        # if USE_ENV is True it'll use currend dir + NexaBots
        # otherwise use location defined in .env file by user
        print("> Setting up file locations")
        self.cwd = os.getcwd()
        if os.getenv("USE_ENV") in ["True", "true"]:
            self.dl_loc = f"{self.cwd}/NexaBots"
        else:
            self.dl_loc = os.getenv("DOWNLOAD_LOCATION")

        self.tmp_loc = f"{self.dl_loc}/temps"
        self.mx_size = int(os.getenv("TG_MAX_SIZE", 2040108421))

        if not os.path.isdir(self.dl_loc):
            os.makedirs(self.dl_loc)

        if not os.path.isdir(self.tmp_loc):
            os.makedirs(self.tmp_loc)

        # Initializing pyrogram
        print("> Initializing client")
        super().__init__(
            "MegaBot",
            bot_token=os.getenv("BOT_TOKEN"),
            api_id=os.getenv("APP_ID"),
            api_hash=os.getenv("API_HASH"),
            plugins=dict(root="megadl/modules"),
            sleep_threshold=10,
        )

        # Initializing mongodb
        print("> Initializing database")
        self.glob_tmp = {}
        self.cipher = None
        self.is_public = True if self.database else False

        if self.is_public:
            # check if private key exists as a file
            key_loc = f"{os.getcwd()}/cipher.key"
            if os.path.isfile(key_loc):
                with open(key_loc, "r") as f:
                    key = f.read().encode()
                    self.cipher = Fernet(key)
            # check if private key exists as an env var
            elif os.getenv("CIPHER_KEY"):
                self.cipher = Fernet(os.getenv("CIPHER_KEY").encode())
            # otherwise exit with error code 1
            # although we can generate a new key that's not a good idea
            # because if deployer lose it, it'll make all the existing data useless
            # too much black magic leads to chaos
            else:
                logging.warning("Unable to find encryption key")
                exit(1)
        else:
            print("     Warning: Mongodb url not found")

        # other stuff
        print("> Setting up additional functions")
        self.listening = {}
        self.mega_running = {}
        self.add_handler(MessageHandler(self.use_listner))

        print("--------------------")

    @classmethod
    def handle_checks(self, func: Callable) -> Callable:
        """
        Decorator to run middleware
        """

        async def fn_run(client: Client, msg: Message):
            can_use = False
            uid = msg.from_user.id
            try:
                if self.database:
                    await self.database.add(uid)

                if self.auth_users == "*":
                    can_use = True

                else:
                    can_use = uid in self.auth_users

                if not can_use:
                    await msg.reply(
                        "You're not authorized to use this bot 🙅‍♂️ \n\n**Join @NexaBotsUpdates ❤️**"
                    )
                    return msg.stop_propagation()

                return await func(client, msg)
            # Floodwait handling
            except errors.FloodWait as e:
                await xsleep(e.value)
                return await func(client, msg)
            # pyrogram message not modified error handling
            except errors.MessageNotModified:
                pass
            # Other exceptions
            except Exception as e:
                logging.warning(_emsg.format(self.version, func.__module__, e))

        return fn_run

    async def ask(self, chat_id: int, text: str, *args, **kwargs):
        await self.send_message(chat_id, text, *args, **kwargs)
        woop = asyncio.get_running_loop()
        futr = woop.create_future()

        futr.add_done_callback(
            functools.partial(lambda _, uid: self.listening.pop(uid, None), chat_id)
        )
        self.listening[chat_id] = {"task": futr}

        # wait for 1 min
        try:
            return await asyncio.wait_for(futr, 60.0)
        except asyncio.TimeoutError:
            await self.send_message(
                chat_id, "Task was cancelled as you haven't answered for 1 minute 🥱"
            )
            self.listening.pop(chat_id, None)
            return None

    async def use_listner(self, _, msg: Message):
        lstn = self.listening.get(msg.chat.id)
        if lstn and not lstn["task"].done():
            lstn["task"].set_result(msg)
        return msg.continue_propagation()

    async def full_cleanup(self, path: str, msg_id: int, chat_id: int = None):
        """
        Delete the file/folder and the message
        """
        fs_cleanup(path)
        self.glob_tmp.pop(msg_id)
        if chat_id and chat_id in self.mega_running:
            self.mega_running.remove(chat_id)

    async def send_files(self, files: list[str], chat_id: int, msg_id: int):
        """
        Send files with automatic floodwait handling and file splitting
        """
        if files:
            for file in files:
                # Split files larger than 2GB
                if os.stat(file).st_size > self.mx_size:
                    await self.edit_message_text(
                        chat_id,
                        msg_id,
                        """
                        The file you're trying to upload exceeds telegram limits 😬.
                        Trying to split the files 🔪...
                        """,
                    )
                    splout = f"{self.tmp_loc}/splitted"
                    await splitit(file, splout)
                    for file in listfiles(splout):
                        await send_as_guessed(self, file, chat_id, msg_id)
                    fs_cleanup(splout)
                else:
                    await send_as_guessed(self, file, chat_id, msg_id)
        else:
            await self.edit_message_text(
                chat_id,
                msg_id,
                "Couldn't find files to send. Maybe you've canceled the process 🤔?",
            )

    async def send_document(self, *args, **kwargs):
        try:
            return await super().send_document(*args, **kwargs)
        except errors.FloodWait as fw:
            await xsleep(fw.value)
            return await self.send_document(*args, **kwargs)

    async def send_photo(self, *args, **kwargs):
        try:
            return await super().send_photo(*args, **kwargs)
        except errors.FloodWait as fw:
            await xsleep(fw.value)
            return await self.send_photo(*args, **kwargs)

    async def send_animation(self, *args, **kwargs):
        try:
            return await super().send_animation(*args, **kwargs)
        except errors.FloodWait as fw:
            await xsleep(fw.value)
            return await self.send_animation(*args, **kwargs)

    async def send_video(self, *args, **kwargs):
        try:
            return await super().send_video(*args, **kwargs)
        except errors.FloodWait as fw:
            await xsleep(fw.value)
            return await self.send_video(*args, **kwargs)

    async def send_audio(self, *args, **kwargs):
        try:
            return await super().send_audio(*args, **kwargs)
        except errors.FloodWait as fw:
            await xsleep(fw.value)
            return await self.send_audio(*args, **kwargs)
