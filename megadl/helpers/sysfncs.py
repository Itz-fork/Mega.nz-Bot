# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Contains functions related to shell, async execution


from functools import partial
from subprocess import Popen, PIPE
from psutil import Process as PsuPrc
from asyncio import get_running_loop


async def run_partial(func, *args, **kwargs):
    """
    Run synchronous functions in a non-blocking coroutine and return the result

    Arguments:

        - func: function - Function to execute
    """
    loop = get_running_loop()
    return await loop.run_in_executor(None, partial(func, *args, **kwargs))


def run_on_shell(cmd):
    """
    Run shell commands and get it's output
    """
    run = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    shout = run.stdout.read()[:-1].decode("utf-8")
    return shout


async def kill_family(pid: int):
    """
    Murder a process and it's whole family using pid
    """
    running = PsuPrc(pid)
    for child in running.children(recursive=True):
        child.kill()
    running.kill()
