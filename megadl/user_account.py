# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae
# This plugin is working only if you Login with Mega Account

import json

from pyrogram import Client, filters
from pyrogram.types import Message
from hurry.filesize import size

from megadl.account import m
from megadl.mega_dl import GITHUB_REPO
from config import Config

# Get Mega user Account info
@Client.on_message(filters.command("info") & filters.private)
async def nomegaurl(_, message: Message):
  if message.from_user.id not in Config.AUTH_USERS:
    await message.reply_text("**Sorry this bot isn't a Public Bot 🥺! But You can make your own bot ☺️, Click on Below Button!**", reply_markup=GITHUB_REPO)
    return
  if Config.USER_ACCOUNT == "False":
    await message.reply_text("You didn't setup a Mega.nz Account to Get details!")
    return
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
  await message.reply_text(f"**~ Your User Account Info ~** \n\n▪ **Account Name:** `{acc_name}` \n▪ **Email:** `{acc_email}` \n▪ **Storage,** \n - **Total:** `{total_space}` \n - **Used:** `{used_space}` \n - **Free:** `{free_space}` \n▪ **Quota:** `{acc_quota} MB`")
