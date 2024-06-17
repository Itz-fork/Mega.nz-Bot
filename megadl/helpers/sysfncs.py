# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Shell, loops and other sys functions

import asyncio

from functools import partial
from subprocess import Popen, PIPE
from psutil import Process as psu_proc
from asyncio import iscoroutinefunction, get_running_loop


async def run_partial(func, *args, **kwargs):
    """
    Run synchronous functions in a non-blocking coroutine and return the result

    - Arguments:
        - func: function - Function to execute

    - Note:
        Used for CPU-bound tasks or blocking IO that can't be handled efficiently with asyncio's non-blocking IO.
    """
    if iscoroutinefunction(func):
        return await func(*args, **kwargs)
    else:
        loop = get_running_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))


def run_on_shell(cmd: str):
    """
    Run shell commands and get it's output

    - Arguments:
        - cmd: str - Command to execute
    """
    run = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    shout = run.stdout.read()[:-1].decode("utf-8")
    return shout


async def with_sub_shell(cmd: str, **kwargs):
    """
    Run shell commands and get it's output

    - Arguments:
        - cmd: str - Command to execute

    - Note:
        Creates a subprocess using asyncio.create_subprocess_shell
        Not suitable for heavy IO bound tasks (use run_on_shell with run_partial for that)
    """
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, **kwargs
    )

    stdout, stderr = await process.communicate()

    if stdout:
        return stdout[:-1].decode("utf-8")
    if stderr:
        return stderr[:-1].decode("utf-8")


async def kill_family(pid: int):
    """
    Murder a process and it's whole family using pid
    """
    running = psu_proc(pid)
    for child in running.children(recursive=True):
        child.kill()
    running.kill()
    await asyncio.to_thread(running.wait)
