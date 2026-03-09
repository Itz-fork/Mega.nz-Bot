# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Custom pyrogram client useful methods

import os
import json
import asyncio
import logging
import requests
import functools

from typing import Callable
from asyncio import sleep as xsleep
from cryptography.fernet import Fernet

from pyrogram import Client, errors
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message, CallbackQuery


from .database import CypherDB
from .sysfncs import run_on_shell, kill_family
from .files import send_as_guessed, fs_cleanup, splitit, listfiles

_emsg = """
##### Mega.nz-Bot Error Handler #####

Raised by: {}
Version: {}
Module: {}
Error:
{}

"""


class MeganzClient(Client):
    """
    Custom pyrogram client for Mega.nz-Bot
    """

    version = "2.0.1"
    dl_loc = None
    tmp_loc = None
    database = CypherDB() if os.getenv("MONGO_URI") else None

    def __init__(self):
        # set DOWNLOAD_LOCATION variable
        # if USE_ENV is True it'll use currend dir + NexaBots
        # otherwise use location defined in .env file by user
        print("> Setting up file locations")
        self.cwd = os.getcwd()
        if os.getenv("USE_ENV") in ["True", "true"] or not os.getenv(
            "DOWNLOAD_LOCATION"
        ):
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
            "MegaBotCypher",
            bot_token=os.getenv("BOT_TOKEN"),
            api_id=os.getenv("APP_ID"),
            api_hash=os.getenv("API_HASH"),
            plugins=dict(root="megadl/modules"),
            sleep_threshold=10,
        )

        # Initializing mongodb
        print("> Initializing database")
        self.glob_tmp = {}
        self.environs = os.environ.copy()
        self.cipher = None

        print("> Updating privacy settings")
        _auths = os.getenv("AUTH_USERS")
        self.auth_users = (
            set()
            if not isinstance(_auths, (list, str))
            else set(map(int, os.getenv("AUTH_USERS").split()))
            if not _auths.startswith("*")
            else {"*"}
            if len(_auths) < 2
            else set(map(int, _auths.split("|")[1].split())).union({"*"})
        )
        log_chat = os.getenv("LOG_CHAT")
        self.log_chat = int(log_chat) if log_chat and log_chat != "-1001234567890" else None
        self.use_logs = {"dl_from", "up_to"}
        self.req_db_fn = {"mega_logger", "mega_logoutter", "set_user_proxy"}
        self.is_public = True if self.database else False

        if self.is_public:
            # check if private key exists as a file
            key_loc = f"{os.getcwd()}/cipher.key"
            if os.path.isfile(key_loc):
                with open(key_loc, "r") as f:
                    key = f.read().encode()
                    self.cipher = Fernet(key)
            # check if private key exists as an env var
            elif os.getenv("CYPHER_KEY"):
                self.cipher = Fernet(os.getenv("CYPHER_KEY").encode())
            # otherwise exit with error code 1
            # although we can generate a new key that's not a good idea
            # because if deployer lose it, it'll make all the existing data useless
            # too much black magic leads to chaos
            else:
                logging.warning("Unable to find encryption key")
                exit(1)
        else:
            logging.warning("Warning: Mongodb url not found")

        # Check for updates
        print("> Checking for updates")
        try:
            remote_updates = requests.get(
                "https://raw.githubusercontent.com/Itz-fork/Mega.nz-Bot/main/updates.json",
                timeout=10
            ).json()
            
            with open("updates.json", "r") as f:
                local_updates = json.load(f)
                if remote_updates["commit"] != local_updates["commit"]:
                    print("    |> New update found, updating...")
                    run_on_shell("git update-index --assume-unchanged .env mega.ini")
                    run_on_shell("git pull")
                    self.version = remote_updates["version"]
                    self.send_message(
                        self.log_chat,
                        f"**#UPDATE** \n\n**Version:** `{self.version}` \n**Date:** `{remote_updates['date']}` \n**Changes:** `{remote_updates['message']}`",
                    )
        except (requests.RequestException, json.JSONDecodeError, KeyError, FileNotFoundError) as e:
            logging.warning(f"Auto-update check failed: {e}")

        # other stuff
        print("> Setting up additional functions")
        self.listening = {}
        self.mega_running = {}
        self.ddl_running = {}
        self.add_handler(MessageHandler(self.use_listner))


    def run_checks(self, func) -> Callable:
        """
        Decorator to run middleware
        """

        async def cy_run(client: Client, msg: Message | CallbackQuery):
            can_use = False
            # use message of the query if it's a callback query
            uid = msg.from_user.id

            try:
                # no need to use "Cypher.cyeor" as `use_logs` are Message handlers
                _func_name = func.__name__
                if _func_name in self.use_logs:
                    # return if user has already started a process
                    if uid in self.mega_running or uid in self.ddl_running:
                        return await msg.reply(
                            "`You've already started a process. Wait until it's finished before starting another one 🥱`"
                        )
                    # send logs to the log chat if available
                    if self.log_chat:
                        _frwded = await msg.forward(chat_id=self.log_chat)
                        await _frwded.reply(
                            f"**#UPLOAD_LOG** \n\n**From:** `{uid}` \n**Get history:** `/info {uid}`"
                        )

                # admin function handling
                # if you are modifying this code: Never have a function name start with "admin_" prefix
                # unless its indended to be used by one
                if _func_name.startswith("admin") or _func_name in self.req_db_fn:
                    if not self.database:
                        await self.cyeor(
                            msg,
                            "`Please set up database to use this feature!`",
                            True,
                        )
                        return msg.stop_propagation()
                    if uid not in client.auth_users:
                        await self.cyeor(
                            msg,
                            "✋🛑 Only admins can use this command. Fuck off, will you?",
                            True,
                        )
                        return msg.stop_propagation()

                # Check auth users
                if self.database:
                    status = await self.database.add(uid)
                    if status["banned"]:
                        return await self.cyeor(
                            msg,
                            f"**You're banned from using this bot 😬** \n\n**Reason:** `{status['reason']}`",
                            True,
                        )

                if "*" in self.auth_users:
                    can_use = True
                else:
                    can_use = uid in self.auth_users

                if not can_use:
                    await self.cyeor(
                        msg,
                        "`You're not authorized to use this bot 🙅‍♂️` \n\n**Join @NexaBotsUpdates ❤️**",
                        True,
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
            except FileExistsError:
                await self.cyeor(
                    msg, "`File already exists in the server. Try again after I wipe your data 😬`"
                )
                await self.full_cleanup(f"{self.dl_loc}/{uid}", uid)
            # Other exceptions
            except Exception as e:
                await self.cyeor(msg, f"**Oops 🫨, Somethig bad happend!** \n\n`{e}`")
                await self.full_cleanup(f"{self.dl_loc}/{uid}", uid)
                logging.warning(
                    _emsg.format(func.__name__, self.version, func.__module__, e)
                )

        return cy_run

    async def cyeor(
        self, msg: Message | CallbackQuery, text: str, reply: bool = False, **kwargs
    ):
        """
        Edit or Reply to a Message or CallbackQuery

        Arguments:
            msg (Message | CallbackQuery): Message or CallbackQuery to edit or reply to
            text (str): Text to edit or reply with
            reply (bool, optional): Whether to reply to the msg or not. Defaults to False.
        """
        if isinstance(msg, Message):
            if reply:
                await msg.reply(text)
            else:
                await msg.edit(text, **kwargs)
        else:
            if reply:
                await msg.message.reply(text, **kwargs)
            else:
                await msg.message.edit_text(text, **kwargs)

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

    async def full_cleanup(self, path: str = None, user_id: int = None):
        """
        Delete the file/folder and the message
        """
        try:
            # remove from memory. RAM baby!!
            self.glob_tmp.pop(user_id, None)

            # clean up tasks
            if user_id:
                mg_pid = self.mega_running.pop(user_id, None)
                ddl_task = self.ddl_running.pop(user_id, None)
                if mg_pid:
                    await kill_family(mg_pid)
                if ddl_task:
                    ddl_task.cancel()
                    await ddl_task
            
            # clean after task kill
            # sometimes ddl produce unfinished download files and they might not get cleaned up until full_cleanup called again
            # when run_checks gets triggered by the same user
            # not mandatory. would've been better to yield before calling this but thats just more work to do
            if path:
                fs_cleanup(path)
        # no need for anything else
        except asyncio.CancelledError::
            pass
        except Exception as e:
            logging.debug(f"Cleanup error: {e}")

    async def send_files(self, files: list[str], chat_id: int, msg_id: int, **kwargs):
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
                    splout = f"{self.tmp_loc}/{chat_id}/splitted"
                    await splitit(file, splout)
                    for file in listfiles(splout):
                        await send_as_guessed(self, file, chat_id, msg_id, **kwargs)
                    fs_cleanup(splout)
                else:
                    await send_as_guessed(self, file, chat_id, msg_id, **kwargs)
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
