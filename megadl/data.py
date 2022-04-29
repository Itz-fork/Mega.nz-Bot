# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Help messages
Messages = {
    "dl": """
**Here is The Help Of Mega.nz Downloader Module**


  ✘ Send me a Mega.nz file/folder link. (Use `/megapy` command for old `mega.py` download engine)

  ✘ Wait Till It Download and Upload to Telegram.


**Made with ❤️ by @NexaBotsUpdates**    
""",

    "up": """
**Here is The Help Of Mega.nz Uploader Module**


  ✘ First Send or Forward a File to Me. You can also send me a direct link.

  ✘ Then Reply to that file with `/upload` command.

  ✘ Wait till It Download and Upload to Mega.nz
  

**Made with ❤️ by @NexaBotsUpdates**
""",

    "import": """
"**Here is The Help Of Mega.nz Url Importer Module**


  ✘ Send or Reply to a Public Mega.nz url with `/import` Command (**Usage:** `/import your_mega_link`)
  
  ✘ Wait till It Finish


**Made with ❤️ by @NexaBotsUpdates**    
""",

    "file_info": """
**Here is The Help Of Get File Info Via Inline Module**


  ✘ Go to any chat

  ✘ Type: `{uname} details` and after that give a one space and paste your mega.nz link (**Usage:** `{uname} details your_mega_link`)


**Made with ❤️ by @NexaBotsUpdates**
""",

    "acc_info": """
**Here is The Help Of Get Account Info Via Inline Module**


  ✘ Go to any chat (This will send your mega.nz account data so better do this in a private chat)
  
  ✘ Type: `{uname} info` (**Usage:** `{uname} info`)


**Made with ❤️ by @NexaBotsUpdates**
"""
}


# Callback buttons
Buttons = {
    "start": [
        [InlineKeyboardButton("Help 📜", callback_data="helpcallback"),
         InlineKeyboardButton("About ⁉️", callback_data="aboutcallback")],

        [InlineKeyboardButton(
            "Go Inline", switch_inline_query_current_chat="")]
    ],

    "inline": [
        [InlineKeyboardButton("Commands Help �", callback_data="helpcallback"),
         InlineKeyboardButton("Inline Query Help �", callback_data="inlinehelpcallback")],

        [InlineKeyboardButton(
            "Go Inline", switch_inline_query_current_chat="")]
    ],

    "help": [
        [InlineKeyboardButton("Downloader 📥", callback_data="meganzdownloadercb"),
         InlineKeyboardButton("Uploader 📤", callback_data="meganzuploadercb")],

        [InlineKeyboardButton(
            "Importer 📲", callback_data="meganzimportercb")],
        [InlineKeyboardButton(
            "Back ⬅️", callback_data="startcallback")]
    ],

    "inline_help": [
        [InlineKeyboardButton("Get File Details 📖", callback_data="getfiledetailscb"),
         InlineKeyboardButton("Get Account Info 💳", callback_data="getaccoutinfo")]
    ],

    "mod_help": [
                [InlineKeyboardButton("Close ❌", callback_data="closeqcb")],

                [InlineKeyboardButton("Back ⬅️", callback_data="helpcallback")]
    ],

    "imod_help": [
        [InlineKeyboardButton("Close ❌", callback_data="closeqcb")],

        [InlineKeyboardButton(
            "Back ⬅️", callback_data="inlinehelpcallback")]
    ],

    "about": [
        [InlineKeyboardButton(
            "Source Code 🗂", url="https://github.com/Itz-fork/Mega.nz-Bot")],

        [InlineKeyboardButton("Back ⬅️", callback_data="startcallback"),
         InlineKeyboardButton("Close ❌", callback_data="closeqcb")]
    ],

    "github": [
        [InlineKeyboardButton(
            "Source Code 🗂", url="https://github.com/Itz-fork/Mega.nz-Bot")],
        [InlineKeyboardButton(
            "Support Group 🆘", url="https://t.me/Nexa_bots")]
    ],

    "cancel": [
        [InlineKeyboardButton(
            "Cancel ❌", callback_data="cancelvro")]
    ]
}


async def get_buttons(name):
    return InlineKeyboardMarkup(Buttons.get(name))

async def get_msg(name):
    return Messages.get(name)



############ DEFAULT STRINGS ############
B_START_TEXT = """
   __  ___                                     ___       __ 
  /  |/  /__ ___ ____ _      ___  ___   ____  / _ )___  / /_
 / /|_/ / -_) _ `/ _ `/ _   / _ \/_ /  /___/ / _  / _ \/ __/
/_/  /_/\__/\_, /\_,_/ (_) /_//_//__/       /____/\___/\__/ 
           /___/

Process: {}
"""

PROCESS_TEXT = """
Process: {}
"""

LOGGED_AS_USER = """
Successfully Logged Into Mega.nz User Account
"""

LOGIN_ERROR_TEXT = """
Unable to find Mega Email and Password, Loging as an anonymous User...
"""

ERROR_TEXT = """
 _____                     
| ____|_ __ _ __ ___  _ __ 
|  _| | '__| '__/ _ \| '__|
| |___| |  | | | (_) | |   
|_____|_|  |_|  \___/|_|  

Log: {}

Save the Log file and Send it to @Nexa_bots for Help :)
"""

START_TEXT="""
    _   __                   ____        __      
   / | / /__  _  ______ _   / __ )____  / /______
  /  |/ / _ \| |/_/ __ `/  / __  / __ \/ __/ ___/
 / /|  /  __/>  </ /_/ /  / /_/ / /_/ / /_(__  ) 
/_/ |_/\___/_/|_|\__,_/  /_____/\____/\__/____/ 


Bot is Running Now! Join @NexaBotsUpdates
"""
