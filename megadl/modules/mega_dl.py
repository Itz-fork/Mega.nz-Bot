# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

import os
import re
import shutil

from pyrogram import Client, filters
from pyrogram.types import Message
from filesplit.split import Split
from functools import partial
from asyncio import get_running_loop

from megadl.data import get_buttons
from megadl.helpers_nexa.account import m
from megadl.helpers_nexa.decorators import is_public
from megadl.helpers_nexa.mega_help import send_errors, send_logs
from megadl.helpers_nexa.up_helper import guess_and_send
from megadl.helpers_nexa.megatools import MegaTools
from config import Config


# Automatic Url Detect (From stackoverflow. Can't find link lol)
MEGA_REGEX = "https?:\/\/mega\.nz\/(?:[^\/\s]+\/)+"


# Function to download Mega Link
def DownloadMegaLink(url, alreadylol, download_msg):
    try:
        m.download_url(url, alreadylol, statusdl_msg=download_msg)
    except Exception as e:
        send_errors(e)


# Function to split large files
def split_files(input_file, out_path):
    split = Split(input_file, out_path)
    split.bysize(2040108421)


# Uses mega.py package
@Client.on_message(filters.regex(MEGA_REGEX) & filters.command("megapy") & filters.private)
@is_public
async def megadl_megapy(_, message: Message):
    url = message.text.split(None, 1)[1]
    userpath = str(message.from_user.id)
    the_chat_id = str(message.chat.id)
    megadl_path = Config.DOWNLOAD_LOCATION + "/" + userpath
    # Temp fix for the https://github.com/Itz-fork/Mega.nz-Bot/issues/11
    if os.path.isdir(megadl_path):
        return await message.reply_text("`Already One Process is Going On. Please wait until it's finished!`")
    else:
        os.makedirs(megadl_path)
    try:
        download_msg = await message.reply_text("**Starting to Download The Content! This may take while 😴**", reply_markup=await get_buttons("cancel"))
        await send_logs(user_id=userpath, mchat_id=the_chat_id, mega_url=url, download_logs=True)
        loop = get_running_loop()
        await loop.run_in_executor(None, partial(DownloadMegaLink, url, megadl_path, download_msg))
        folder_f = [val for sublist in [[os.path.join(
            i[0], j) for j in i[2]] for i in os.walk(megadl_path)] for val in sublist]
        await download_msg.edit("**Successfully Downloaded The Content!**")
    except Exception as e:
        if os.path.isdir(megadl_path):
            await download_msg.edit(f"**Error:** `{e}`")
            shutil.rmtree(Config.DOWNLOAD_LOCATION + "/" + userpath)
            await send_errors(e)
        return

    if os.path.isdir(megadl_path) is False:
        return

    try:
        for mg_file in folder_f:
            file_size = os.stat(mg_file).st_size
            if file_size > Config.TG_MAX_SIZE:
                base_splt_out_dir = megadl_path + "splitted_files"
                await download_msg.edit("`Large File Detected, Trying to split it!`")
                loop = get_running_loop()
                await loop.run_in_executor(None, partial(split_files(mg_file, base_splt_out_dir)))
                split_out_dir = [val for sublist in [[os.path.join(
                    i[0], j) for j in i[2]] for i in os.walk(megadl_path)] for val in sublist]
                for spl_f in split_out_dir:
                    await guess_and_send(spl_f, int(the_chat_id), "cache", download_msg)
            else:
                await guess_and_send(mg_file, int(the_chat_id), "cache", download_msg)
    except Exception as e:
        await download_msg.edit(f"**Error:** \n`{e}`")
        await send_errors(e)
    try:
        shutil.rmtree(Config.DOWNLOAD_LOCATION + "/" + userpath)
        print("Successfully Removed Downloaded File and the folder!")
    except Exception as e:
        return await send_errors(e)


# Uses megatools cli
@Client.on_message(filters.regex(MEGA_REGEX) & filters.private & ~filters.command("megapy"))
@is_public
async def megadl_megatools(_, message: Message):
    url = message.text
    if not re.match(MEGA_REGEX, url):
        return await message.reply("`This isn't a mega url!`")
    userpath = str(message.from_user.id)
    the_chat_id = str(message.chat.id)
    megadl_path = Config.DOWNLOAD_LOCATION + "/" + userpath
    # Temp fix for the https://github.com/Itz-fork/Mega.nz-Bot/issues/11
    if os.path.isdir(megadl_path):
        return await message.reply_text("`Already One Process is Going On. Please wait until it's finished!`")
    else:
        os.makedirs(megadl_path)
    try:
        download_msg = await message.reply_text("**Starting to Download The Content! This may take while 😴** \n\n`Note: You can't cancel this!`")
        await send_logs(user_id=userpath, mchat_id=the_chat_id, mega_url=url, download_logs=True)
        mcli = MegaTools()
        dl_files = await mcli.download(url, download_msg.chat.id, download_msg.id, megadl_path)
        await download_msg.edit("**Successfully Downloaded The Content!**")
    except Exception as e:
        if os.path.isdir(megadl_path):
            await download_msg.edit(f"**Error:** `{e}`")
            shutil.rmtree(Config.DOWNLOAD_LOCATION + "/" + userpath)
            await send_errors(e)
        return
    try:
        for mg_file in dl_files:
            file_size = os.stat(mg_file).st_size
            if file_size > Config.TG_MAX_SIZE:
                base_splt_out_dir = megadl_path + "splitted_files"
                await download_msg.edit("`Large file detected, Trying to split!`")
                loop = get_running_loop()
                await loop.run_in_executor(None, partial(split_files(mg_file, base_splt_out_dir)))
                split_out_dir = [val for sublist in [[os.path.join(
                    i[0], j) for j in i[2]] for i in os.walk(megadl_path)] for val in sublist]
                for spl_f in split_out_dir:
                    await guess_and_send(spl_f, int(the_chat_id), download_msg)
            else:
                await guess_and_send(mg_file, int(the_chat_id), download_msg)
        await download_msg.edit("**Successfully Uploaded The Content!**")
    except Exception as e:
        await download_msg.edit(f"**Error:** \n`{e}`")
        await send_errors(e)
    try:
        shutil.rmtree(Config.DOWNLOAD_LOCATION + "/" + userpath)
        print("Successfully Removed Downloaded File and the folder!")
    except Exception as e:
        await send_errors(e)


# Replying If There is no mega url in the message
@Client.on_message(~filters.command(["start", "help", "info", "upload", "import", "megapy"]) & ~filters.regex(MEGA_REGEX) & filters.private & ~filters.media)
@is_public
async def nomegaurl(_, message: Message):
    await message.reply_text("Sorry, I can't find a **valid mega.nz url** in your message! Can you check it again? \n\nAlso Make sure your url **doesn't** contain `mega.co.nz`. \n\n**If there is,** \n - Open that url in a web-browser and wait till webpage loads. \n - Then simply copy url of the webpage that you're in \n - Try Again")
