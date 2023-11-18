# @Author: https://github.com/Itz-fork
# @Project: https://github.com/Itz-fork/Mega.nz-Bot
# @Version: nightly-0.1
# @Description: Contains code related to fs functions

from shutil import rmtree
from re import search as isit
from datetime import timedelta
from os import path, walk, makedirs, remove

from filetype import guess
from filesplit.split import Split

from bot.helpers.cors import run_partial, run_on_shell


# List all the files inside a dir
def listfiles(rpath: str):
    """
    Return all files in the path as a list
    """
    return [path.join(dpath, f) for (dpath, drnms, fnams) in walk(rpath) for f in fnams]


# Clean up function
def cleanup(cpath):
    if path.isfile(cpath):
        remove(cpath)
    elif path.isdir(cpath):
        rmtree(cpath)


# Guess the file type and send it accordingly
async def send_as_guessed(client, file, chat_id):
    """
    Upload the file to telegram as the way it should
    """
    ftype = await run_partial(guess, file)
    # Send file as a document if the file type could't be guessed
    if not ftype:
        await client.send_document(chat_id, file)
    else:
        fmime = ftype.mime
        # GIFs
        if isit(r"\bimage/gif\b", fmime):
            await client.send_animation(chat_id, file)
        # Images
        elif isit(r"\bimage\b", fmime):
            await client.send_photo(chat_id, file)
        # Audio
        elif isit(r"\baudio\b", fmime):
            await client.send_audio(chat_id, file)
        # Video
        elif isit(r"\bvideo\b", fmime):
            # Get duration of video in seconds
            _sh = await run_partial(
                run_on_shell,
                f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {file}",
            )
            vid_dur = int(float(_sh))
            # Generate thumbnail for the video
            _thumb = f"MegaDownloads/Thumbnails/{chat_id}"
            if not path.isdir(_thumb):
                makedirs(_thumb)
            _sh = await run_partial(
                run_on_shell,
                f"ffmpeg -i {file}, -ss {timedelta(seconds=int(vid_dur/10))} -vframes 1 {_thumb}",
            )
            await client.send_video(chat_id, file, duration=vid_dur, thumb=_thumb)
        # Document
        else:
            await client.send_document(chat_id, file)


# Split files
def _usesplit(path_in, path_out):
    spl = Split(path_in, path_out)
    spl.bysize(2040108421)


async def splitit(path_in, path_out):
    await run_partial(_usesplit, path_in, path_out)
