# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

from mega import Mega
from config import Config
from megadl.data import PROCESS_TEXT, LOGIN_ERROR_TEXT, LOGGED_AS_USER

# Mega user account credentials
mega = Mega()


# Mega Account Login
def login_to_mega():
    try:
        if Config.MEGA_EMAIL and Config.MEGA_PASSWORD is not None:
            # Login as Mega user account
            login_to_mega.m = mega.login(
                Config.MEGA_EMAIL, Config.MEGA_PASSWORD)
            print(LOGGED_AS_USER)
        else:
            print(LOGIN_ERROR_TEXT)
            # Login as anonymous account
            login_to_mega.m = mega.login()
    except Exception as e:
        print(f"Error: \n{e}")
        exit()


# Mega client
print(PROCESS_TEXT.format("Trying to Log Into Mega.nz ..."))
login_to_mega()
m = login_to_mega.m
