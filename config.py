import os

class Config(object):
    APP_ID = int(os.environ.get("APP_ID", 123456))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
    TG_MAX_SIZE = 2097152000