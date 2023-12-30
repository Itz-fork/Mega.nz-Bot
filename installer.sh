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
PKGMN=""
declare -A pkgs_git=([apt]=git-all [pacman]=git [dnf]=git-all)
declare -A pkgs_pip=([apt]=python3-pip [pacman]=python-pip [dnf]=python3-pip)


# Output functions
function show_process() {
    echo -e "${White}==> ${1}${Reset}"
}

function show_hint() {
    echo -e "  Tip 💡: ${Yellow}${1}${Reset}"
}

function show_error() {
    echo -e "${Red}ERROR: ${1}${Reset}"
    if [ $2 == "noex" ]; then
        :
    else
        exit 1
    fi
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
    else show_error "Your system isn't compatible with the installer"
    fi
}


# Install packages for the current system
function pkg_installer() {
    echo -e "${White}   > Installing ${1}${Reset}"

    case $PKGMN in

        pacman)
            sudo pacman -S $1 &> /dev/null || show_error "pacman: Unable to install ${1}"
            ;;
        
        apt)
            sudo apt install $1 &> /dev/null || show_error "apt: Unable to install ${1}"
            ;;
        
        dnf)
            sudo dnf install $1 &> /dev/null || show_error "dnf: Unable to install ${1}"
            ;;
        
        *)
            show_error "Your system isn't compatible with the installer"
            ;;
            
    esac
}


# CLone git repo
function clone_repo() {
    show_process "Cloning Mega.nz-Bot repository"
    git clone -b nightly https://github.com/Itz-fork/Mega.nz-Bot.git || show_error "git: Clone failed"

    show_process "Changing current working directory"
    cd Mega.nz-Bot || show_error "fs: 'Mega.nz-Bot' not found"
}


# Check dependencies
function check_deps() {
    show_process "Checking dependencies 🔍"
    if ! command -v git &> /dev/null ; then
        pkg_installer ${pkgs_git[$PKGMN]}
    elif ! command -v pip3 &> /dev/null ; then
        pkg_installer ${pkgs_pip[$PKGMN]}
    elif ! command -v ffmpeg &> /dev/null ; then
        pkg_installer ffmpeg
    elif ! command -v megatools &> /dev/null ; then
        pkg_installer megatools
    fi

    show_process "Setting up python virtual environment"
    python3 -m venv .venv
    source .venv/bin/activate

    pip3 install -U -r requirements.txt ||
        pip install -U -r requirements.txt ||
            show_error "python: Unable to install requirements"
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
        read -p "Do you want to create private bot with pre-configured mega account? [y/n]" add_mega
        case $add_mega in
            y|yes|Y|Yes ) private_bot=true; break;;
            * ) private_bot=false; break;;
        esac
    done
    if $private_bot ; then
        read -p "Enter your Mega.nz Email [$def_mail]: " mega_email
        mega_email="MEGA_EMAIL=${mega_email:-def_mail}"
        read -p "Enter your Mega.nz Passsword [$def_pass]: " mega_password
        mega_password="MEGA_PASSWORD=${mega_password:-def_pass}"
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
        read -p "Do you want to see user activity logs? [y/n]" see_logs
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
        read -p "Do you want to setup mongodb? [y/n]" set_mongo
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
    

    touch .env || echo "" > .env
    cat <<EOF >> .env
APP_ID=$api_id
API_HASH=$api_hash
BOT_TOKEN=$bot_token

$mega_email
$mega_password

USE_ENV=False
AUTH_USERS=$auth_users
$log_chat
$mongo_url
CYPHER_KEY=$cypher_key

DOWNLOAD_LOCATION="${PWD}"/NexaBots
CHUNK_SIZE=524288
TG_MAX_SIZE=2040108421
EOF

   show_hint "If your bot won't work as expected, try reassigning USE_ENV and DOWNLOAD_LOCATION in .env file. Not sure what to do? Contact support at @Nexa_bots"
}


function run_installer() {
    echo -e "${White}${Un_Purple}Welcome to ${Red}Mega.nz-Bot${Reset}${White}${Un_Purple} - ${Cyan}Cypher${Reset}${White}${Un_Purple} Setup!${Reset}"

    exit
    setup_env
    clone_repo
    check_deps
    gen_env

    show_hint "You can start the bot with: python3 -m megadl"
}

run_installer