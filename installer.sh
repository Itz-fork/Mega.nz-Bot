#!/usr/bin/env bash


# COLORS #
White="\033[1;37m"
Red="\033[1;31m"
Yellow="\033[1;93m"
Green="\033[1;32m"
Un_Purple="\033[4;35m"
Reset="\033[0m"

# Variables
PKGMN=""
declare -A pkgs_git=([apt]=git-all [pacman]=git [dnf]=git-all)
declare -A pkgs_pip=([apt]=python3-pip [pacman]=python-pip [dnf]=python3-pip)


# Output functions #
function show_process() {
    echo -e "${White}==> ${1}${Reset}"
}

function show_hint() {
    echo -e "  💡: ${Yellow}${1}${Reset}"
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

    is_git=$(command -v git &> /dev/null)
    is_pip3=$(command -v pip3 &> /dev/null)
    is_ffmpeg=$(command -v ffmpeg &> /dev/null)
    is_megatools=$(command -v megatools &> /dev/null)

    if ! $is_git ; then
        pkg_installer ${pkgs_git[$PKGMN]}
    elif ! $is_pip3 ; then
        pkg_installer ${pkgs_pip[$PKGMN]}
    elif ! $is_ffmpeg ; then
        pkg_installer ffmpeg
    elif ! $is_megatools ; then
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

    # Mega account
    def_mail="your@mail.com"
    def_pass="strong#password"
    read -p "Enter your Mega.nz Email [$def_mail]: " mega_email
    mega_email=${mega_email:-def_mail}
    read -p "Enter your Mega.nz Passsword [$def_pass]: " mega_password
    mega_password=${mega_password:-def_pass}

    touch .env
    cat <<EOF >> .env
APP_ID=$api_id
API_HASH=$api_hash
BOT_TOKEN=$bot_token

USE_ENV=True
MEGA_EMAIL=$mega_email
MEGA_PASSWORD=$mega_password

DOWNLOAD_LOCATION=${PWD}/NexaBots
CHUNK_SIZE=10240
TG_MAX_SIZE=2040108421
EOF

   show_hint "If your bot won't work as expected, try reassigning USE_ENV and DOWNLOAD_LOCATION in .env file"
}


function run_installer() {
    echo -e "${White}${Un_Purple}Welcome to ${Red}Mega.nz-Bot${Reset}${White}${Un_Purple} Setup!${Reset}"

    exit 0
    setup_env
    clone_repo
    check_deps
    gen_env

    show_hint "You can start the bot with: python3 -m megadl"
}

run_installer