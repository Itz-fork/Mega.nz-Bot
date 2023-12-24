# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Contains code related to custom pyrogram.Client

import os
import logging

from typing import Callable
from dotenv import load_dotenv
from asyncio import sleep as xsleep
from pyrogram.types import Message
from pyrogram import Client, errors

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
    Custom pyrogram client for Megan.nz-Bot
    """

    version = "v2-nightly"
    dl_loc = None
    tmp_loc = None

    def __init__(self):
        print("--------------------")

        print("> Loading config")
        load_dotenv()
        self.dl_loc = os.getenv("DOWNLOAD_LOCATION")
        self.tmp_loc = f"{self.dl_loc}/temps"

        print("> Initializing client")
        super().__init__(
            "MegaBot",
            bot_token=os.getenv("BOT_TOKEN"),
            api_id=os.getenv("APP_ID"),
            api_hash=os.getenv("API_HASH"),
            plugins=dict(root="megadl/modules"),
            sleep_threshold=10,
        )

        # creating directories
        print("> Creating directories")
        if not os.path.isdir(self.dl_loc):
            os.makedirs(self.dl_loc)

        if not os.path.isdir(self.tmp_loc):
            os.makedirs(self.tmp_loc)

        print("--------------------")

    @classmethod
    def handle_checks(self, func: Callable) -> Callable:
        """
        Decorator to handle,
            - errors
            - private mode
        """

        async def fn_run(client: Client, msg: Message):
            try:
                return await func(client, msg)
            # Floodwait handling
            except errors.FloodWait as e:
                await xsleep(e.value)
                return await func(client, msg)
            # Other exceptions
            except Exception as e:
                logging.warning(_emsg.format(self.version, func.__module__, e))

        return fn_run

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
