# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

from mega import Mega
from config import Config

email = Config.MEGA_EMAIL
password = Config.MEGA_PASSWORD

mega = Mega()

# Mega User Account
if Config.USER_ACCOUNT == "True":
  m = mega.login(email, password)
else:
  m = mega.login()
