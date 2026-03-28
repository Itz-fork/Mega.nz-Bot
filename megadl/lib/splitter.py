# Copyright (c) 2021 - Present partiallywritten
# Author: https://github.com/partiallywritten
# Project: https://github.com/partiallywritten/Mega.nz-Bot
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

    makedirs(output_dir, exist_ok=True)

    file_size = os.stat(input_path).st_size

    if file_size <= split_size:
        return [input_path]

    base_name = path.basename(input_path)

    return await asyncio.to_thread(
        _sync_split,
        input_path,
        output_dir,
        base_name,
        file_size,
        split_size,
        buffer_size,
    )


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
    """

    num_parts = (file_size + split_size - 1) // split_size
    split_files = [None] * num_parts
    use_sendfile = hasattr(os, "sendfile")

    with open(input_path, "rb") as infile:
        infile_fd = infile.fileno()

        for part_index in range(num_parts):
            part_num = part_index + 1
            part_size = min(split_size, file_size - part_index * split_size)
            part_path = path.join(output_dir, f"{base_name}.part{part_num:03d}")
            split_files[part_index] = part_path

            with open(part_path, "wb") as outfile:
                outfile_fd = outfile.fileno()
                if use_sendfile:
                    offset = infile.tell()
                    remaining = part_size

                    while remaining > 0:
                        sent = os.sendfile(outfile_fd, infile_fd, offset, remaining)
                        if sent == 0:
                            break
                        offset += sent
                        remaining -= sent
                    infile.seek(offset)

                else:
                    # fallback buffered copy
                    bytes_written = 0

                    while bytes_written + buffer_size <= part_size:
                        outfile.write(infile.read(buffer_size))
                        bytes_written += buffer_size

                    remaining = part_size - bytes_written
                    if remaining:
                        outfile.write(infile.read(remaining))

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
