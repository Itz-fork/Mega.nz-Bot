# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae
# This plugin is working only if you Login with Mega Account

import json
import os
import time

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from hurry.filesize import size
from functools import partial
from asyncio import get_running_loop
from genericpath import isfile
from posixpath import join

from megadl.account import m
from megadl.mega_dl import GITHUB_REPO
from config import Config
from megadl.mega_help import progress_for_pyrogram, humanbytes

# Get Mega user Account info
@Client.on_message(filters.command("info") & filters.private)
async def accinfo(_, message: Message):
  if message.from_user.id not in Config.AUTH_USERS:
    await message.reply_text("**Sorry this bot isn't a Public Bot 🥺! But You can make your own bot ☺️, Click on Below Button!**", reply_markup=GITHUB_REPO)
    return
  if Config.USER_ACCOUNT == "False":
    await message.reply_text("`You didn't setup a Mega.nz Account to Get details!`")
    return
  acc_info_msg = await message.reply_text("`Processing ⚙️...`")
  get_user = m.get_user()
  imported_user = json.dumps(get_user)
  uacc_info = json.loads(imported_user)
  acc_email = uacc_info['email']
  acc_name = uacc_info['name']
  acc_quota = m.get_quota()
  js_acc_space = m.get_storage_space()
  acc_space_f = json.dumps(js_acc_space)
  acc_space = json.loads(acc_space_f)
  btotal_space = acc_space['total']
  bused_space = acc_space['used']
  bfree_space = btotal_space - bused_space
  total_space = size(btotal_space)
  used_space = size(bused_space)
  free_space = size(bfree_space)
  await acc_info_msg.edit(f"**~ Your User Account Info ~** \n\n✦ **Account Name:** `{acc_name}` \n✦ **Email:** `{acc_email}` \n✦ **Storage,** \n       - **Total:** `{total_space}` \n       - **Used:** `{used_space}` \n       - **Free:** `{free_space}` \n✦ **Quota:** `{acc_quota} MB`")


# uplaod files
def UploadToMega(toupload, megaupmsg):
  try:
    uploadfile = m.upload(f"{toupload}", upstatusmsg=megaupmsg)
    flink = m.get_upload_link(uploadfile)
    return flink
  except Exception as e:
    print(e)
    return

@Client.on_message(filters.command("upload") & filters.private)
async def uptomega(client: Client, message: Message):
  if message.from_user.id not in Config.AUTH_USERS:
    await message.reply_text("**Sorry this bot isn't a Public Bot 🥺! But You can make your own bot ☺️, Click on Below Button!**", reply_markup=GITHUB_REPO)
    return
  if Config.USER_ACCOUNT == "False":
    await message.reply_text("`You didn't setup a Mega.nz Account to Get details!`")
    return
  todownfile = message.reply_to_message
  if not todownfile:
    await message.reply_text("**Please reply to a Media File to Upload!**")
    return
  if todownfile.media is None:
    await message.reply_text("Sorry, I can't Upload Text to Mega! Please reply to a Media File!")
    return
  try:
    start_time = time.time()
    megaupmsg = await message.reply_text("**Starting to Download The Content to My Server! This may take while 😴**")
    toupload = await client.download_media(message=todownfile, progress=progress_for_pyrogram, progress_args=("**Trying to Download!** \n", megaupmsg, start_time))
    await megaupmsg.edit("**Successfully Downloaded the File!**")
    await megaupmsg.edit("**Trying to Upload to Mega.nz! This may take while 😴****")
    loop = get_running_loop()
    await loop.run_in_executor(None, partial(UploadToMega, toupload, megaupmsg))
    link = flink
    await megaupmsg.edit(f"**Successfully Uploaded To Mega.nz** \n\n**Link:** `{link}` \n\n**Powered by @NexaBotsUpdates**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📥 Mega.nz Link 📥", url=f"{link}")]]))
    os.remove(toupload)
  except Exception as e:
    await megaupmsg.edit(f"**Error:** `{e}`")
    try:
      os.remove(toupload)
    except Exception as e:
      print(f"Why this file is gae? \nError: {e}")


