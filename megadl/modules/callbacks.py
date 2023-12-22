# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Contains global callbacks

from shutil import rmtree

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from megadl import GLOB_TMP


@Client.on_callback_query(filters.regex(r"closeqcb"))
async def close_gb(_: Client, query: CallbackQuery):
    try:
        # Remove user from global temp db
        dtmp = GLOB_TMP.pop(int(query.data.split("-")[1]))
        # Remove download folder of the user
        rmtree(dtmp[1])
    except:
        pass
    await query.edit_message_text(
        """
    Process was canceled by the user""",
        reply_markup=None,
    )
