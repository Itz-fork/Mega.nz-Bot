# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

from pyrogram import Client, filters
from pyrogram.types import Message

from megadl.account import m

@Client.on_message(filters.command("info") & filters.private)
async def nomegaurl(_, message: Message):
  info = m.get_user()
  await message.reply_text(info)
