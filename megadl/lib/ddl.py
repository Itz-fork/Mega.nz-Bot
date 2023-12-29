# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Downloader for direct download links and gdrive

import os
import asyncio

from time import time
from re import match, sub
from aiohttp import ClientSession
from aiofiles import open as async_open

from ..helpers.pyros import track_progress


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
        self.gdrive_regex = r"https://drive\.google\.com/file/d/(.*?)/.*?\?usp=sharing"
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
        if match(self.gdrive_regex, url):
            url = await self._parse_gdrive(url)

        dl_task = asyncio.create_task(
            self.from_ddl(url=url, path=path, ides=(ides[0], ides[1]), **kwargs)
        )
        self.tg_client.ddl_running[ides[2]] = dl_task
        return await dl_task

    async def _parse_gdrive(self, url: str):
        return sub(
            r"https://drive\.google\.com/file/d/(.*?)/.*?\?usp=sharing",
            r"https://drive.google.com/uc?export=download&id=\1",
            url,
        )

    async def from_ddl(
        self, url: str, path: str, ides: tuple[int, int], **kwargs
    ) -> str:
        """
        Download files from a direct download link

        Arguments:
            - `url` - Url of the file
            - `path` - Output path
            - `ides` - chat id and message id where the action takes place (chat_id, msg_id)
        """
        # Create folder if it doesn't exist
        wpath = f"{path}/{ides[0]}"
        os.makedirs(wpath)
        wpath = f"{wpath}/{os.path.basename(url)}"

        async with ClientSession() as session:
            _chunksize = int(os.getenv("CHUNK_SIZE"))
            async with session.get(url, timeout=None, allow_redirects=True) as resp:
                # Raise HttpStatusError on failed requests
                if resp.status != 200:
                    raise HttpStatusError(resp.status)
                # Handle content length header
                total = resp.content_length
                curr = 0
                st = time()
                async with async_open(wpath, mode="wb") as file:
                    async for chunk in resp.content.iter_chunked(_chunksize):
                        await file.write(chunk)
                        curr += len(chunk)
                        # Make sure everything is present before calling track_progress
                        if None not in {ides, self.tg_client, total}:
                            await track_progress(
                                curr, total, self.tg_client, ides, st, **kwargs
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
