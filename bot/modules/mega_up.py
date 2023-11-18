# @Author: https://github.com/Itz-fork
# @Project: https://github.com/Itz-fork/Mega.nz-Bot
# @Version: nightly-0.1
# @Description: Responsible for upload function


from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.lib.megatools import MegaTools


# Respond only to Documents/Photos/Videos/GIFs and Audio
@Client.on_message(filters.document| filters.photo | filters.video | filters.animation | filters.audio)
async def to_up(_: Client, msg: Message):
    await msg.reply(
        "Should' I download it?",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Download ", callback_data=f"up_tgdl-{msg.id}")],
                [InlineKeyboardButton("Close ❌", callback_data="closeqcb")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("up_tgdl?.+"))
async def to_up_cb(_: Client, query: CallbackQuery):
    # Get message content
    qcid = query.message.chat.id
    qmid = query.message.id
    msg = await _.get_messages(qcid, int(query.data.split("-")[1]))
    dl_path = await _.download_media(msg)
    # Upload the file
    cli = MegaTools(_)
    limk = await cli.upload(dl_path, qcid, query.message.id)
    await _.edit_message_text(qcid, qmid, limk)
