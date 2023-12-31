<p align="center">
	<img src="assests/logo.png" width=200, height=200/>
	<br>
	<a href="https://megabot.hirusha.codes/"><img src="https://img.shields.io/badge/Docs-e6615f?style=for-the-badge&logo=gitbook&logoColor=white" /></a>
	<a href="https://t.me/Nexa_bots"><img src="https://img.shields.io/badge/Support-0a0a0a?style=for-the-badge&logo=telegram&logoColor=white" /></a>
</p>


# Mega.nz-Bot - Cypher 🥷
A simple telegram bot to download, upload files or folders from [Mega.nz](https://mega.nz/)

# Use [nightly](https://github.com/Itz-fork/Mega.nz-Bot/tree/nightly)

> [!WARNING]
> This branch is unmaintained! New version of the project can be found at: [`nightly`](https://github.com/Itz-fork/Mega.nz-Bot/tree/nightly) branch.

# Features
- ⚡ Download, Upload files/folders easily
- 🙅‍♂️ No login required[^1]
- 🗃️ Support for Mega.nz user account
- 🤝 Support for both private and public content
- 🛡 Can be used as either private or public bot
- 🖇 Direct download link to mega.nz upload
- 🧐 See what files are in your links


# Deploy
Deploy your own Bot ♥️! **Star 🌟 Fork 🍴 and Deploy**

### Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://github.com/Itz-fork/X-Bin-Patch#deployment)

### Local
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
- Create a `.env` file (see [example](/.env.sample))
- Fill config vars with your own values ([How to get config values](#config-vars)),
- Run the Bot,
```
python3 -m megadl
```

### Config vars
Please refer to [documentation](https://megabot.hirusha.codes/config-vars)


[^1]: This only applies to public contents and you're still limited by the daily download quota limit of the mega.nz platform

# Support
[![Support Group](https://img.shields.io/badge/Support_Group-0a0a0a?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Nexa_bots)
