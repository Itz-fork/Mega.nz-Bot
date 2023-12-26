# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Contains code related to custom pyrogram.Client

import functools
import os
import asyncio
import logging

from typing import Callable
from dotenv import load_dotenv
from asyncio import sleep as xsleep
from pyrogram.types import Message
from pyrogram import Client, errors
from pyrogram.handlers import MessageHandler

from .database import Users
from .files import send_as_guessed, cleanup, splitit, listfiles


_emsg = """
##### Mega.nz-Bot Error Handler #####

Bot version: {}
Module: {}
Error:
{}

"""


class MeganzClient(Client):
    """
    Custom pyrogram client for Mega.nz-Bot
    """

    version = "v2-nightly"
    database = Users() if os.getenv("MONGO_URI") else None
    dl_loc = None
    tmp_loc = None

    def __init__(self):
        # set DOWNLOAD_LOCATION variable
        # if USE_ENV is True it'll use currend dir + NexaBots
        # otherwise use location defined in .env file by user
        if os.getenv("USE_ENV") in ["True", "true"]:
            self.dl_loc = f"{os.getcwd()}/NexaBots"
        else:
            self.dl_loc = os.getenv("DOWNLOAD_LOCATION")

        self.tmp_loc = f"{self.dl_loc}/temps"

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
        self.is_public = True if self.database else False
        if not self.database:
            print("     Warning: Mongodb url not found")

        # creating directories
        print("> Creating directories")
        if not os.path.isdir(self.dl_loc):
            os.makedirs(self.dl_loc)

        if not os.path.isdir(self.tmp_loc):
            os.makedirs(self.tmp_loc)

        # other stuff
        print("> Setting up additional functions")
        self.add_handler(MessageHandler(self.use_listner))
        self.tasks = {}

        print("--------------------")

    @classmethod
    def handle_checks(self, func: Callable) -> Callable:
        """
        Decorator to run middleware
        """

        async def fn_run(client: Client, msg: Message):
            try:
                # db functions
                if self.database:
                    await self.database.add(msg.from_user.id)

                return await func(client, msg)
            # Floodwait handling
            except errors.FloodWait as e:
                await xsleep(e.value)
                return await func(client, msg)
            # Other exceptions
            except Exception as e:
                logging.warning(_emsg.format(self.version, func.__module__, e))

        return fn_run

    async def ask(self, chat_id: int, text: str, *args, **kwargs):
        await self.send_message(chat_id, text, *args, **kwargs)
        woop = asyncio.get_running_loop()
        futr = woop.create_future()

        futr.add_done_callback(
            functools.partial(lambda _, uid: self.tasks.pop(uid, None), chat_id)
        )
        self.tasks[chat_id] = {"task": futr}

        # wait for 1 min
        try:
            return await asyncio.wait_for(futr, 60.0)
        except asyncio.TimeoutError:
            await self.send_message(
                chat_id, "Task was cancelled as you haven't answered for 1 minute"
            )
            self.tasks.pop(chat_id, None)
            return None

    async def use_listner(self, _, msg: Message):
        lstn = self.tasks.get(msg.chat.id)
        if lstn and not lstn["task"].done():
            lstn["task"].set_result(msg)
        return msg.continue_propagation()

    async def send_files(self, files: list[str], chat_id: int, msg_id: int):
        """
        Send files with automatic floodwait handling and file splitting
        """
        for file in files:
            # Split files larger than 2GB
            if os.stat(file).st_size > int(os.getenv("TG_MAX_SIZE")):
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
                cleanup(splout)
            else:
                await send_as_guessed(self, file, chat_id, msg_id)

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