# Import files from a public url
@Client.on_message(filters.command("import") & filters.private)
async def importurlf(_, message: Message):
  if message.from_user.id not in Config.AUTH_USERS:
    await message.reply_text("**Sorry this bot isn't a Public Bot 🥺! But You can make your own bot ☺️, Click on Below Button!**", reply_markup=GITHUB_REPO)
    return
  if Config.USER_ACCOUNT == "False":
    await message.reply_text("You didn't setup a Mega.nz Account to Get details!")
    return
  importing_msg = await message.reply_text("`Processing ⚙️...`")
  reply_msg = message.reply_to_message
  try:
    if reply_msg:
      replied_txt_msg = reply_msg.text
      if "mega.nz" not in replied_txt_msg:
        await importing_msg.edit("Send me a **Valid Mega.nz** Link to Import 😏!")
        return
      else:
        msg_text = replied_txt_msg
    else:
      msg_txt_url = message.text
      if "mega.nz" not in msg_txt_url:
        await importing_msg.edit("Send me a **Valid Mega.nz** Link to Import 😏!")
        return
      else:
        msg_text = msg_txt_url
  except Exception as e:
    await importing_msg.edit("Hmmm... Looks like there is something other than text! Mind if check it again 🤔?")
    print(e)
    return
  else:
    try:
      import_file = m.import_public_url(msg_text)
      imported_link = m.get_upload_link(import_file)
      await importing_msg.delete()
      await message.reply_text(f"**Successfully Imported 😌** \n\n**Link:** `{imported_link}` \n\n**Powered by @NexaBotsUpdates**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📥 Imported Link 📥", url=f"{imported_link}")]]))
    except Exception as e:
      await message.reply_text(f"**Error:** `{e}`")


# Start message
@Client.on_message(filters.command("start"))
async def startcmd(megabot: Client, message: Message):
  # To use bot private or public
  try:
    if Config.IS_PUBLIC_BOT == "False":
      if message.from_user.id not in Config.AUTH_USERS:
        await message.reply_text("**Sorry this bot isn't a Public Bot 🥺! But You can make your own bot ☺️, Click on Below Button!**", reply_markup=GITHUB_REPO)
        return
    elif Config.IS_PUBLIC_BOT == "True":
      pass
  except:
    print("Da Fak happend to me?")
    return
  await message.reply_text(f"Hello, Nice to Meet You **{message.from_user.first_name}** 😇!, \n\nI'm **@{(await megabot.get_me()).username}**, \nMega.nz Url Uploader 😉! \n\nIf You don't Know how to work with me hit on /help command 😁")

# Help command
@Client.on_message(filters.command("help"))
async def helpcmd(megabot: Client, message: Message):
  # To use bot private or public
  try:
    if Config.IS_PUBLIC_BOT == "False":
      if message.from_user.id not in Config.AUTH_USERS:
        await message.reply_text("**Sorry this bot isn't a Public Bot 🥺! But You can make your own bot ☺️, Click on Below Button!**", reply_markup=GITHUB_REPO)
        return
    elif Config.IS_PUBLIC_BOT == "True":
      pass
  except:
    print("Da Fak happend to me?")
    return
  await message.reply_text(f"Hi **{message.from_user.first_name}** 😇!, \n\n\n**📥 Download Mega.nz Links** \n - Just send me a valid Mega.nz Link. (Folder Not Supported) \n\n**📤 Upload to Mega.nz** \n - First Send or Forward a File to Me. \n - Then Reply to that file with `/upload` command \n\n**🖇️ Import Public Mega,nz Files** \n - Send or reply to a mega.nz url with `/import` command (**Usage:** `/import your_mega_link`) \n\n**Powered by @NexaBotsUpdates**")
