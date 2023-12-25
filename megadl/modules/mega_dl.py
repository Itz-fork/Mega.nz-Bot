# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Responsible for download function


from os import path, makedirs

from pyrogram import filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from megadl import MeganzClient, GLOB_TMP
from megadl.lib.megatools import MegaTools
from megadl.helpers.files import cleanup


@MeganzClient.on_message(
    filters.regex(r"(https?:\/\/mega\.nz\/(file|folder|#)?.+)|(\/Root\/?.+)")
)
@MeganzClient.handle_checks
async def dl_from(_: MeganzClient, msg: Message):
    # Push info to temp db
    GLOB_TMP[msg.id] = [msg.text, f"{_.dl_loc}/{msg.id}"]
    await msg.reply(
        "Select what you want to do 🤗",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Download 💾", callback_data=f"dwn_mg-{msg.id}")],
                [InlineKeyboardButton("Info ℹ️", callback_data=f"info_mg-{msg.id}")],
                [InlineKeyboardButton("Close ❌", callback_data="closeqcb")],
            ]
        ),
    )


@MeganzClient.on_callback_query(filters.regex(r"dwn_mg?.+"))
@MeganzClient.handle_checks
async def dl_from_cb(client: MeganzClient, query: CallbackQuery):
    # Access saved info
    dtmp = GLOB_TMP.pop(int(query.data.split("-")[1]))
    url = dtmp[0]
    dlid = dtmp[1]
    qcid = query.message.chat.id

    # Create unique download folder
    if not path.isdir(dlid):
        makedirs(dlid)

    # Download the file/folder
    resp = await query.edit_message_text(
        "Your download is starting 📥...", reply_markup=None
    )

    conf = None
    if client.is_public:
        udoc = await client.database.is_there(qcid)
        if udoc:
            conf = f"--username {udoc['email']} --password {udoc['password']}"
    cli = MegaTools(client, conf)

    f_list = await cli.download(url, qcid, resp.id, path=dlid)
    try:
        await query.edit_message_text("Successfully downloaded the content 🥳")
    except Exception as e:
        await query.edit_message_text(
            f"""
            Oops 🫨, Somethig bad happend!

            `{e}`
            """
        )
    # Send file(s) to the user
    await resp.edit("Trying to upload now 📤...")
    await client.send_files(f_list, qcid, resp.id)
    cleanup(dlid)
    await resp.delete()


@MeganzClient.on_callback_query(filters.regex(r"info_mg?.+"))
@MeganzClient.handle_checks
async def info_from_cb(_: MeganzClient, query: CallbackQuery):
    url = GLOB_TMP.pop(int(query.data.split("-")[1]))[0]
    size, name = MegaTools.file_info(url)
    await query.edit_message_text(
        f"""
》 **File Details**

**📛 Name:** `{name}`
**🗂 Size:** `{size}`
**📎 URL:** `{url}`

""",
        reply_markup=None,
    )
