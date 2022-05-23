# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

import shutil

from pyrogram import Client, filters, __version__ as pyrogram_version
from pyrogram.types import Message, CallbackQuery

from megadl.helpers_nexa.mega_help import send_errors
from megadl.data import get_buttons, get_msg
from config import Config


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
            shutil.rmtree(Config.DOWNLOAD_LOCATION + "/" + userpath)
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
    await message.reply_text(
        f"Hi **{message.from_user.first_name}** 😇!, \n\nI'm **@{(await megabot.get_me()).username}**, \nA Simple Mega.nz Downloader Bot with some cool features 😉! \n\nUse Below Buttons to Know More About Me and My Commands 😁 \n\n**Made with ❤️ by @NexaBotsUpdates**",
        reply_markup=await get_buttons("start"))
