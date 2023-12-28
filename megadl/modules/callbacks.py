# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Contains global callbacks

from pyrogram import filters
from pyrogram.types import CallbackQuery

from megadl import MeganzClient
from megadl.helpers.sysfncs import kill_family


@MeganzClient.on_callback_query(filters.regex(r"cancelqcb?.+"))
@MeganzClient.handle_checks
async def close_gb(client: MeganzClient, query: CallbackQuery):
    _mid = int(query.data.split("-")[1])
    try:
        # Remove user from global temp db
        dtmp = client.glob_tmp.get(_mid)
        
        # cancel if user has a download running
        prcid = client.mega_running.get(query.message.chat.id)
        if prcid:
            await kill_family(prcid)

        # Remove download folder of the user
        if dtmp:
            await client.full_cleanup(dtmp[1], _mid)
    except:
        pass
    await query.edit_message_text(
        "Process was canceled by the user ❌",
        reply_markup=None,
    )
