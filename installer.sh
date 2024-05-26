#!/usr/bin/env bash


# COLORS
White="\033[1;37m"
Red="\033[1;31m"
Cyan="\033[1;36m"
Yellow="\033[1;93m"
Green="\033[1;32m"
Un_Purple="\033[4;35m"
Reset="\033[0m"

# Variables
USE_DOCKER=false
PKGMN=""
declare -A pkgs_git=([apt]="sudo apt-get install git-all" [pacman]="sudo pacman -S git" [dnf]="sudo dnf install git-all" [apk]="sudo apk add git")
declare -A pkgs_pip=([apt]="sudo apt-get install python3-pip" [pacman]="sudo pacman -S python-pip" [dnf]="sudo dnf install python3-pip" [apk]="sudo apk add py3-pip")
declare -A pkgs_ffmpeg=([apt]="sudo apt-get install ffmpeg" [pacman]="sudo pacman -S ffmpeg" [dnf]="sudo dnf install ffmpeg" [apk]="sudo apk add ffmpeg")
declare -A pkgs_megatools=([apt]="sudo apt-get install megatools" [pacman]="sudo pacman -S megatools" [dnf]="sudo dnf install megatools" [apk]="apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing/; sudo apk add megatools")
declare -A pkgs_docker=([apt]="sudo apt-get update; sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release; curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg; echo 'deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable' | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null; sudo apt-get update; sudo apt-get install docker-ce docker-ce-cli containerd.io"
                    [dnf]="sudo dnf -y install dnf-plugins-core; sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo; sudo dnf install docker-ce docker-ce-cli containerd.io"
                    [pacman]="sudo pacman -S docker"
                    [apk]="sudo apk update; sudo apk add docker")


# Argument parser
while [[ $# -gt 0 ]]; do
    case "${1}" in
        -d|--docker)
            USE_DOCKER=true
            shift
            shift
            ;;
    esac
done


# Output functions
function show_process() {
    echo -e "${White}==> ${1}${Reset}"
}

function show_hint() {
    echo -e "  Tip 💡: ${Yellow}${1}${Reset}"
}

function show_error() {
    echo -e "${Red}ERROR: ${1}${Reset}"
    if [ "$2" == "noex" ]; then
        :
    else
        exit 1
    fi
}

# CLone git repo
function clone_repo() {
    show_process "Cloning Mega.nz-Bot repository"
    git clone https://github.com/Itz-fork/Mega.nz-Bot.git || show_error "git: Clone failed"

    show_process "Changing current working directory"
    cd Mega.nz-Bot || show_error "fs: 'Mega.nz-Bot' not found"
}


# Identify current package manager
function setup_env() {
    # Detect current systems package manager
    if $(command -v pacman &> /dev/null) ; then
        PKGMN=pacman
    elif $(command -v apt &> /dev/null) ; then
        PKGMN=apt
    elif $(command -v dnf &> /dev/null) ; then
        PKGMN=dnf
    elif $(command -v apk &> /dev/null) ; then
        PKGMN=apk
    else show_error "Your system isn't compatible with the installer"
    fi
}


# Install packages for the current system
function pkg_installer() {
    echo -e "${White}   > Installing ${1}${Reset}"
    eval $2 || show_error "package installer: Unable to install ${1}"
}

# Check dependencies
function check_deps() {
    show_process "Checking dependencies 🔍"
    if [ $USE_DOCKER = true ]; then
        if ! command -v git &> /dev/null ; then pkg_installer Docker "${pkgs_docker[$PKGMN]}"; fi
    else
        if ! command -v git &> /dev/null ; then pkg_installer git ${pkgs_git[$PKGMN]}; fi
        if ! command -v pip3 &> /dev/null ; then pkg_installer pip3 ${pkgs_pip[$PKGMN]}; fi
        if ! command -v ffmpeg &> /dev/null ; then pkg_installer ffmpeg ${pkgs_ffmpeg[$PKGMN]}; fi
        if ! command -v megatools &> /dev/null ; then pkg_installer megatools ${pkgs_megatools[$PKGMN]}; fi

        show_process "Setting up python virtual environment"
        python3 -m venv .venv
        source .venv/bin/activate

        pip3 install -U -r requirements.txt ||
            pip install -U -r requirements.txt ||
                show_error "python: Unable to install requirements"
    fi
}


# Generate .env file
function gen_env() {
    show_process "Generating env file ⚙️"

    # Mandotory vars
    read -p "Enter your API ID: " api_id
    read -p "Enter your API HASH: " api_hash
    read -p "Enter your BOT TOKEN: " bot_token

    # read mega.nz email and password with default values
    def_mail="your@mail.com"
    def_pass="strong#password"
    mega_email=""
    mega_password=""
    private_bot=false
    while true; do
        read -p "Do you want to create private bot with pre-configured mega account? [y/n]: " add_mega
        case $add_mega in
            y|yes|Y|Yes ) private_bot=true; break;;
            * ) private_bot=false; break;;
        esac
    done
    if $private_bot ; then
        read -p "Enter your Mega.nz Email [$def_mail]: " mega_email
        mega_email=${mega_email:-$def_mail}
        read -p "Enter your Mega.nz Password [$def_pass]: " mega_password
        mega_password=${mega_password:-$def_pass}
    fi

    # read authorized users in to a variable called auth_users
    # if auth_users are empty set to "*" otherwise check if private_bot var is set to true
    # if the private_bot var is set to true then auth_users will be the input otherwise it will be "*|<user input>"
    read -p "Enter authorized users (seperate with space) [empty for all users]: " auth_users
    auth_users=${auth_users:-"*"}
    if $private_bot ; then
        auth_users="$auth_users"
    else
        auth_users="*|$auth_users"
    fi

    # add log chat
    log_chat=""
    while true; do
        read -p "Do you want to see user activity logs? [y/n]: " see_logs
        case $see_logs in
            y|yes|Y|Yes ) see_logs=true; break;;
            * ) see_logs=false; break;;
        esac
    done

    if $see_logs ; then
        read -p "Enter a chat id where bot is an admin [preferably a channel]: " log_chat
        log_chat="LOG_CHAT=${log_chat}"
    fi
    
    
    # add mongodb url
    mongo_url=""
    while true; do
        read -p "Do you want to setup mongodb? [y/n]: " set_mongo
        case $set_mongo in
            y|yes|Y|Yes ) set_mongo=true; break;;
            * ) set_mongo=false; break;;
        esac
    done
    
    if $set_mongo ; then
        read -p "Enter the mongodb url [more info: https://t.ly/YxYXq]: " mongo_url
        mongo_url="MONGO_URI=${mongo_url}"
    fi
    

    # generate cypher key
    cypher_key=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
    

    # write config files
    touch .env || echo "" > .env
    cat <<EOF >> .env
