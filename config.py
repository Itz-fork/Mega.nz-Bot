from os import getenv, getcwd


class Config(object):
    APP_ID = getenv("APP_ID")
    API_HASH = getenv("API_HASH")
    BOT_TOKEN = getenv("BOT_TOKEN")
    AUTH_USERS = set(int(x) for x in getenv("AUTH_USERS").split(" "))
    # DON'T CHANGE THESE 2 VARS
    DOWNLOAD_LOCATION = f"{getcwd()}/NexaBots"
    TG_MAX_SIZE = 2040108421
