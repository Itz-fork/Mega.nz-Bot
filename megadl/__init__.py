# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: __init__.py

import os
import sys
import logging

# start msg
print("Mega.nz Bot - Cypher is starting...")

# uvloop integration for better asyncio performance
# only on Unix-like systems (not Windows)
if sys.platform != "win32":
    try:
        import uvloop
        uvloop.install()
        print("> Using uvloop for better performance")
    except ImportError:
        pass

# loading config
from dotenv import load_dotenv
print("--------------------")
print("> Loading config")
if os.path.isfile('.env'):
    load_dotenv()
else:
    logging.warning("WARNING: No .env file found")

# client
from .helpers.cypher import MeganzClient
CypherClient: "MeganzClient" = MeganzClient()