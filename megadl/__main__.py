# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

import os

from pyrogram import idle
from . import meganzbot
from megadl.helpers_nexa.mega_help import check_logs
from config import Config, B_START_TEXT, PROCESS_TEXT, START_TEXT

if __name__ == "__main__" :
    print(B_START_TEXT.format("Your Mega.nz-Bot is Starting! Please Wait..."))
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    meganzbot.start()
    print(PROCESS_TEXT.format("Checking Log Channel ..."))
    check_logs()
    print(START_TEXT)
    idle()