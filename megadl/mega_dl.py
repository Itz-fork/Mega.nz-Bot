# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

import os
import shutil
import filetype
import moviepy.editor
import time
import logging

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from hurry.filesize import size
from megadl.mega_help import progress_for_pyrogram, humanbytes

from megadl.account import m
from config import Config

# Logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# path we gonna give the download
basedir = Config.DOWNLOAD_LOCATION
# Telegram's max file size
TG_MAX_FILE_SIZE = Config.TG_MAX_SIZE

# Automatic Url Detect (From ImJanindu's AnyDLBot)
MEGA_REGEX = (r"^((?:https?:)?\/\/)"
              r"?((?:www)\.)"
              r"?((?:mega\.nz))"
              r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$")

# Github Repo (Don't remove this)
GITHUB_REPO=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Github Repo", url="https://github.com/Itz-fork/Mega.nz-Bot"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🆘 Support Group 🆘", url="https://t.me/Nexa_bots"
                    )
                ]
            ]
        )


@Client.on_message(filters.regex(MEGA_REGEX) & filters.private)
async def megadl(_, message: Message):
    # Auth users only
    if message.from_user.id not in Config.AUTH_USERS:
        await message.reply_text("**Sorry this bot isn't a Public Bot 🥺! But You can make your own bot ☺️, Click on Below Button!**", reply_markup=GITHUB_REPO)
        return
    url = message.text
    userpath = str(message.from_user.id)
    alreadylol = basedir + "/" + userpath
    if not os.path.isdir(alreadylol):
        megadldir = os.makedirs(alreadylol)
    try:
        download_msg = await message.reply_text("**Starting to Download The Content! This may take while 😴**")
        magapylol = m.download_url(url, megadldir)
        logger = logging.getLogger(magapylol) # Log
        await download_msg.edit("**Successfully Downloaded The Content!**")
    except Exception as e:
        await message.edit(f"**Error:** `{e}`")
        shutil.rmtree(basedir + "/" + userpath)
        return
    lmaocheckdis = os.stat(alreadylol).st_size
    readablefilesize = size(lmaocheckdis) # Convert Bytes into readable size
    if lmaocheckdis > TG_MAX_FILE_SIZE:
        await download_msg.edit(f"**Detected File Size:** `{readablefilesize}` \n**Accepted File Size:** `2GB` \n\nOops! File Size is too large to send in Telegram")
        shutil.rmtree(basedir + "/" + userpath)
        return
    else:
        start_time = time.time()
        guessedfilemime = filetype.guess(f"{magapylol}") # Detecting file type
        if not guessedfilemime.mime:
            await download_msg.edit("**Trying to Upload Now!** \n\n**Error:** `Can't Get File Mime Type! Sending as a Document!`")
            await message.reply_document(magapylol, progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", download_msg, start_time))
            await download_msg.edit(f"**Successfully Uploaded** \n\n**Join @NexaBotsUpdates If You're Enjoying This Bot**")
            shutil.rmtree(basedir + "/" + userpath)
            print(e)
            return
        filemimespotted = guessedfilemime.mime
        # Checking If it's a gif
        if "image/gif" in filemimespotted:
            await download_msg.edit("**Trying to Upload Now!**")
            await message.reply_animation(magapylol, progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", download_msg, start_time))
            await download_msg.edit(f"**Successfully Uploaded** \n\n**Join @NexaBotsUpdates If You're Enjoying This Bot**")
            shutil.rmtree(basedir + "/" + userpath)
            return
        # Checking if it's a image
        if "image" in filemimespotted:
            await download_msg.edit("**Trying to Upload Now!**")
            await message.reply_photo(magapylol, progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", download_msg, start_time))
            await download_msg.edit(f"**Successfully Uploaded** \n\n**Join @NexaBotsUpdates If You're Enjoying This Bot**")
        # Checking if it's a video
        elif "video" in filemimespotted:
            viddura = moviepy.editor.VideoFileClip(f"{magapylol}")
            vidduration = int(viddura.duration)
            if "!streamable" in url:
                await message.reply_video(magapylol, duration=vidduration, progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", download_msg, start_time))
                await download_msg.edit(f"**Successfully Uploaded** \n\n**Join @NexaBotsUpdates If You're Enjoying This Bot**")
            else:
                await message.reply_document(magapylol, progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", download_msg, start_time))
                await download_msg.edit(f"**Successfully Uploaded** \n\n**Join @NexaBotsUpdates If You're Enjoying This Bot**")
        # Checking if it's a audio
        elif "audio" in filemimespotted:
            await download_msg.edit("**Trying to Upload Now!**")
            await message.reply_audio(magapylol, progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", download_msg, start_time))
            await download_msg.edit(f"**Successfully Uploaded** \n\n**Join @NexaBotsUpdates If You're Enjoying This Bot**")
        # If it's not a image/video or audio it'll reply it as doc
        else:
            await download_msg.edit("**Trying to Upload Now!**")
            await message.reply_document(magapylol, progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", download_msg, start_time))
            await download_msg.edit(f"**Successfully Uploaded** \n\n**Join @NexaBotsUpdates If You're Enjoying This Bot**")
    try:
        shutil.rmtree(basedir + "/" + userpath)
        print("Successfully Removed Downloaded File and the folder!")
    except Exception as e:
        print(e)
        return


# Replying If There is no mega url in the message
@Client.on_message(~filters.regex(MEGA_REGEX) & filters.private)
async def nomegaurl(_, message: Message):
  # Auth users only
    if message.from_user.id not in Config.AUTH_USERS:
        await message.reply_text("**Sorry this bot isn't a Public Bot 🥺! But You can make your own bot ☺️, Click on Below Button!**", reply_markup=GITHUB_REPO)
        return
    else:
      await message.reply_text("**Sorry, I can't find a valid mega.nz url in your message! Can you check it again?")
      return
