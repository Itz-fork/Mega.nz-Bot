# Copyright (c) 2021 - Present partiallywritten
# Author: https://github.com/partiallywritten
# Project: https://github.com/partiallywritten/Mega.nz-Bot
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
