# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

import os
import re
import subprocess

from time import time
from filetype import guess
from megadl.helpers_nexa.mega_help import progress_for_pyrogram
from megadl import meganzbot as Client

async def run_shell_cmds(command):
    run = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    shell_ouput = run.stdout.read()[:-1].decode("utf-8")
    return shell_ouput

async def get_vid_duration(input_video):
    result = await run_shell_cmds(f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {input_video}")
    return int(result)

async def guess_and_send(input_file, chat_id, message, thumb_path="cache"):
    start_time = time()
    guessedfilemime = guess(f"{input_file}")
    try:
        mention = (await Client.get_me()).mention
    except:
        mention = "**Your Mega.nz-Bot!**"
    if not guessedfilemime or not guessedfilemime.mime:
        return await Client.send_document(chat_id=chat_id, document=f"{input_file}", caption=f"`Uploaded by` {mention}", progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", message, start_time))
    try:
        filemimespotted = guessedfilemime.mime
        # For gifs
        if re.search(r'\bimage/gif\b', filemimespotted):
            await Client.send_animation(chat_id=chat_id, animation=f"{input_file}", caption=f"`Uploaded by` {mention}", progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", message, start_time))
        # For images
        elif re.search(r'\bimage\b', filemimespotted):
            await Client.send_photo(chat_id=chat_id, photo=f"{input_file}", caption=f"`Uploaded by` {mention}", progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", message, start_time))
        # For videos
        elif re.search(r'\bvideo\b', filemimespotted):
            viddura = await get_vid_duration(input_video=f"{input_file}")
            thumbnail_path = f"{thumb_path}/thumbnail_{os.path.basename(input_file)}.jpg"
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            await run_shell_cmds(f"ffmpeg -i {input_file} -ss 00:00:01.000 -vframes 1 {thumbnail_path}")
            await Client.send_video(chat_id=chat_id, video=f"{input_file}", duration=viddura, thumb=thumbnail_path, caption=f"`Uploaded by` {mention}", progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", message, start_time))
        # For audio
        elif re.search(r'\baudio\b', filemimespotted):
            await Client.send_audio(chat_id=chat_id, audio=f"{input_file}", caption=f"`Uploaded by` {mention}", progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", message, start_time))
        else:
            await Client.send_document(chat_id=chat_id, document=f"{input_file}", caption=f"`Uploaded by` {mention}", progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", message, start_time))
    except Exception as e:
        print(e)
        await Client.send_document(chat_id=chat_id, document=f"{input_file}", caption=f"`Uploaded by` {mention}", progress=progress_for_pyrogram, progress_args=("**Trying to Upload Now!** \n", message, start_time))