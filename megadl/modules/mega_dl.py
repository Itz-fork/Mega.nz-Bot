# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Handle mega.nz download function


import re
from os import path, makedirs

from pyrogram import filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from megadl import CypherClient
from megadl.lib.megatools import MegaTools


@CypherClient.on_message(
    filters.regex(r"(https?:\/\/mega\.nz\/(file|folder|#)?.+)|(\/Root\/?.+)")
)
@CypherClient.run_checks
async def dl_from(client: CypherClient, msg: Message):
    # Push info to temp db
    _mid = msg.id
    _usr = msg.from_user.id
    client.glob_tmp[_usr] = [msg.text, f"{client.dl_loc}/{_usr}"]
    await msg.reply(
        "**Select what you want to do 🤗**",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Download 💾", callback_data=f"dwn_mg-{_mid}")],
                [InlineKeyboardButton("Info ℹ️", callback_data=f"info_mg-{_mid}")],
                [InlineKeyboardButton("Cancel ❌", callback_data=f"cancelqcb-{_usr}")],
            ]
        ),
    )


prv_rgx = r"(\/Root\/?.+)"


@CypherClient.on_callback_query(filters.regex(r"dwn_mg?.+"))
@CypherClient.run_checks
async def dl_from_cb(client: CypherClient, query: CallbackQuery):
    # Access saved info
    _mid = int(query.data.split("-")[1])
    qcid = query.message.chat.id
    qusr = query.from_user.id
    dtmp = client.glob_tmp.get(qusr)
    url = dtmp[0]
    dlid = dtmp[1]

    # weird workaround to add support for private mode
    conf = None
    if client.is_public:
        udoc = await client.database.is_there(qusr, True)
        if not udoc and re.match(prv_rgx, url):
            return await query.edit_message_text(
                "`You must be logged in first to download this file 😑`"
            )
        if udoc:
            conf = f"--username {client.cipher.decrypt(udoc['email']).decode()} --password {client.cipher.decrypt(udoc['password']).decode()}"

    # Create unique download folder
    if not path.isdir(dlid):
        makedirs(dlid)

    # Download the file/folder
    resp = await query.edit_message_text(
        "`Your download is starting 📥...`", reply_markup=None
    )

    cli = MegaTools(client, conf)

    f_list = None
    f_list = await cli.download(
        url,
        qusr,
        qcid,
        resp.id,
        path=dlid,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Cancel ❌", callback_data=f"cancelqcb-{qusr}")],
            ]
        ),
    )
    if not f_list:
        return

    await query.edit_message_text("`Successfully downloaded the content 🥳`")
    # update download count
    await client.database.plus_fl_count(qusr, downloads=len(f_list))
    # Send file(s) to the user
    await resp.edit("`Trying to upload now 📤...`")
    await client.send_files(
        f_list,
        qcid,
        resp.id,
        reply_to_message_id=_mid,
        caption=f"**Join @NexaBotsUpdates ❤️**",
    )
    await client.full_cleanup(dlid, qusr)
    await resp.delete()


@CypherClient.on_callback_query(filters.regex(r"info_mg?.+"))
@CypherClient.run_checks
async def info_from_cb(client: CypherClient, query: CallbackQuery):
    url = client.glob_tmp.get(query.from_user.id)[0]
    retrieved = await MegaTools.get_info(url)

    if isinstance(retrieved, list):
        await query.edit_message_text(
            f"""
》 **File Details**

**📛 Name:** `{retrieved[0]}`
**🗂 Size:** `{retrieved[1]}`
**📎 URL:** `{url}`
""",
            reply_markup=None,
        )

    else:
        await query.edit_message_text(
            f"""
`{retrieved}`
""",
            reply_markup=None,
        )
