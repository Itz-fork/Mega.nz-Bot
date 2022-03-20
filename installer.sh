#!/usr/bin/bash


# Colors
White="\033[1;37m"
Red="\033[1;31m"
Green="\033[1;32m"
Reset="\033[0m"


# Helper functions
function show_process_msg() {
    echo -e "$White ==> $1 $Reset"
}

function show_success_msg() {
    echo -e "\n${Green}Successfully finished$Reset$White ${1}$Reset${Green}!$Reset"
    exit
}

function show_error_msg() {
    echo -e "$Red ERROR: $1 $Reset"
    exit
}

# Script
echo -e "$White

Mega.nz-Bot Installer

"

function checkDepends() {
    is_git=$(command -v git &> /dev/null)
    is_ffmpeg=$(command -v ffmpeg &> /dev/null)
    is_pip3=$(command -v pip3 &> /dev/null)
    is_megatools=$(command -v megatools &> /dev/null)
    # Checks if git is installed
    if ! $is_git ; then
        show_process_msg "Installing git"
        sudo apt install git-all ||
            sudo pacman -S git ||
                show_error_msg "Git is not installed. Visit - https://git-scm.com/book/en/v2/Getting-Started-Installing-Git"
    # Checks if ffmpeg is installed
    elif ! $is_ffmpeg ; then
        show_process_msg "Installing ffmpeg"
        curl -sS https://webinstall.dev/ffmpeg | bash ||
            show_error_msg "Ffmpeg is not installed. Visit - https://ffmpeg.org/download.html"
    # Checks if pip3 is installed
    elif ! $is_pip3 ; then
        show_error_msg "Pip3 is not installed"
    # Checks if megatools is installed
    elif ! $is_megatools ; then
        show_process_msg "Installing megatools"
        sudo apt install megatools ||
            sudo pacman -S megatools ||
                show_error_msg "Your system deosn't use 'pacman' or 'apt' as the package manager. Please install 'megatools' from - https://megatools.megous.com/"
    fi
}

function install() {
    show_process_msg "Checking dependencies"
    checkDepends

    show_process_msg "Cloning into Mega.nz-Bot repository"
    git clone https://github.com/Itz-fork/Mega.nz-Bot || show_error_msg "Unable to clone the Mega.nz-Bot repository"

    show_process_msg "Changing the directory to 'Mega.nz-Bot'"
    cd Mega.nz-Bot || show_error_msg "'Mega.nz-Bot' folder not found"

    show_process_msg "Installing Requirements using pip3"
    pip3 install -r requirements.txt &> /dev/null || show_error_msg "Unable to install requirements"

    show_success_msg "Installation"

    echo -e "$White Please edit 'config.py' file according to your own values before runnig the bot! $Reset"
}

install