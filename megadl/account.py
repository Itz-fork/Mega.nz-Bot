# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

from mega import Mega
from pyrogram import Client
from pyrogram.types import Message

from config import Config

email = Config.MEGA_EMAIL
password = Config.MEGA_PASSWORD

mega = Mega()

# Mega User Account
if Config.USER_ACCOUNT == "True":
  try:
    m = mega.login(email, password)
  except:
    print("Please Check Your Config Vars. Mega Email or Password is Missing! \nOr Change USER_ACCOUNT var value 'False' to Login as Anonymouse Account! \n\n Mega.nz Bot is Leaving The World....")
    exit()

# If there is no User account Bot can login as a anonymouse user. (This is the default option)
if Config.USER_ACCOUNT == "False":
  try:
    m = mega.login()
  except:
    print("Can't Login as a Anonymouse user for some reason. Can You Login with Your Mega Account? \n\n Bot is Leaving This world...")
    exit()


# Method to check if user is using Mega user account
def is_using_mega_acc(func):
    async def using_mega_acc(client: Client, message: Message):
      if Config.USER_ACCOUNT == "True":
        return await func(client, message)
      else:
        await message.reply_text("You didn't setup a Mega.nz Account to Get details!")
        return
      
      return using_mega_acc
