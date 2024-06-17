# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Callbacks that can be used globally

import logging
import asyncio


from pyrogram import filters
from pyrogram.types import CallbackQuery

from megadl import CypherClient
from megadl.helpers.sysfncs import kill_family


@CypherClient.on_callback_query(filters.regex(r"cancelqcb?.+"))
@CypherClient.run_checks
async def close_gb(client: CypherClient, query: CallbackQuery):
    usr = int(query.data.split("-")[1])
    try:
        # get user from global temp db
        dtmp = client.glob_tmp.get(usr)

        # cancel if user has a download running
        # this cancels both mega and ddl downloads/uploads
        # it should'nt be a problem since user can do either of those task at a time
        mg_prc = client.mega_running.get(usr)
        dl_prc = client.ddl_running.get(usr)
        if mg_prc:
            await kill_family(mg_prc)
        if dl_prc:
            dl_prc.cancel()
            await asyncio.sleep(0)

        # Remove download folder of the user
        if dtmp:
            await client.full_cleanup(dtmp[1], usr)
    except Exception as e:
        logging.warning(e)
    await query.edit_message_text(
        "`Process was canceled by the user ❌`",
        reply_markup=None,
    )
