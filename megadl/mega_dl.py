# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

import os
import shutil
import filetype
import moviepy.editor
import time
import logging
import subprocess

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from hurry.filesize import size
from functools import partial
from asyncio import get_running_loop
from genericpath import isfile
from posixpath import join
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

# Download Mega Link
def DownloadMegaLink(url, alreadylol, download_msg):
    try:
        m.download_url(url, alreadylol, statusdl_msg=download_msg)
    except Exception as e:
        #await download_msg.edit(f"**Error:** `{e}`")
        print(e)

@Client.on_message(filters.regex(MEGA_REGEX) & filters.private)
async def megadl(_, message: Message):
    # To use bot private or public
    try:
      if Config.IS_PUBLIC_BOT == "False":
        if message.from_user.id not in Config.AUTH_USERS:
          await message.reply_text("**Sorry this bot isn't a Public Bot 🥺! But You can make your own bot ☺️, Click on Below Button!**", reply_markup=GITHUB_REPO)
          return
        if Config.IS_PUBLIC_BOT == "True":
          pass
    except:
      print("Da Fak happend to me?")
      pass
    url = message.text
    userpath = str(message.from_user.id)
    alreadylol = basedir + "/" + userpath
    if not os.path.isdir(alreadylol):
        os.makedirs(alreadylol)
    try:
        download_msg = await message.reply_text("**Starting to Download The Content! This may take while 😴**")
        loop = get_running_loop()
        await loop.run_in_executor(None, partial(DownloadMegaLink, url, alreadylol, download_msg))
        getfiles = [f for f in os.listdir(alreadylol) if isfile(join(alreadylol, f))]
        files = getfiles[0]
        magapylol = f"{alreadylol}/{files}"
        await download_msg.edit("**Successfully Downloaded The Content!**")
    except Exception as e:
        await download_msg.edit(f"**Error:** `{e}`")
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
            await download_msg.edit("**Generating Data...**")
            viddura = moviepy.editor.VideoFileClip(f"{magapylol}")
            vidduration = int(viddura.duration)
            thumbnail_path = f"{alreadylol}/thumbnail.jpg"
            subprocess.call(['ffmpeg', '-i', magapylol, '-ss', '00:00:00.000', '-vframes', '1', thumbnail_path])
            await message.reply_video(magapylol, duration=vidduration, thumb=thumbnail_path, progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", download_msg, start_time))
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
@Client.on_message(~filters.command(["start", "help", "info", "upload", "import"]) & ~filters.regex(MEGA_REGEX) & filters.private & ~filters.media)
async def nomegaurl(_, message: Message):
  # Auth users only
    if message.from_user.id not in Config.AUTH_USERS:
        await message.reply_text("**Sorry this bot isn't a Public Bot 🥺! But You can make your own bot ☺️, Click on Below Button!**", reply_markup=GITHUB_REPO)
        return
    else:
      await message.reply_text("Sorry, I can't find a **valid mega.nz url** in your message! Can you check it again? \n\nAlso Make sure your url **doesn't** contain `mega.co.nz`. \n\n**If there is,** \n - Open that url in a web-browser and wait till webpage loads. \n - Then simply copy url of the webpage that you're in \n - Try Again")
