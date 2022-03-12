#!/usr/bin/bash

echo "
█▀▄▀█ █▀▀ █▀▀ ▄▀█   █▄ █ ▀█ 
█ ▀ █ ██▄ █▄█ █▀█ ▄ █ ▀█ █▄

        █▄▄ █▀█ ▀█▀
        █▄█ █▄█  █


Copyright (c) 2021 Itz-fork | @NexaBotsUpdates
"

function check_depends() {
    is_megatools=$(command -v megatools &> /dev/null)
    is_ffmpeg=$(command -v ffmpeg &> /dev/null)
    # Checks if megatools is installed
    if ! $is_megatools ; then
        show_error_msg "'megatools' is not installed on this system. Please install it from - https://megatools.megous.com/"
    # Checks if ffmpeg is installed
    elif ! $is_ffmpeg ; then
        show_error_msg "'ffmpeg' is not installed on this system. Please install it from - https://ffmpeg.org/download.html"
    fi
}

function run() {
    echo ">> Starting the main repo"
    python3 -m megadl
}

check_depends
run