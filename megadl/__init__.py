# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: __init__.py

# start msg
print("Mega.nz Bot - Cypher is starting...")


# loading config
from dotenv import load_dotenv
print("--------------------")
print("> Loading config")
load_dotenv()

# client
from .helpers.cypher import MeganzClient
MegaCypher: "MeganzClient" = MeganzClient()