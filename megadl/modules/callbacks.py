# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Contains global callbacks

from shutil import rmtree

from pyrogram import filters
from pyrogram.types import CallbackQuery

from megadl import MeganzClient, GLOB_TMP


@MeganzClient.on_callback_query(filters.regex(r"cancelqcb"))
@MeganzClient.handle_checks
async def close_gb(client: MeganzClient, query: CallbackQuery):
    try:
        # Remove user from global temp db
        dtmp = GLOB_TMP.pop(int(query.data.split("-")[1]))
        # cancel if user has a download running
        running = client.mega_running.get(query.message.chat.id)
        if running:
            running.kill()
        # Remove download folder of the user
        rmtree(dtmp[1])
    except:
        pass
    await query.edit_message_text(
        "Process was canceled by the user",
        reply_markup=None,
    )
