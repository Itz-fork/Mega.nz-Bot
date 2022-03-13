# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

import shutil

from pyrogram import Client, filters, __version__ as pyrogram_version
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from .mega_dl import basedir
from megadl.helpers_nexa.mega_help import send_errors
from config import Config


# Start Message Callback buttons
Buttons = {
    "start": [
        [InlineKeyboardButton("Help 📜", callback_data="helpcallback"),
         InlineKeyboardButton("About ⁉️", callback_data="aboutcallback")],

        [InlineKeyboardButton(
            "Go Inline", switch_inline_query_current_chat="")]
    ],

    "inline": [
        [InlineKeyboardButton("Commands Help �", callback_data="helpcallback"),
         InlineKeyboardButton("Inline Query Help �", callback_data="inlinehelpcallback")],

        [InlineKeyboardButton(
            "Go Inline", switch_inline_query_current_chat="")]
    ],

    "help": [
        [InlineKeyboardButton("Downloader 📥", callback_data="meganzdownloadercb"),
         InlineKeyboardButton("Uploader 📤", callback_data="meganzuploadercb")],

        [InlineKeyboardButton(
            "Importer 📲", callback_data="meganzimportercb")],
        [InlineKeyboardButton(
            "Back ⬅️", callback_data="startcallback")]
    ],

    "inline_help": [
        [InlineKeyboardButton("Get File Details 📖", callback_data="getfiledetailscb"),
         InlineKeyboardButton("Get Account Info 💳", callback_data="getaccoutinfo")]
    ],

    "mod_help": [
                [InlineKeyboardButton("Close ❌", callback_data="closeqcb")],

                [InlineKeyboardButton("Back ⬅️", callback_data="helpcallback")]
    ],

    "imod_help": [
        [InlineKeyboardButton("Close ❌", callback_data="closeqcb")],

        [InlineKeyboardButton(
            "Back ⬅️", callback_data="inlinehelpcallback")]
    ],

    "about": [
        [InlineKeyboardButton(
            "Source Code 🗂", url="https://github.com/Itz-fork/Mega.nz-Bot")],

        [InlineKeyboardButton("Back ⬅️", callback_data="startcallback"),
         InlineKeyboardButton("Close ❌", callback_data="closeqcb")]
    ]
}

async def get_buttons(name):
    return InlineKeyboardMarkup(Buttons.get(name))


# Help messages
Messages = {
    "dl": """
**Here is The Help Of Mega.nz Downloader Module**


  ✘ Send me a Mega.nz file/folder link. (Use `/megadl` command if you're using folder links)

  ✘ Wait Till It Download and Upload to Telegram.


**Made with ❤️ by @NexaBotsUpdates**    
""",

    "up": """
**Here is The Help Of Mega.nz Uploader Module**


  ✘ First Send or Forward a File to Me. You can also send me a direct link.

  ✘ Then Reply to that file with `/upload` command.

  ✘ Wait till It Download and Upload to Mega.nz
  

**Made with ❤️ by @NexaBotsUpdates**
""",

    "import": """
"**Here is The Help Of Mega.nz Url Importer Module**


  ✘ Send or Reply to a Public Mega.nz url with `/import` Command (**Usage:** `/import your_mega_link`)
  
  ✘ Wait till It Finish


**Made with ❤️ by @NexaBotsUpdates**    
""",

    "file_info": """
**Here is The Help Of Get File Info Via Inline Module**


  ✘ Go to any chat

  ✘ Type: `{uname} details` and after that give a one space and paste your mega.nz link (**Usage:** `{uname} details your_mega_link`)


**Made with ❤️ by @NexaBotsUpdates**
""",

    "acc_info": """
**Here is The Help Of Get Account Info Via Inline Module**


  ✘ Go to any chat (This will send your mega.nz account data so better do this in a private chat)
  
  ✘ Type: `{uname} info` (**Usage:** `{uname} info`)


**Made with ❤️ by @NexaBotsUpdates**
"""
}

async def get_msg(name):
    return Messages.get(name)


