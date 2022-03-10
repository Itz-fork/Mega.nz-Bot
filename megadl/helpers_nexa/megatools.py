# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae

import os
import subprocess

from config import Config

class MegaTools:
    """
    Helper class to interact with megatools cli
    """

    def __init__(self) -> None:
        self.u = Config.MEGA_EMAIL
        self.p = Config.MEGA_PASSWORD
    
    async def __runCommands(self, cmd):
        run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        shell_ouput = run.stdout.read()[:-1].decode("utf-8")
        cc = await self.__checkErrors(shell_ouput)
        if cc == "retry":
            return await self.__runCommands(cmd)
        return shell_ouput

    async def __isFile(self, path):
        return os.path.isfile(path)
    
    async def __genErrorMsg(self, bs):
        return f"""
>>> {bs}

Please make sure that you've provided the correct username and password.

You can open a new issue if the problem persists - https://github.com/Itz-fork/Mega.nz-Bot/issues
        """

    async def __checkErrors(self, out):
        if "Parent directory doesn't exist" in out:
            await self.makeDir("MegaBot")
            return "retry"
        
        elif "Can't create directory" in out:
            raise UnableToCreateDirectory(await self.__genErrorMsg("The program wasn't able to create the directory you requested for."))
        elif "No directories specified" in out:
            raise UnableToCreateDirectory(await self.__genErrorMsg("No directory name was given."))
        
        elif "Upload failed" in out:
            raise UploadFailed(await self.__genErrorMsg("Uploading was cancelled due to an (un)known error."))
        elif "No files specified for upload" in out:
            raise UploadFailed(await self.__genErrorMsg("Path to the file which need to be uploaded wasn't provided"))

        elif "Can't login to mega.nz" in out:
            raise LoginError(await self.__genErrorMsg("Unable to login to your mega.nz account."))
        
        elif "ERROR" in out:
            raise UnknownError(await self.__genErrorMsg("Operation cancelled due to an unknown error."))
        
        else:
            return True


    async def makeDir(self, path):
        cmd = f"megatools mkdir -u {self.u} -p {self.p} /Root/{path}"
        await self.__runCommands(cmd)

    async def upload(self, path):
        if not self.__isFile(path):
            raise UploadFailed(await self.__genErrorMsg("Given path isn't belong to a file."))
        ucmd = f"megatools put -u {self.u} -p {self.p} --no-progress --disable-previews --no-ask-password --path /Root/MegaBot {path}"
        await self.__runCommands(ucmd)
        lcmd = f"megatools export -u {self.u} -p {self.p} /Root/MegaBot/{path}"
        return await self.__runCommands(lcmd)



# Errors

class UnableToCreateDirectory(Exception):
    pass

class UploadFailed(Exception):
    pass

class LoginError(Exception):
    pass

class UnknownError(Exception):
    pass