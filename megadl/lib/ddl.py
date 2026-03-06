# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Downloader for direct download links and gdrive
# Optimized for handling thousands of simultaneous connections

import os
import re
import asyncio
import hashlib
import mimetypes

from time import time
from aiohttp import ClientSession, TCPConnector, ClientTimeout
from aiofiles import open as async_open

from ..helpers.pyros import track_progress


# pre compiled regexes for ddl
CMP_GD_QUERY = re.compile(
    r"https://drive\.google\.com/file/d/(.*?)/.*?\?usp=(sharing|drive_link)"
)
STR_GD_REPLACE = r"https://drive.google.com/uc?export=download&id=\1"
DEFAULT_EXT = ".megabot.bin"
# Default chunk size in bytes (512KB) - balances memory usage and download speed
DEFAULT_CHUNK_SIZE = 524288
# Connection pool limits for resource-constrained environments
DEFAULT_POOL_LIMIT = 100  # Max simultaneous connections per host
DEFAULT_TOTAL_LIMIT = 500  # Max total connections


class Downloader:
    """
    Download files from urls
    
    Optimized for resource-constrained environments handling thousands of connections:
    - Connection pooling via shared ClientSession with configurable limits
    - Efficient memory usage with streaming downloads
    - Non-blocking I/O with proper async patterns

    Supports
        - Direct download links
        - Google Drive links (shared files)

    Arguments:
        - `client` - Pyrogram client object
    """
    
    # Shared connector for connection pooling across all Downloader instances
    _connector = None
    _session = None
    _lock = asyncio.Lock()

    def __init__(self, client) -> None:
        self.tg_client = client

    @classmethod
    async def get_session(cls) -> ClientSession:
        """
        Get or create a shared session with connection pooling.
        
        Uses a shared connector to efficiently manage connections across
        all download instances, reducing memory overhead and connection setup time.
        """
        async with cls._lock:
            if cls._session is None or cls._session.closed:
                # Configure connector for high concurrency with resource limits
                pool_limit = int(os.getenv("DDL_POOL_LIMIT", str(DEFAULT_POOL_LIMIT)))
                total_limit = int(os.getenv("DDL_TOTAL_LIMIT", str(DEFAULT_TOTAL_LIMIT)))
                
                cls._connector = TCPConnector(
                    limit_per_host=pool_limit,
                    limit=total_limit,
                    ttl_dns_cache=300,  # Cache DNS for 5 minutes
                    enable_cleanup_closed=True,  # Clean up closed connections
                )
                
                # Create session with reasonable timeouts
                timeout = ClientTimeout(
                    total=None,  # No total timeout for large downloads
                    connect=30,  # 30 seconds to establish connection
                    sock_read=60,  # 60 seconds between reads
                )
                
                cls._session = ClientSession(
                    connector=cls._connector,
                    timeout=timeout,
                )
            
            return cls._session

    @classmethod
    async def close_session(cls):
        """Close the shared session and connector."""
        async with cls._lock:
            if cls._session and not cls._session.closed:
                await cls._session.close()
                cls._session = None
            if cls._connector and not cls._connector.closed:
                await cls._connector.close()
                cls._connector = None

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
        
        Optimized for minimal memory usage and maximum concurrency:
        - Uses shared connection pool
        - Streams directly to disk without loading entire file in memory
        - Yields control to event loop periodically

        Arguments:
            - `url` - Url of the file
            - `path` - Output path
            - `chat_id` - Chat id where the action takes place
            - `msg_id` - Message id for progress updates
        """
        # Create folder if it doesn't exist
        wpath = f"{path}/{chat_id}"
        os.makedirs(wpath, exist_ok=True)

        session = await self.get_session()
        _chunksize = int(os.getenv("CHUNK_SIZE", str(DEFAULT_CHUNK_SIZE)))
        
        async with session.get(url, allow_redirects=True) as resp:
            # Raise HttpStatusError on failed requests
            if resp.status != 200:
                raise HttpStatusError(resp.status)

            # Try to get the file name
            fname = self._extract_filename(resp, url)
            wpath = f"{wpath}/{fname}"

            # Handle content length header
            total = resp.content_length
            curr = 0
            st = time()
            
            # Stream directly to file for memory efficiency
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
                    
                    # Yield control to allow other tasks to run
                    await asyncio.sleep(0)
        
        return wpath

    def _extract_filename(self, resp, url: str) -> str:
        """Extract filename from response headers or URL."""
        # Try Content-Disposition header first
        cnt_disp = resp.headers.get("Content-Disposition")
        if cnt_disp:
            cd_parts = cnt_disp.split("filename=")
            if len(cd_parts) > 1:
                return cd_parts[1].strip('\"')

        # Try to guess from mime type
        ftype = mimetypes.guess_type(url)
        if ftype and ftype[0]:
            fext = mimetypes.guess_extension(ftype[0])
            return f"{hashlib.md5(url.encode()).hexdigest()}{DEFAULT_EXT if not fext else fext}"

        # Fall back to URL basename
        return os.path.basename(url) or f"{hashlib.md5(url.encode()).hexdigest()}{DEFAULT_EXT}"


# Exceptions raised by the Downloader class
class InvalidUrl(Exception):
    def __init__(self) -> None:
        super().__init__("The provided string isn't an url!")


class HttpStatusError(Exception):
    def __init__(self, e) -> None:
        super().__init__(f"Request failed with status: {e}")
