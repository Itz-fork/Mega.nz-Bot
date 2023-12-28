# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Responsible for download function


import re
from os import path, makedirs

from pyrogram import filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from megadl import MeganzClient
from megadl.lib.megatools import MegaTools


@MeganzClient.on_message(
    filters.regex(r"(https?:\/\/mega\.nz\/(file|folder|#)?.+)|(\/Root\/?.+)")
)
@MeganzClient.handle_checks
async def dl_from(client: MeganzClient, msg: Message):
    # Push info to temp db
    _mid = msg.id
    client.glob_tmp[msg.id] = [msg.text, f"{client.dl_loc}/{_mid}"]
    await msg.reply(
        "Select what you want to do 🤗",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Download 💾", callback_data=f"dwn_mg-{_mid}")],
                [InlineKeyboardButton("Info ℹ️", callback_data=f"info_mg-{_mid}")],
                [InlineKeyboardButton("Cancel ❌", callback_data=f"cancelqcb-{_mid}")],
            ]
        ),
    )


prv_rgx = r"(\/Root\/?.+)"


@MeganzClient.on_callback_query(filters.regex(r"dwn_mg?.+"))
@MeganzClient.handle_checks
async def dl_from_cb(client: MeganzClient, query: CallbackQuery):
    # Access saved info
    _mid = int(query.data.split("-")[1])
    dtmp = client.glob_tmp.get(_mid)
    url = dtmp[0]
    dlid = dtmp[1]
    qcid = query.message.chat.id
    
    # weird workaround to add support for private mode
    conf = None
    if client.is_public:
        udoc = await client.database.is_there(qcid, True)
        if not udoc and re.match(prv_rgx, url):
            return await query.edit_message_text(
                "You need to be logged in first to download this file 😑"
            )
        if udoc:
            conf = f"--username {client.cipher.decrypt(udoc[0]).decode()} --password {client.cipher.decrypt(udoc[1]).decode()}"

    # Create unique download folder
    if not path.isdir(dlid):
        makedirs(dlid)

    # Download the file/folder
    resp = await query.edit_message_text(
        "Your download is starting 📥...", reply_markup=None
    )

    cli = MegaTools(client, conf)

    f_list = None
    try:
        f_list = await cli.download(
            url,
            qcid,
            resp.id,
            path=dlid,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Cancel ❌", callback_data=f"cancelqcb-{_mid}"
                        )
                    ],
                ]
            ),
        )
        if not f_list:
            return
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
    await client.full_cleanup(dlid, _mid)
    await resp.delete()


@MeganzClient.on_callback_query(filters.regex(r"info_mg?.+"))
@MeganzClient.handle_checks
async def info_from_cb(client: MeganzClient, query: CallbackQuery):
    url = client.glob_tmp.pop(int(query.data.split("-")[1]))[0]
    size, name = await MegaTools.file_info(url)
    await query.edit_message_text(
        f"""
》 **File Details**

**📛 Name:** `{name}`
**🗂 Size:** `{size}`
**📎 URL:** `{url}`

""",
        reply_markup=None,
    )
