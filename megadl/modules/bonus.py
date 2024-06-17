# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Bonus functions such as file/folder info, proxy setting and account status

from pyrogram import filters
from aiohttp import ClientSession
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from megadl import CypherClient
from megadl.lib.megatools import Regexes, MegaTools


@CypherClient.on_callback_query(filters.regex(r"info_mg?.+"))
@CypherClient.run_checks
async def info_from_cb(client: CypherClient, query: CallbackQuery):
    url = client.glob_tmp.get(query.from_user.id)[0]
    await query.edit_message_text("`Getting info ℹ️...`")
    retrieved = await MegaTools.get_info(url)

    if isinstance(retrieved, list):
        await query.edit_message_text(
            f"""
》 **File Details**

**📛 Name:** `{retrieved[1]}`
**🗂 Size:** `{retrieved[0]}`
**📎 URL:** `{url}`
""",
            reply_markup=None,
        )

    else:
        async with ClientSession() as nekoc:
            resp = await nekoc.post(
                "https://nekobin.com/api/documents", json={"content": retrieved}
            )
            if resp.status == 201:
                nekourl = f"https://nekobin.com/{(await resp.json())['result']['key']}"
                await query.edit_message_text(
                    f"**👀 View is the generated [folder info]({nekourl})**",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Visit 🔗", url=nekourl)]]
                    ),
                )
            else:
                await query.edit_message_text(
                    "`Failed to generate folder info 😕, Please try again later`"
                )


@CypherClient.on_message(filters.command("acc"))
@CypherClient.run_checks
async def acc(_: CypherClient, msg: Message):
    # Check if the user exists in database
    usr = msg.from_user.id
    udoc = await _.database.is_there(usr, True)
    if not udoc:
        return await msg.reply(
            "`You must be logged in first to check account status 😑`"
        )

    # Get user data
    email = _.cipher.decrypt(udoc["email"]).decode()
    password = _.cipher.decrypt(udoc["password"]).decode()
    conf = f"--username {email} --password {password}"
    cli = MegaTools(_, conf)
    total, used, free = await cli.user_fs()

    return await msg.reply(
        f"""
**~ Your User Account Info ~**

✦ **Email:** `{email}`
✦ **Password:** `{password}`
✦ **Storage,**
    ⤷ **Total:** `{total}`
    ⤷ **Used:** `{used}`
    ⤷ **Free:** `{free}`
"""
    )


@CypherClient.on_message(filters.command("proxy"))
@CypherClient.run_checks
async def set_user_proxy(client: CypherClient, msg: Message):
    prxy = None
    try:
        prxy = msg.text.split(None, 1)[1]
    except:
        pass
    if not prxy or not Regexes.proxy_regex.match(prxy):
        return await msg.reply(
            "Provide a proxy to set \n\nEx: `/proxy socks5h://localhost:9050`"
        )

    await client.database.update_proxy(msg.from_user.id, prxy)
    await msg.reply(
        f"Proxy set to: `{prxy}` \n\n**Note:**\nIf your download seems to stuck, it's likely due to proxy not working properly. Free proxies on internet do not work!"
    )
