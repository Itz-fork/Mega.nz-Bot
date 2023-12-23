# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Helper class for downloading direct download links

import os
from time import time
from re import match, sub
from aiofiles import open as async_open
from aiohttp import ClientSession

from .pyros import track_progress


class Downloader:
    """
    Download files from urls

    Supports
        - Direct download links
        - Google Drive links (shared files)
    """

    def __init__(self) -> None:
        self.gdrive_regex = r"https://drive\.google\.com/file/d/(.*?)/.*?\?usp=sharing"

    async def download(self, url: str, path: str, client, ides: tuple[int, int]) -> str:
        """
        Download a file from direct / gdrive link

        Parameters:

            - `url` - Url to the file
            - `path` - Output path
            - `client` - Pyrogram client object
            - `ides` - Tuple of ids (chat_id, msg_id)
        """
        if match(self.gdrive_regex, url):
            gurl = await self._parse_gdrive(url)
            return await self.from_ddl(url=gurl, path=path, client=client, ides=ides)
        else:
            return await self.from_ddl(url=url, path=path, client=client, ides=ides)

    async def _parse_gdrive(self, url: str):
        return sub(
            r"https://drive\.google\.com/file/d/(.*?)/.*?\?usp=sharing",
            r"https://drive.google.com/uc?export=download&id=\1",
            url,
        )

    async def from_ddl(self, url: str, path: str, client, ides: tuple[int, int]) -> str:
        """
        Download files from a direct download link

        Arguments:
            - `url` - Url of the file
            - `path` - Output path
            - `client` - Pyrogram client object
            - `ides` - chat id and message id where the action takes place (chat_id, msg_id)
        """
        # Create folder if it doesn't exist
        wpath = f"{path}/{ides[0]}"
        os.makedirs(wpath)
        wpath = f"{wpath}/{os.path.basename(url)}"

        async with ClientSession() as session:
            async with session.get(url, timeout=None, allow_redirects=True) as resp:
                # Raise HttpStatusError on failed requests
                if resp.status != 200:
                    raise HttpStatusError(resp.status)
                # Handle content length header
                total = resp.content_length
                curr = 0
                st = time()
                async with async_open(wpath, mode="wb") as file:
                    async for chunk in resp.content.iter_chunked(
                        int(os.getenv("CHUNK_SIZE"))
                    ):
                        await file.write(chunk)
                        curr += len(chunk)
                        # Make sure everything is present before calling track_progress
                        if None not in {ides, client, total}:
                            await track_progress(curr, total, client, ides, st)
            return wpath


# Exceptions raised by the Downloader class
class InvalidUrl(Exception):
    def __init__(self) -> None:
        super().__init__("The provided string isn't an url!")


class HttpStatusError(Exception):
    def __init__(self, e) -> None:
        super().__init__(f"Request failed with status: {e}")
