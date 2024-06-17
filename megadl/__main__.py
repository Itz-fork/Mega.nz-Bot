# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: __main__.py

from pyrogram import idle

from . import CypherClient

# Run the bot
if __name__ == "__main__":
    # Custom pyrogram client
    print("> Starting Client")
    CypherClient.start()
    print("--------------------")
    idle()
