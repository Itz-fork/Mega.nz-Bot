# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: __main__.py


from pyrogram import idle

from . import CypherClient
# loading config
from dotenv import load_dotenv
print("--------------------")
print("> Loading config")
load_dotenv()

# client
from .helpers.cypher import MeganzClient
CypherClient: "MeganzClient" = MeganzClient()

# Run the bot
if __name__ == "__main__":
    # Custom pyrogram client
    print("> Starting Client")
    CypherClient.start()
    print("--------------------")
    idle()
