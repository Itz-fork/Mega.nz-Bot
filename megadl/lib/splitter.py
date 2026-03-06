# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Optimized async file splitter for resource-constrained environments

import os
import asyncio
from os import path, makedirs


# Default split size: ~2GB (Telegram's file limit)
DEFAULT_SPLIT_SIZE = 2040108421
# Buffer size: 1MB - good balance between memory and I/O performance
DEFAULT_BUFFER_SIZE = 1024 * 1024


async def split_file(
    input_path: str,
    output_dir: str,
    split_size: int = DEFAULT_SPLIT_SIZE,
    buffer_size: int = DEFAULT_BUFFER_SIZE,
) -> list[str]:
    """
    Split a file into smaller chunks asynchronously with minimal memory footprint.
    
    Designed to handle thousands of simultaneous connections efficiently by:
    - Using buffered reading to minimize memory usage
    - Running blocking I/O in thread pool to avoid blocking event loop
    - Yielding control periodically to allow other tasks to run
    
    Arguments:
        input_path: Path to the file to split
        output_dir: Directory to save split files
        split_size: Maximum size of each split file in bytes (default: ~2GB)
        buffer_size: Buffer size for reading/writing (default: 1MB)
    
    Returns:
        List of paths to the split files
    """
    if not path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if not path.isdir(output_dir):
        makedirs(output_dir)
    
    file_size = os.stat(input_path).st_size
    
    # If file is smaller than split size, no need to split
    if file_size <= split_size:
        return [input_path]
    
    base_name = path.basename(input_path)
    split_files = []
    
    # Run the actual splitting in a thread pool to avoid blocking
    loop = asyncio.get_running_loop()
    split_files = await loop.run_in_executor(
        None,
        _sync_split,
        input_path,
        output_dir,
        base_name,
        file_size,
        split_size,
        buffer_size,
    )
    
    return split_files


def _sync_split(
    input_path: str,
    output_dir: str,
    base_name: str,
    file_size: int,
    split_size: int,
    buffer_size: int,
) -> list[str]:
    """
    Synchronous file splitting implementation.
    
    This runs in a thread pool to avoid blocking the async event loop.
    Uses buffered I/O to minimize memory usage even with large files.
    """
    split_files = []
    part_num = 1
    bytes_remaining = file_size
    
    with open(input_path, "rb") as infile:
        while bytes_remaining > 0:
            # Calculate how many bytes to write to this part
            part_size = min(split_size, bytes_remaining)
            part_path = path.join(output_dir, f"{base_name}.part{part_num:03d}")
            split_files.append(part_path)
            
            bytes_written = 0
            with open(part_path, "wb") as outfile:
                while bytes_written < part_size:
                    # Read in chunks to minimize memory usage
                    to_read = min(buffer_size, part_size - bytes_written)
                    chunk = infile.read(to_read)
                    if not chunk:
                        break
                    outfile.write(chunk)
                    bytes_written += len(chunk)
            
            bytes_remaining -= bytes_written
            part_num += 1
    
    return split_files


async def get_split_count(file_path: str, split_size: int = DEFAULT_SPLIT_SIZE) -> int:
    """
    Calculate how many parts a file would be split into.
    
    Arguments:
        file_path: Path to the file
        split_size: Size of each split in bytes
    
    Returns:
        Number of parts the file would be split into
    """
    if not path.isfile(file_path):
        return 0
    
    file_size = os.stat(file_path).st_size
    return (file_size + split_size - 1) // split_size
