# Mega.nz-Bot (nightly 🌃)
A simple telegram bot to download, upload files or folders from [Mega.nz](https://mega.nz/)


# Features
- Download, Upload fies/folders easily ⚡
- No login required 🙅‍♂️
- Support for Mega.nz user account 🗃️
- Support for both private and public content 🤝

> Note ⚠️️:
> Please see [Roadmap](#Roadmap) for current feature implementations 🤗
> This is the successor to the popular [Mega.nz-Bot](https://github.com/Itz-fork/Mega.nz-Bot/tree/legacy). So don't expect all of it's original features.


# Config Vars 📓
Config vars are stored `.env` file at the root of the bot. Check [sample file](/.env.sample) for more info


# Deploy
Deploy your own Bot ♥️! **Star 🌟 Fork 🍴 and Deploy**

### Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://github.com/Itz-fork/X-Bin-Patch#deployment)

### local
---
**Tip 💡:**
If you're using a linux distro with `apt`, `pacman` or `dnf` as the package manager, you can use the official installer script to setup [Mega.nz-Bot](https://github.com/Itz-fork/Mega.nz-Bot).

```bash
curl -sS https://raw.githubusercontent.com/Itz-fork/Mega.nz-Bot/nightly/installer.sh | bash
```
---

To setup [Mega.nz-Bot](https://github.com/Itz-fork/Mega.nz-Bot) follow these steps,

- Clone the Repo,
```
git clone -b nightly https://github.com/Itz-fork/Mega.nz-Bot
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
- Create a `.env` file (see [example](/.env.sample))
- Fill config vars with your own values ([How to get config values](https://github.com/Itz-fork/Mega.nz-Bot#config-vars-)),
- Run the Bot,
```
python3 -m megadl
```

# Roadmap
- [ ] Implement private mode
- [ ] Url to Mega.nz uploader
- [ ] Better CLI output parser
- [x] Heroku support
- [x] Port [installer](https://github.com/Itz-fork/Mega.nz-Bot/blob/legacy/startup.sh)
- [ ] Add better documentation


# Support
[![Support Group](https://img.shields.io/badge/Support_Group-0a0a0a?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Nexa_bots)