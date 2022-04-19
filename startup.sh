#!/usr/bin/bash

echo "
█▀▄▀█ █▀▀ █▀▀ ▄▀█   █▄ █ ▀█ 
█ ▀ █ ██▄ █▄█ █▀█ ▄ █ ▀█ █▄

        █▄▄ █▀█ ▀█▀
        █▄█ █▄█  █


Copyright (c) 2021 Itz-fork | @NexaBotsUpdates
"

# Helper functions to show process / error messages
function show_process_msg() {
    echo -e "$White ==> $1 $Reset"
}

function show_error_msg() {
    echo -e "ERROR: $1"
    exit
}

# Function to install megatools (https://github.com/Itz-fork/Mega.nz-Bot/blob/abe1b0736c9e85b547b806eef82c78b0f574f215/installer.sh#L70)

OS_TYPE=$( (lsb_release -ds || cat /etc/*release || uname -om) 2>/dev/null | head -n1) || "Unknown"

function install_megatools() {
    case $OS_TYPE in
        Zorin* )
            sudo apt install git-all; shift ;;
        Debian* )
            sudo apt install git-all; shift ;;
        Ubuntu* )
            sudo apt install git-all; shift ;;
        Fedora* )
            sudo dnf install git; shift ;;
        Arch* )
            git clone https://aur.archlinux.org/megatools.git
            cd megatools || show_error_msg "megatools dir doesn't exists rn! Tf did you do?"
            makepkg -si
            cd ..
            rm -rf megatools; shift ;;
        *)
            show_error_msg "Your system deosn't match the current list of Oses. Please install 'megatools' from - https://megatools.megous.com/"
    esac
}



function check_depends() {
    is_megatools=$(command -v megatools &> /dev/null)
    is_ffmpeg=$(command -v ffmpeg &> /dev/null)
    # Checks if megatools is installed
    if ! $is_megatools ; then
        show_process_msg "Installing megatools"
        install_megatools
    # Checks if ffmpeg is installed
    elif ! $is_ffmpeg ; then
        show_process_msg "Installing ffmpeg"
        curl -sS https://webinstall.dev/ffmpeg | bash ||
            show_error_msg "Ffmpeg is not installed. Visit - https://ffmpeg.org/download.html"
    fi
}

function run() {
    echo ">> Starting the main repo"
    python3 -m megadl
}

check_depends
run
