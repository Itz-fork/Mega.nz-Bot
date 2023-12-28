# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: File system functions

from time import time
from shutil import rmtree
from re import search as isit
from datetime import timedelta
from os import path, walk, makedirs, remove

from filetype import guess
from filesplit.split import Split

from megadl.lib.pyros import track_progress
from megadl.helpers.sysfncs import run_partial, run_on_shell


# List all the files inside a dir
def listfiles(rpath: str):
    """
    Return all files in the path as a list
    """
    return [path.join(dpath, f) for (dpath, drnms, fnams) in walk(rpath) for f in fnams]


# Clean up function
def fs_cleanup(cpath: str):
    if path.isfile(cpath):
        remove(cpath)
    elif path.isdir(cpath):
        rmtree(cpath)


# Guess the file type and send it accordingly
async def send_as_guessed(client, file, chat_id, mid):
    """
    Upload the file to telegram as the way it should
    """
    ftype = await run_partial(guess, file)
    strtim = time()
    # Send file as a document if the file type could't be guessed
    if not ftype:
        await client.send_document(chat_id, file)
    else:
        fmime = ftype.mime
        # GIFs
        if isit(r"\bimage/gif\b", fmime):
            await client.send_animation(
                chat_id,
                file,
                progress=track_progress,
                progress_args=(client, [chat_id, mid], strtim),
            )
        # Images
        elif isit(r"\bimage\b", fmime):
            await client.send_photo(
                chat_id,
                file,
                progress=track_progress,
                progress_args=(client, [chat_id, mid], strtim),
            )
        # Audio
        elif isit(r"\baudio\b", fmime):
            await client.send_audio(
                chat_id,
                file,
                progress=track_progress,
                progress_args=(client, [chat_id, mid], strtim),
            )
        # Video
        elif isit(r"\bvideo\b", fmime):
            # Get duration of video in seconds
            _sh = await run_partial(
                run_on_shell,
                f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {file}",
            )
            vid_dur = int(float(_sh))
            # Generate thumbnail for the video
            _tmpth = f"{client.tmp_loc}/thumbnails"
            _thumb = f"{_tmpth}/{{chat_id}}_{mid}.png"
            if not path.isdir(_tmpth):
                makedirs(_tmpth)
            _sh = await run_partial(
                run_on_shell,
                f"ffmpeg -i {file} -ss {timedelta(seconds=int(vid_dur/10))} -vframes 1 {_thumb}",
            )
            await client.send_video(
                chat_id,
                file,
                duration=vid_dur,
                thumb=_thumb,
                progress=track_progress,
                progress_args=(client, [chat_id, mid], strtim),
            )
        # Document
        else:
            await client.send_document(
                chat_id,
                file,
                progress=track_progress,
                progress_args=(client, [chat_id, mid], strtim),
            )


# Split files
def _usesplit(path_in, path_out):
    spl = Split(path_in, path_out)
    spl.bysize(2040108421)


async def splitit(path_in, path_out):
    await run_partial(_usesplit, path_in, path_out)