APP_ID=$api_id
API_HASH=$api_hash
BOT_TOKEN=$bot_token
AUTH_USERS=$auth_users
$log_chat
$mongo_url
CYPHER_KEY=$cypher_key

DOWNLOAD_LOCATION=${PWD}/NexaBots
CHUNK_SIZE=524288
TG_MAX_SIZE=2040108421
EOF

    if $private_bot ; then
        if [ ! -f mega.ini ]; then
            touch mega.ini || echo "" > mega.ini
        fi
        cat <<EOF >> mega.ini

[Login]
Username = $mega_email
Password = $mega_password
EOF
    else
        cat <<EOF >> .env

USE_ENV=false
MEGA_EMAIL=$mega_email
MEGA_PASSWORD=$mega_password
EOF
    fi

    show_hint "If your bot won't work as expected, try reassigning USE_ENV and DOWNLOAD_LOCATION in .env file. Not sure what to do? Contact support at @Nexa_bots"

    show_hint "It is recommended to check the mega.ini file for more configuration options"
}


function run_installer() {
    echo -e "${White}${Un_Purple}Welcome to ${Red}Mega.nz-Bot${Reset}${White}${Un_Purple} - ${Cyan}Cypher${Reset}${White}${Un_Purple} Setup!${Reset}"
    
    setup_env
    clone_repo
    check_deps
    gen_env

    if [ $USE_DOCKER = true ]; then
        show_hint "You chose to run the bot in a docker container"
        show_hint "Once you make sure that .env file is correctly configured, you can build the bot"
        show_hint "Use: cd Mega.nz-Bot && docker build -t meganzbot && docker run meganzbot"
    else
        show_hint "You can start the bot with: cd Mega.nz-Bot && .venv/bin/python3 -m megadl"
    fi
}

run_installer