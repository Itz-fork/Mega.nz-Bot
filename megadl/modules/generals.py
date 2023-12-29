# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: General commands of the bot


from pyrogram import filters
from pyrogram.types import Message

from megadl import MegaCypher


@MegaCypher.on_message(filters.command("start"))
@MegaCypher.run_checks
async def start_msg(_: MegaCypher, msg: Message):
    await msg.reply_text(
        f"""
Hi `{msg.from_user.first_name}` 👋, I'm [Mega.nz-Bot](https://github.com/Itz-fork/Mega.nz-Bot)!

I can help you download, upload files or folders from telegram.
Not sure what to do? Check /help for more info 😇


**Made with ❤️ by @NexaBotsUpdates**
    """,
        disable_web_page_preview=True,
    )


@MegaCypher.on_message(filters.command("help"))
@MegaCypher.run_checks
async def help_msg(_: MegaCypher, msg: Message):
    await msg.reply_text(
        f"""
**How do I login?**
  Send /login command and enter your details when I ask you. Don't worry we encrypt your data before sending it anywhere 🤗

**How to download from mega link?**
  It's very easy. Just send the link you want to download and I'll download it for you 😉

**How to upload files to Mega.nz?**
  Just send me the files and I'll ask you whether you want to upload it or not. Same goes for direct download links 😎


  
**Made with ❤️ by @NexaBotsUpdates**
      """
    )
