# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

import shutil

from pyrogram import Client, filters, __version__ as pyrogram_version
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from .mega_dl import basedir
from megadl.helpers_nexa.mega_help import send_errors
from config import Config

# Start Message Callback buttons
START_MSGA_B=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Help 📜", callback_data="helpcallback"
                    ),
                    InlineKeyboardButton(
                        "About ⁉️", callback_data="aboutcallback"
                    )
                ]
            ]
        )

# Help Menu Callback buttons
HELP_BUTTONS=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Downloader 📥", callback_data="meganzdownloadercb"
                    ),
                    InlineKeyboardButton(
                        "Uploader 📤", callback_data="meganzuploadercb"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Importer 📲", callback_data="meganzimportercb"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Back ⬅️", callback_data="startcallback"
                    )
                ]
            ]
        )

# Module Help Callbacks
MODULES_HELP=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Close ❌", callback_data="closeqcb"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Back ⬅️", callback_data="helpcallback"
                    )
                ]
            ]
        )

# About Callbacks
ABUT_BUTTONS=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Source Code 🗂", url="https://github.com/Itz-fork/Mega.nz-Bot"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Back ⬅️", callback_data="startcallback"
                    ),
                    InlineKeyboardButton(
                        "Close ❌", callback_data="closeqcb"
                    )
                ]
            ]
        )


# Callbacks
@Client.on_callback_query()
async def meganz_cb(megabot: Client, query: CallbackQuery):
  if query.data == "startcallback":
    await query.edit_message_text(f"Hi **{query.from_user.first_name}** 😇!, \n\nI'm **@{(await megabot.get_me()).username}**, \nA Simple Mega.nz Downloader Bot 😉! \n\nUse Below Buttons to Know More About Me and My Commands 😁 \n\n**Made with ❤️ by @NexaBotsUpdates**", reply_markup=START_MSGA_B)

  elif query.data == "helpcallback":
    await query.edit_message_text(f"**Here is the Help Menu Of @{(await megabot.get_me()).username}** \n\nUse Below Buttons to Get Help Menu of That Module 😊", reply_markup=HELP_BUTTONS)
  
  elif query.data == "meganzdownloadercb":
    user_id = query.from_user.id
    if Config.IS_PUBLIC_BOT == "False":
      if user_id not in Config.AUTH_USERS:
        await query.answer("Sorry This Bot is a Private Bot 😔! \n\nJoin @NexaBotsUpdates to Make your own bot!", show_alert=True)
        return
      else:
        pass
    await query.edit_message_text("**Here is The Help Of Mega.nz Downloader Module** \n\n\n  ✘ Send Me a Mega.nz File Link. (Size Must be Under 2GB due to Telegram API Limitations. Folder Not Supported) \n\n  ✘ Wait Till It Download and Upload That File to Telegram \n\n**Made with ❤️ by @NexaBotsUpdates**", reply_markup=MODULES_HELP)
  
  elif query.data == "meganzuploadercb":
    user_id = query.from_user.id
    if Config.IS_PUBLIC_BOT == "False":
      if user_id not in Config.AUTH_USERS:
        await query.answer("Sorry This Bot is a Private Bot 😔! \n\nJoin @NexaBotsUpdates to Make your own bot!", show_alert=True)
        return
      else:
        pass
    await query.edit_message_text("**Here is The Help Of Mega.nz Uploader Module** \n\n\n  ✘ First Send or Forward a File to Me. \n\n  ✘ Then Reply to that file with `/upload` command \n\n  ✘ Wait till It Download and Upload That File to Mega.nz \n\n**Made with ❤️ by @NexaBotsUpdates**", reply_markup=MODULES_HELP)
  
  elif query.data == "meganzimportercb":
    user_id = query.from_user.id
    if Config.IS_PUBLIC_BOT == "False":
      if user_id not in Config.AUTH_USERS:
        await query.answer("Sorry This Bot is a Private Bot 😔! \n\nJoin @NexaBotsUpdates to Make your own bot!", show_alert=True)
        return
      else:
        pass
    await query.edit_message_text("**Here is The Help Of Mega.nz Url Importer Module** \n\n\n  ✘ Send or Reply to a Public Mega.nz url with `/import` Command (**Usage:** `/import your_mega_link`) \n\n   ✘ Wait till It Finish \n\n**Made with ❤️ by @NexaBotsUpdates**", reply_markup=MODULES_HELP)
  
  elif query.data == "aboutcallback":
    await query.edit_message_text(f"**About Mega.nz Bot** \n\n\n  ✘ **Username:** @{(await megabot.get_me()).username} \n\n  ✘ **Language:** [Python](https://www.python.org/) \n\n  ✘ **Library:** [Pyrogram](https://docs.pyrogram.org/) \n\n  ✘ **Pyrogram Version:** `{pyrogram_version}` \n\n  ✘ **Source Code:** [Mega.nz-Bot](https://github.com/Itz-fork/Mega.nz-Bot) \n\n  ✘ **Developer:** [Itz-fork](https://github.com/Itz-fork) \n\n**Made with ❤️ by @NexaBotsUpdates**", reply_markup=ABUT_BUTTONS, disable_web_page_preview=True)

  elif query.data == "cancelvro":
    userpath = str(query.from_user.id)
    try:
        shutil.rmtree(basedir + "/" + userpath)
        await query.message.delete()
        await query.message.reply_text("`Process Cancelled by User`")
    except Exception as e:
        await send_errors(e)

  elif query.data == "closeqcb":
    try:
      await query.message.delete()
      await query.answer(f"Closed Help Menu of @{(await megabot.get_me()).username}")
    except:
      await query.answer(f"Can't Close Via Inline Messages!")

# Start message
@Client.on_message(filters.command("start"))
async def startcmd(megabot: Client, message: Message):
  await message.reply_text(f"Hi **{message.from_user.first_name}** 😇!, \n\nI'm **@{(await megabot.get_me()).username}**, \nA Simple Mega.nz Downloader Bot with some cool features 😉! \n\nUse Below Buttons to Know More About Me and My Commands 😁 \n\n**Made with ❤️ by @NexaBotsUpdates**", reply_markup=START_MSGA_B)