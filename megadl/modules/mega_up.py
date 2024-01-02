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

from megadl import CypherClient
from megadl.lib.ddl import Downloader
from megadl.lib.megatools import MegaTools
from megadl.helpers.pyros import track_progress


# Respond only to Documents, Photos, Videos, GIFs, Audio and to urls other than mega
@CypherClient.on_message(
    filters.document
    | filters.photo
    | filters.video
    | filters.animation
    | filters.audio
    | filters.regex(
        r"((http|https)://)(www.)?(?!mega)[a-zA-Z0-9@:%._\+~#?&//=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%._\+~#?&//=]*)"
    )
)
@CypherClient.run_checks
async def up_to(_: CypherClient, msg: Message):
    _mid = msg.id
    await msg.reply(
        "**Select what you want to do 🤗**",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Upload 🗃", callback_data=f"up_tgdl-{_mid}")],
                [
                    InlineKeyboardButton(
                        "Cancel ❌", callback_data=f"cancelqcb-{msg.from_user.id}"
                    )
                ],
            ]
        ),
    )


@CypherClient.on_callback_query(filters.regex(r"up_tgdl?.+"))
@CypherClient.run_checks
async def to_up_cb(client: CypherClient, query: CallbackQuery):
    # Get message content
    _mid = int(query.data.split("-")[1])
    qmid = query.message.id
    qcid = query.message.chat.id
    qusr = query.from_user.id

    # weird workaround to add support for private mode
    conf = None
    if client.is_public:
        udoc = await client.database.is_there(qusr, True)
        if not udoc:
            return await query.edit_message_text(
                "`You must be logged in first to download this file 😑`"
            )
        if udoc:
            conf = f"--username {client.cipher.decrypt(udoc['email']).decode()} --password {client.cipher.decrypt(udoc['password']).decode()}"

    # Get message
    msg = await client.get_messages(qcid, _mid)
    strtim = time()
    # Status msg
    await query.edit_message_text("`Trying to download the file 📥`", reply_markup=None)
    # update upload count
    await client.database.plus_fl_count(qusr, uploads=1)

    # Download files accordingly
    dl_path = None
    if msg.media:
        dl_path = await client.download_media(
            msg, progress=track_progress, progress_args=(client, [qcid, qmid], strtim)
        )
    else:
        dl = Downloader(client)
        dl_path = await dl.download(
            msg.text,
            client.dl_loc,
            (qcid, qmid, qusr),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Cancel ❌", callback_data=f"cancelqcb-{qusr}")]]
            ),
        )

    # Upload the file
    cli = MegaTools(client, conf)

    limk = await cli.upload(dl_path, qusr, qcid, qmid)
    await query.edit_message_text(
        f"`Your file has been uploaded to Mega.nz ✅`\n**Link 🔗:** `{limk}`",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Visit 🔗", url=limk)]]
        ),
    )
    await client.full_cleanup(dl_path, qusr)
