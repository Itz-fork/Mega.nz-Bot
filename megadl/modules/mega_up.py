# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Responsible for upload function

from time import time
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from megadl.helpers.files import cleanup
from megadl.lib.megatools import MegaTools
from megadl.lib.pyros import track_progress


# Respond only to Documents/Photos/Videos/GIFs and Audio
@Client.on_message(
    filters.document | filters.photo | filters.video | filters.animation | filters.audio
)
async def to_up(_: Client, msg: Message):
    await msg.reply(
        "Select what you want to do 🤗",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Download 💾", callback_data=f"up_tgdl-{msg.id}")],
                [InlineKeyboardButton("Close ❌", callback_data="closeqcb")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex(r"up_tgdl?.+"))
async def to_up_cb(_: Client, query: CallbackQuery):
    # Get message content
    qcid = query.message.chat.id
    qmid = query.message.id
    strtim = time()
    msg = await _.get_messages(qcid, int(query.data.split("-")[1]))
    dl_path = await _.download_media(
        msg, progress=track_progress, progress_args=(_, [qcid, qmid], strtim)
    )
    # Upload the file
    cli = MegaTools(_)
    limk = await cli.upload(dl_path, qcid, qmid)
    await _.edit_message_text(
        qcid,
        qmid,
        "Your file has been uploaded to Mega.nz ✅",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Visit 🔗", url=limk)]]
        ),
    )
    cleanup(dl_path)