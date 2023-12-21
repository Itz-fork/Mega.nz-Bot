# @Author: https://github.com/Itz-fork
# @Project: https://github.com/Itz-fork/Mega.nz-Bot
# @Version: nightly-0.2
# @Description: Responsible for download function


from os import path, stat, makedirs, getenv

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from megadl import GLOB_TMP
from megadl.lib.megatools import MegaTools
from megadl.helpers.files import send_as_guessed, splitit, listfiles, cleanup


@Client.on_message(filters.regex(r"(https?:\/\/mega\.nz\/(file|folder|#)?.+)|(\/Root\/?.+)"))
async def dl_from(_: Client, msg: Message):
    # Push info to temp db
    GLOB_TMP[msg.id] = [msg.text, f"{getenv('DOWNLOAD_LOCATION')}/{msg.id}"]
    await msg.reply(
        "Select what you want to do 🤗",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Download 💾", callback_data=f"dwn_mg-{msg.id}")],
                [InlineKeyboardButton("Info ℹ️", callback_data=f"dwn_mg-{msg.id}")],
                [InlineKeyboardButton("Close ❌", callback_data="closeqcb")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex(r"dwn_mg?.+"))
async def dl_from_cb(client: Client, query: CallbackQuery):
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
        """
    📥 Your download is starting...""",
        reply_markup=None,
    )
    cli = MegaTools(client)
    f_list = await cli.download(url, qcid, resp.id, path=dlid)
    try:
        await query.edit_message_text(
            """
            🥳 Successfully downloaded the content
            """
        )
    except Exception as e:
        await query.edit_message_text(
            f"""
            Oops 🫨, Somethig bad happend!

            `{e}`
            """
        )
    # Send file(s) to the user
    await resp.edit(
        """
        🕔 Trying to upload now...
        """
    )
    for file in f_list:
        print("yeah")
        # Split files larger than 2GB
        if stat(file).st_size > 2040108421:
            await client.edit_message_text(
                qcid,
                resp.id,
                """
            The file you're trying to upload exceeds telegram limits.
            Trying to split the files...
                """,
            )
            splout = f"{dlid}/splitted"
            await splitit(file, splout)
            for file in listfiles(splout):
                await send_as_guessed(client, file, qcid, resp.id)
            cleanup(splout)
        else:
            await send_as_guessed(client, file, qcid, resp.id)
    await resp.delete()