# Callbacks
@Client.on_callback_query()
async def meganz_cb(megabot: Client, query: CallbackQuery):
    if query.data == "startcallback":
        await query.edit_message_text(f"Hi **{query.from_user.first_name}** 😇!, \n\nI'm **@{(await megabot.get_me()).username}**, \nA Simple Mega.nz Downloader Bot 😉! \n\nUse Below Buttons to Know More About Me and My Commands 😁 \n\n**Made with ❤️ by @NexaBotsUpdates**", reply_markup=await get_buttons("start"))

    elif query.data == "helpcallback":
        await query.edit_message_text(f"**Here is the Commands Help Menu Of @{(await megabot.get_me()).username}** \n\nUse Below Buttons to Get Help Menu of That Module 😊", reply_markup=await get_buttons("help"))

    elif query.data == "meganzdownloadercb":
        user_id = query.from_user.id
        if not Config.IS_PUBLIC_BOT:
            if user_id not in Config.AUTH_USERS:
                return await query.answer("Sorry This Bot is a Private Bot 😔! \n\nJoin @NexaBotsUpdates to Make your own bot!", show_alert=True)
        await query.edit_message_text(await get_msg("dl"), reply_markup=await get_buttons("mod_help"))

    elif query.data == "meganzuploadercb":
        user_id = query.from_user.id
        if not Config.IS_PUBLIC_BOT:
            if user_id not in Config.AUTH_USERS:
                return await query.answer("Sorry This Bot is a Private Bot 😔! \n\nJoin @NexaBotsUpdates to Make your own bot!", show_alert=True)
        await query.edit_message_text(await get_msg("up"), reply_markup=await get_buttons("mod_help"))

    elif query.data == "meganzimportercb":
        user_id = query.from_user.id
        if not Config.IS_PUBLIC_BOT:
            if user_id not in Config.AUTH_USERS:
                return await query.answer("Sorry This Bot is a Private Bot 😔! \n\nJoin @NexaBotsUpdates to Make your own bot!", show_alert=True)
        await query.edit_message_text(await get_msg("import"), reply_markup=await get_buttons("mod_help"))

    elif query.data == "aboutcallback":
        await query.edit_message_text(f"**About Mega.nz Bot** \n\n\n  ✘ **Username:** @{(await megabot.get_me()).username} \n\n  ✘ **Language:** [Python](https://www.python.org/) \n\n  ✘ **Library:** [Pyrogram](https://docs.pyrogram.org/) \n\n  ✘ **Pyrogram Version:** `{pyrogram_version}` \n\n  ✘ **Source Code:** [Mega.nz-Bot](https://github.com/Itz-fork/Mega.nz-Bot) \n\n  ✘ **Developer:** [Itz-fork](https://github.com/Itz-fork) \n\n**Made with ❤️ by @NexaBotsUpdates**", reply_markup=await get_buttons("about"), disable_web_page_preview=True)

    elif query.data == "inlinehelpcallback":
        await query.edit_message_text(f"**Here is the Commands Help Menu Of @{(await megabot.get_me()).username}** \n\nUse Below Buttons to Get Help Menu of That Module 😊", reply_markup=await get_buttons("inline_help"))

    elif query.data == "getfiledetailscb":
        await query.edit_message_text((await get_msg("file_info")).format(uname=(await megabot.get_me()).username), reply_markup=await get_buttons("imod_help"))

    elif query.data == "getaccoutinfo":
        await query.edit_message_text((await get_msg("acc_info")).format(uname=(await megabot.get_me()).username), reply_markup=await get_buttons("imod_help"))

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
    await message.reply_text(f"Hi **{message.from_user.first_name}** 😇!, \n\nI'm **@{(await megabot.get_me()).username}**, \nA Simple Mega.nz Downloader Bot with some cool features 😉! \n\nUse Below Buttons to Know More About Me and My Commands 😁 \n\n**Made with ❤️ by @NexaBotsUpdates**", reply_markup=await get_buttons("start"))
