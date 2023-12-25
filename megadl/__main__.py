# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: __main__.py


from pyrogram import idle

from . import MeganzClient

# Run the bot
if __name__ == "__main__":
    # Custom pyrogram client
    meganzbot = MeganzClient()
    meganzbot.start()
    idle()
