# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Handle mega.nz upload function

from time import time
from pyrogram import filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from megadl import MegaCypher
from megadl.lib.ddl import Downloader
from megadl.lib.megatools import MegaTools
from megadl.lib.pyros import track_progress


# Respond only to Documents, Photos, Videos, GIFs, Audio and to urls other than mega
@MegaCypher.on_message(
    filters.document
    | filters.photo
    | filters.video
    | filters.animation
    | filters.audio
    | filters.regex(
        r"((http|https)://)(www.)?(?!mega)[a-zA-Z0-9@:%._\+~#?&//=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%._\+~#?&//=]*)"
    )
)
@MegaCypher.run_checks
async def up_to(_: MegaCypher, msg: Message):
    _mid = msg.id
    await msg.reply(
        "Select what you want to do 🤗",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Upload 🗃", callback_data=f"up_tgdl-{_mid}")],
                [InlineKeyboardButton("Cancel ❌", callback_data=f"cancelqcb-{_mid}")],
            ]
        ),
    )


@MegaCypher.on_callback_query(filters.regex(r"up_tgdl?.+"))
@MegaCypher.run_checks
async def to_up_cb(client: MegaCypher, query: CallbackQuery):
    # Get message content
    _mid = int(query.data.split("-")[1])
    qcid = query.message.chat.id
    qmid = query.message.id

    # weird workaround to add support for private mode
    conf = None
    if client.is_public:
        udoc = await client.database.is_there(qcid, True)
        if not udoc:
            return await query.edit_message_text(
                "You must be logged in first to download this file 😑"
            )
        if udoc:
            conf = f"--username {client.cipher.decrypt(udoc['email']).decode()} --password {client.cipher.decrypt(udoc['password']).decode()}"

    strtim = time()
    msg = await client.get_messages(qcid, _mid)
    # Status msg
    await client.edit_message_text(
        qcid, qmid, "Trying to download the file 📥", reply_markup=None
    )
    # update upload count
    await client.database.plus_fl_count(qcid, uploads=1)

    # Download files accordingly
    dl_path = None
    if msg.media:
        dl_path = await client.download_media(
            msg, progress=track_progress, progress_args=(client, [qcid, qmid], strtim)
        )
    else:
        dl = Downloader()
        dl_path = await dl.download(msg.text, client.dl_loc, client, (qcid, qmid))

    # Upload the file
    cli = MegaTools(client, conf)

    limk = await cli.upload(dl_path, qcid, qmid)
    await client.edit_message_text(
        qcid,
        qmid,
        f"Your file has been uploaded to Mega.nz ✅ \n\nLink 🔗: `{limk}`",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Visit 🔗", url=limk)]]
        ),
    )
    await client.full_cleanup(dl_path, _mid)
