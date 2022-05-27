# Mega.nz-Bot
A simple telegram bot written in Python using Pyrogram framework which helps you to download, upload and import [^1] files / folders from [Mega.nz](https://mega.nz/) cloud storage with telegram.


# Features
- ⚡ Download, Upload & Import files easily
- 📱 Mega.nz user account support
- 🙅‍♂️ No login required
- 🖇️ Almost all file / folder links are supported [^2]
- 🛡️ Can be used as either public or private bot
- 🕵️‍♂️ Inline Mode [Still In Development Stage: BETA]


# Deploy
Deploy your own Bot ♥️! **Star 🌟 Fork 🍴 and Deploy**

### Config Vars 📓,
**Mandatory Vars,**
- `APP_ID` - Your APP_ID. Get it from [my.telegram.org](my.telegram.org)
- `API_HASH` - Your API_ID. Get it from [my.telegram.org](my.telegram.org)
- `AUTH_USERS` - Telegram IDs Of Auth Users, Only they can use this bot (If you didn't set this as public bot). Separate them by a space. (Ex: `123445 2648589`)
- `BOT_TOKEN` - Your Bot Token From [@BotFather](https://t.me/BotFather)

**Non Mandatory Vars,**
- `IS_PUBLIC_BOT` - Set this to 'True' if you want to set Download Function as Public. Default to 'False'
- `LOGS_CHANNEL` - To get this, follow these steps,
    - Make a private channel
    - Send a message and copy it's link
    - The link'll be something like `https://t.me/c/12345/1`. Simply copy the `12345` part from it and add `-100` to the beginning of it. Now it'll be something like `-10012345`. That's your channel id!
- `MEGA_EMAIL` - Fill this if you want to use your own Mega Account. This is your Mega account Email
- `MEGA_PASSWORD` - Fill this if you want to use your own Mega Account. This is your Mega account Password

Check out [config.sample file](https://github.com/Itz-fork/Mega.nz-Bot/blob/main/config.sample) if you aren't using heroku 🤗

### With Heroku
> Notice ⚠️:
> Please refer the [Deployment](https://github.com/Itz-fork/X-Bin-Patch#deployment) guide inorder to deploy this bot Heroku. THIS REPO ISN'T FUCKING COMPATIBLE WITH HEROKU!

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://github.com/Itz-fork/X-Bin-Patch#deployment)

### With VPS/PC
---
**Tip 💡:**
If you're using a linux distro with `apt`, `pacman` or `dnf` package manager, you can use the official installer script to setup [Mega.nz-Bot](https://github.com/Itz-fork/Mega.nz-Bot). To do so run the following command,

```bash
curl -sS https://raw.githubusercontent.com/Itz-fork/Mega.nz-Bot/main/installer.sh | bash
```
---

To setup [Mega.nz-Bot](https://github.com/Itz-fork/Mega.nz-Bot) follow these steps,

- Clone the Repo,
```
git clone https://github.com/Itz-fork/Mega.nz-Bot
```
- Enter the directory,
```
cd Mega.nz-Bot
```
- Install Requirements,
```
pip3 install -U -r requirements.txt
```
- Install [megatools](https://megatools.megous.com/), [ffmpeg](https://ffmpeg.org/download.html) according to your system
- Fill config vars with your own values ([How to get config values](https://github.com/Itz-fork/Mega.nz-Bot#config-vars-)),
    - If you have GUI system use a normal text editor like notepad, sublime text etc.
    - For CLI systems, [use nano](https://gist.github.com/Itz-fork/fd11c08ef7464bdae3663a1f9c77c9e9) and edit the config file using `nano config.py` command.
- Run the Bot,
```
bash startup.sh
```


[^1]: Only download and upload functions support folder links. Currently import function supports only for files
[^2]: Public content only


# Support
[![Support Group](https://img.shields.io/badge/Support_Group-0a0a0a?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Nexa_bots)