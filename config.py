# Copyright (c) 2022 Itz-fork

import os


class Config(object):
    APP_ID = int(os.environ.get("APP_ID", 1234567))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())
    IS_PUBLIC_BOT = os.environ.get("IS_PUBLIC_BOT") in ["True", "true"]
    LOGS_CHANNEL = int(os.environ.get("LOGS_CHANNEL")) if os.environ.get("LOGS_CHANNEL") else None
    # DON'T CHANGE THESE 2 VARS
    DOWNLOAD_LOCATION = "./NexaBots"
    TG_MAX_SIZE = 2040108421
    # Mega User Account
    MEGA_EMAIL = os.environ.get("MEGA_EMAIL")
    MEGA_PASSWORD = os.environ.get("MEGA_PASSWORD")