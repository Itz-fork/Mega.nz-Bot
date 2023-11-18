# @Author: https://github.com/Itz-fork
# @Project: https://github.com/Itz-fork/Mega.nz-Bot
# @Version: nightly-0.1
# @Description: __main__.py


from config import Config
from pyrogram import Client, idle

meganzbot = Client(
    name="MegaBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    plugins=dict(root="bot/modules"),
    sleep_threshold=10,
)

if __name__ == "__main__":
    meganzbot.start()
    idle()
