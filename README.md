> [!WARNING]
>
> There is little active development going on and the project (under the Nexa brand) has been scheduled to be sunset.
> 
> The project may still receive patches for usability though schedule is not defined
> 
> Latest functionality update was on: 2026-03-06

<p align="center">
	<img src="assests/logo.png" width=200, height=200/>
	<br>
	<a href="https://itz-fork.gitbook.io/mega.nz-bot"><img src="https://img.shields.io/badge/Docs-e6615f?style=for-the-badge&logo=gitbook&logoColor=white" /></a>
	<a href="https://t.me/Nexa_bots"><img src="https://img.shields.io/badge/Support-0a0a0a?style=for-the-badge&logo=telegram&logoColor=white" /></a>
</p>


# Mega.nz-Bot - Cypher 🥷
A simple telegram bot to download, upload files or folders from [Mega.nz](https://mega.nz/)


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
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://github.com/partiallywritten/X-Bin-Patch#deployment)

### Local

**Recomended,**

Use official Docker image to run Mega.nz-Bot 🐳

- Install Docker on your server
- Create the .env file (see [env sample](/.env.sample) and [config vars](https://itz-fork.gitbook.io/mega.nz-bot/config-vars))
- Pull the docker image
	```
	docker pull ghcr.io/partiallywritten/meganzbot:latest
	```
- Run it! (`.env` is path to .env file you created)
	```
	docker run --env-file .env ghcr.io/partiallywritten/meganzbot
	```

**Legacy Metods,**

1) Using installer script

	If you're using a linux distro with `apt`, `apk`, `pacman` or `dnf` as the package manager, you can use the official installer script to setup [Mega.nz-Bot](https://github.com/partiallywritten/Mega.nz-Bot).

	```bash
	curl -sS -O https://raw.githubusercontent.com/partiallywritten/Mega.nz-Bot/main/installer.sh && chmod +x installer.sh && ./installer.sh
	```

2) Using classic git clone

	- Clone the Repo
	```
	git clone https://github.com/partiallywritten/Mega.nz-Bot
	```
	- Enter the directory
	```
	cd Mega.nz-Bot
	```
	- Create a new virtual environment
	```
	python -m venv .venv
	source .venv/bin/activate
	```
	- Install Requirements
	```
	pip3 install -U -r requirements.txt
	```
	- Install [megatools](https://megatools.megous.com/), [ffmpeg](https://ffmpeg.org/download.html) according to your system
	- Create a `.env` file (see [example](/.env.sample))
	- Fill config vars with your own values ([How to get config values](#config-vars)),
	- Run the Bot (using same shell session),
	```
	python3 -m megadl

	# If you get erros such as ModuleNotFoundError, use below command
	.venv/bin/python3 -m megadl
	```

### Config vars
Please refer to [documentation](https://itz-fork.gitbook.io/mega.nz-bot/config-vars)


[^1]: This only applies to public contents and you're still limited by the daily download quota limit of the mega.nz platform

# Support
[![Support Group](https://img.shields.io/badge/Support_Group-0a0a0a?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Nexa_bots)
