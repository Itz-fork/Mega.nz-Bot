# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Downloader for direct download links and gdrive

import os
import re
import asyncio
import hashlib
import mimetypes

from time import time
from aiohttp import ClientSession
from aiofiles import open as async_open

from ..helpers.pyros import track_progress


# pre compled regexes for ddl
CMP_GD_QUERY = re.compile(
    r"https://drive\.google\.com/file/d/(.*?)/.*?\?usp=(sharing|drive_link)"
)
STR_GD_REPLACE = r"https://drive.google.com/uc?export=download&id=\1"
DEFAULT_EXT = ".megabot.bin"


class Downloader:
    """
    Download files from urls

    Supports
        - Direct download links
        - Google Drive links (shared files)

    Arguments:
        - `client` - Pyrogram client object
    """

    def __init__(self, client) -> None:
        self.tg_client = client

    async def download(
        self, url: str, path: str, ides: tuple[int, int, int], **kwargs
    ) -> str:
        """
        Download a file from direct / gdrive link

        Arguments:

            - `url` - Url to the file
            - `path` - Output path
            - `ides` - Tuple of ids (chat_id, msg_id, user_id)
        """
        if re.match(CMP_GD_QUERY, url):
            url = await self._parse_gdrive(url)

        # unpack ids
        chat_id, msg_id, user_id = ides

        dl_task = asyncio.create_task(
            self.from_ddl(url=url, path=path, chat_id=chat_id, msg_id=msg_id, **kwargs)
        )
        self.tg_client.ddl_running[user_id] = dl_task
        return await dl_task

    async def _parse_gdrive(self, url: str):
        return re.sub(
            CMP_GD_QUERY,
            STR_GD_REPLACE,
            url,
        )

    async def from_ddl(
        self, url: str, path: str, chat_id: int, msg_id: int, **kwargs
    ) -> str:
        """
        Download files from a direct download link

        Arguments:
            - `url` - Url of the file
            - `path` - Output path
            - `ides` - chat id and message id where the action takes place (chat_id, msg_id)
        """
        # Create folder if it doesn't exist
        wpath = f"{path}/{chat_id}"
        os.makedirs(wpath)

        async with ClientSession() as session:
            _chunksize = int(os.getenv("CHUNK_SIZE"))
            async with session.get(url, timeout=None, allow_redirects=True) as resp:
                # Raise HttpStatusError on failed requests
                if resp.status != 200:
                    raise HttpStatusError(resp.status)

                # Try to get the file name
                cnt_disp = resp.headers.get("Content-Disposition")
                if (
                    cnt_disp
                    and (cd_parts := cnt_disp.split("filename="))
                    and len(cd_parts) > 1
                ):
                    fname = cd_parts[1].strip('\"')

                elif _ftype := mimetypes.guess_type(url):
                    _fext = mimetypes.guess_extension(_ftype)
                    fname = f"{hashlib.md5(url.encode()).hexdigest()}{DEFAULT_EXT if not _fext else _fext}"

                else:
                    fname = os.path.basename(url)

                wpath = f"{wpath}/{fname}"

                # Handle content length header
                total = resp.content_length
                curr = 0
                st = time()
                async with async_open(wpath, mode="wb") as file:
                    async for chunk in resp.content.iter_chunked(_chunksize):
                        await file.write(chunk)
                        curr += len(chunk)
                        # Make sure everything is present before calling track_progress
                        if None not in {chat_id, msg_id, self.tg_client, total}:
                            await track_progress(
                                curr,
                                total,
                                self.tg_client,
                                chat_id,
                                msg_id,
                                st,
                                **kwargs,
                            )

                        await asyncio.sleep(0)
            return wpath


# Exceptions raised by the Downloader class
class InvalidUrl(Exception):
    def __init__(self) -> None:
        super().__init__("The provided string isn't an url!")


class HttpStatusError(Exception):
    def __init__(self, e) -> None:
        super().__init__(f"Request failed with status: {e}")
