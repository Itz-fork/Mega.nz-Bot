# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import __version__ as pyrogram_version

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
                        "Mega.nz Downloader 📥", callback_data="meganzdownloadercb"
                    ),
                    InlineKeyboardButton(
                        "Mega.nz Uploader 📤", callback_data="meganzuploadercb"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Mega.nz Importer 📲", callback_data="meganzimportercb"
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
                        "Back ⬅️", callback_data="helpcallback"
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
  if query.data == "helpcallback":
    await query.edit_message_text(f"**Here is the Help Menu Of @{(await megabot.get_me()).username}** \n\nUse Below Buttons to Get Help Menu of That Module 😊", reply_markup=HELP_BUTTONS)
  
  elif query.data == "meganzdownloadercb":
    user_id = query.from_user.id
    if Config.IS_PUBLIC_BOT == "False":
      if user_id not in Config.AUTH_USERS:
        await query.answer("Sorry This Bot is a Private Bot 😔! \n\nJoin @NexaBotsUpdates to Make your own bot!", show_alert=True)
        return
      else:
        pass
    await query.edit_message_text("**Here is The Help Of Mega.nz Downloader Module** \n\n\n  ✗ Send Me a Mega.nz File Link. (Size Must be Under 2GB due to Telegram API Limitations. Folder Not Supported) \n\n  ✗ Wait Till It Download and Upload That File to Telegram \n\n**Made with ❤️ by @NexaBotsUpdates**", reply_markup=MODULES_HELP)
  
  elif query.data == "meganzuploadercb":
    user_id = query.from_user.id
    if Config.IS_PUBLIC_BOT == "False":
      if user_id not in Config.AUTH_USERS:
        await query.answer("Sorry This Bot is a Private Bot 😔! \n\nJoin @NexaBotsUpdates to Make your own bot!", show_alert=True)
        return
      else:
        pass
    await query.edit_message_text("**Here is The Help Of Mega.nz Uploader Module** \n\n\n  ✗ First Send or Forward a File to Me. \n\n  ✗ Then Reply to that file with `/upload` command \n\n  ✗ Wait till It Download and Upload That File to Mega.nz \n\n**Made with ❤️ by @NexaBotsUpdates**", reply_markup=MODULES_HELP)
  
  elif query.data == "meganzimportercb":
    user_id = query.from_user.id
    if Config.IS_PUBLIC_BOT == "False":
      if user_id not in Config.AUTH_USERS:
        await query.answer("Sorry This Bot is a Private Bot 😔! \n\nJoin @NexaBotsUpdates to Make your own bot!", show_alert=True)
        return
      else:
        pass
    await query.edit_message_text("**Here is The Help Of Mega.nz Url Importer Module** \n\n\n  ✗ Send or Reply to a Public Mega.nz url with `/import` Command (**Usage:** `/import your_mega_link`) \n\n   ✗ Wait till It Finish \n\n**Made with ❤️ by @NexaBotsUpdates**", reply_markup=MODULES_HELP)
  
  elif query.data == "aboutcallback":
    await query.edit_message_text(f"**About Mega.nz Bot** \n\n\n  ✗ **Username:** @{(await megabot.get_me()).username} \n\n  ✗ **Language:** [Python](https://www.python.org/) \n\n  ✗ **Library:** [Pyrogram](https://docs.pyrogram.org/) \n\n  ✗ **Pyrogram Version:** `{pyrogram_version}` \n\n  ✗ **Source Code:** [Mega.nz-Bot](https://github.com/Itz-fork/Mega.nz-Bot) \n\n  ✗ **Developer:** [Itz-fork](https://github.com/Itz-fork) \n\n**Made with ❤️ by @NexaBotsUpdates**", reply_markup=ABUT_BUTTONS)
  
  elif query.data == "closeqcb":
    await query.answer(f"Closed Help Menu of @{(await megabot.get_me()).username}")
    await query.message.delete()

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
  await message.reply_text(f"Hi **{message.from_user.first_name}** 😇!, \n\nI'm **@{(await megabot.get_me()).username}**, \nA Simple Mega.nz Downloader Bot 😉! \n\nUse Below Buttons to Know More About Me and My Commands 😁 \n\n**Made with ❤️ by @NexaBotsUpdates**", reply_markup=START_MSGA_B)
                                  
