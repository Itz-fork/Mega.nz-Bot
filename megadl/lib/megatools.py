# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Helper class for pyrogram bots to interact with megatools cli

import os
import subprocess


from re import search, match
from aiohttp import ClientSession
from megadl.lib.pyros import humanbytes
from megadl.helpers.files import listfiles
from megadl.helpers.sysfncs import run_partial, run_on_shell
from megadl.helpers.crypt import base64_to_a32, base64_url_decode, decrypt_attr


class MegaTools:
    """
    Helper class for pyrogram bots to interact with megatools cli

    Author: https://github.com/Itz-fork
    Project: https://github.com/Itz-fork/Mega.nz-Bot
    """

    def __init__(self, tg_client, pre_conf=None) -> None:
        if pre_conf:
            self.config = f"--config {os.getcwd()}/mega.ini {pre_conf}"
        elif os.getenv("USE_ENV") in ["True", "true"]:
            self.config = "--username $MEGA_EMAIL --password $MEGA_PASSWORD"
        else:
            self.config = f"--config {os.getcwd()}/mega.ini"
        self.client = tg_client

        # regexes
        self.rgx_pubf = r"https?:\/\/mega\.nz\/(file|folder|#)?.+"
        self.rgx_prvf = r"\/Root\/((.*)|([^\s]*))\."

    async def download(
        self,
        url: str,
        chat_id: int,
        message_id: int,
        path: str = "MegaDownloads",
        **kwargs,
    ) -> list:
        """
        Download file/folder from given link

        Arguments:
            - url: string - Mega.nz link of the content
            - chat_id: integer - Telegram chat id of the user
            - message_id: integer - Id of the progress message
            - path (optional): string - Custom path to where the files need to be downloaded
        """
        # Public link download: Supports both file and folders
        if match(self.rgx_pubf, url):
            cmd = f'megadl {self.config} --path "{path}" {url}'

        # Private link downloads: Supports both file and folders
        elif match(self.rgx_prvf, url):
            cmd = f'megaget --no-ask-password {self.config} --path "{path}" {url}'

        else:
            cmd = f'megacopy --no-ask-password {self.config} -l "{path}" -r "{url}" --download'
        await run_partial(
            self.__shellExec, cmd, chat_id=chat_id, msg_id=message_id, **kwargs
        )
        return listfiles(path)

    async def upload(
        self,
        path: str,
        chat_id: int,
        message_id: int,
        to_path: str = "MegaBot",
        **kwargs,
    ) -> str:
        """
        Upload files/folders

        Arguments:

            - path: string - Path to the file or folder
            - chat_id: integer - Telegram chat id of the user
            - message_id: integer - Id of the progress message
            - to_path (optional): string - Custom path to where the files need to be uploaded
        """
        cmd = ""
        # For files
        if os.path.isfile(path):
            cmd = f'megaput {self.config} --disable-previews --no-ask-password --path "/Root/{to_path}/" "{path}"'
        # For folders
        elif os.path.isdir(path):
            cmd = f'megacopy {self.config} --no-ask-password -l "{path}" -r "/Root/{to_path}"'
        else:
            raise UploadFailed(
                self.__genErrorMsg("Given path doesn't belong to a file or folder.")
            )
        # Create remote upload path if it doesn't exist
        if not f"/Root/{to_path}" in (
            await run_partial(run_on_shell, f"megals {self.config} /Root/")
        ):
            await run_partial(
                run_on_shell, f'megamkdir {self.config} "/Root/{to_path}"'
            )
        # Upload
        await run_partial(
            self.__shellExec, cmd, chat_id=chat_id, msg_id=message_id, **kwargs
        )
        # Generate link
        ulink = await run_partial(
            run_on_shell,
            f'megaexport {self.config} "/Root/{to_path}/{os.path.basename(path)}"',
        )
        if not ulink:
            raise UploadFailed(
                self.__genErrorMsg("Upload failed due to an unknown error.")
            )
        return ulink

    @staticmethod
    async def file_info(url: str) -> list[str]:
        """
        Return basic info of a public file

        Arguments:
            - url: string - Mega.nz link of the file
        """
        file_id = None
        file_key = None
        data = None
        # for mega.nz/file/
        if "/file/" in url:
            file_id = search(r"(?<=/file/)(.*)(?=#)", url)[0]
            file_key = search(r"(?<=#)(.*)", url)[0]
        # for mega.nz/#!...!....
        elif "/#!" in url:
            _udta = search(r"(?<=!)(.*)", url)[0].split("!")
            file_id = _udta[0]
            file_key = _udta[1]
        else:
            return "undefined", "undefined"

        async with ClientSession() as session:
            async with session.post(
                "https://g.api.mega.co.nz/cs", json=[{"a": "g", "ad": 1, "p": file_id}]
            ) as resp:
                data = (await resp.json())[0]
        key = base64_to_a32(file_key)
        tk = (key[0] ^ key[4], key[1] ^ key[5], key[2] ^ key[6], key[3] ^ key[7])
        fsize = humanbytes(data["s"])
        fname = decrypt_attr(base64_url_decode(data["at"]), tk)["n"]
        return [fsize, fname]

    def __shellExec(self, cmd: str, chat_id: int = None, msg_id: int = None, **kwargs):
        run = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            encoding="utf-8",
        )
        self.client.mega_running[chat_id] = run.pid

        try:
            # Live process info update
            while run.poll() is None:
                out = run.stdout.readline()
                if out != "":
                    try:
                        self.client.edit_message_text(
                            chat_id, msg_id, f"**Process info:** \n`{out}`", **kwargs
                        )
                    except:
                        pass
        except FileNotFoundError:
            pass
        sh_out = run.stdout.read()[:-1]
        self.__checkErrors(sh_out)
        return sh_out

    def __genErrorMsg(self, bs):
        return f"""
>>> {bs}

Please make sure that you've provided the correct username and password.

You can open a new issue if the problem persists - https://github.com/Itz-fork/Mega.nz-Bot/issues
        """

    def __checkErrors(self, out):
        if "not found" in out:
            raise MegatoolsNotFound

        elif "already exists at" in out:
            pass

        elif "Can't create directory" in out:
            raise UnableToCreateDirectory(
                self.__genErrorMsg(
                    "The program wasn't able to create the directory you requested for."
                )
            )
        elif "No directories specified" in out:
            raise UnableToCreateDirectory(
                self.__genErrorMsg("No directory name was given.")
            )

        elif "Upload failed" in out:
            raise UploadFailed(
                self.__genErrorMsg("Uploading was cancelled due to an (un)known error.")
            )
        elif "No files specified for upload" in out:
            raise UploadFailed(
                self.__genErrorMsg(
                    "Path to the file which need to be uploaded wasn't provided"
                )
            )

        elif "Can't login to mega.nz" in out:
            raise LoginError

        elif "ERROR" in out:
            raise UnknownError(
                self.__genErrorMsg("Operation cancelled due to an unknown error.")
            )
        else:
            return


# Errors
class MegatoolsNotFound(Exception):
    def __init__(self) -> None:
        super().__init__(
            "'megatools' cli is not installed in this system. You can download it at - https://megatools.megous.com/"
        )


class LoginError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Unable to login to your mega.nz account. \n\nYou can open a new issue if the problem persists - https://github.com/Itz-fork/Mega.nz-Bot/issues"
        )


class UnableToCreateDirectory(Exception):
    def __init__(self, e) -> None:
        super().__init__(e)


class UploadFailed(Exception):
    def __init__(self, e) -> None:
        super().__init__(e)


class UnknownError(Exception):
    def __init__(self, e) -> None:
        super().__init__(e)
