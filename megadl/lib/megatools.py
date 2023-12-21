# @Author: https://github.com/Itz-fork
# @Project: https://github.com/Itz-fork/Mega.nz-Bot
# @Version: nightly-0.2
# @Description: Helper class for pyrogram bots to interact with megatools cli

import os
import subprocess

from re import match
from megadl.helpers.files import listfiles
from megadl.helpers.cors import run_partial, run_on_shell


class MegaTools:
    """
    Helper class for pyrogram bots to interact with megatools cli

    Author: https://github.com/Itz-fork
    Project: https://github.com/Itz-fork/Mega.nz-Bot
    """

    def __init__(self, tg_client) -> None:
        if os.getenv("USE_ENV"):
            self.config = "--username $MEGA_EMAIL --password $MEGA_PASSWORD"
        else:
            self.config = f"--config {os.getcwd()}/mega.ini"
        self.client = tg_client

    async def download(
        self,
        url: str,
        chat_id: int,
        message_id: int,
        path: str = "MegaDownloads",
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
        if match(r"https?:\/\/mega\.nz\/(file|folder|#)?.+", url):
            cmd = f'megadl {self.config} --path "{path}" {url}'

        # Private link downloads: Supports both file and folders
        elif match(r"\/Root\/((.*)|([^\s]*))\.", url):
            cmd = f'megaget --no-ask-password {self.config} --path "{path}" {url}'
        else:
            cmd = f'megacopy --no-ask-password {self.config} -l "{path}" -r "{url}" --download'
        await run_partial(self.__shellExec, cmd, chat_id=chat_id, msg_id=message_id)
        return listfiles(path)

    async def upload(
        self, path: str, chat_id: int, message_id: int, to_path: str = "MegaBot"
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
            if not os.path.isfile(path):
                raise UploadFailed(
                    self.__genErrorMsg("Given path doesn't belong to a file.")
                )
            cmd = f'megaput {self.config} --disable-previews --no-ask-password --path "/Root/{to_path}" "{path}"'
        # For folders
        if os.path.isdir(path):
            if not os.path.isdir(path):
                raise UploadFailed(
                    self.__genErrorMsg("Given path doesn't belong to a folder.")
                )
            cmd = f'megacopy {self.config} --no-ask-password -l "{path}" -r "/Root/{to_path}"'
        # Create remote upload path if it doesn't exist
        if not f"/Root/{to_path}" in (
            await run_partial(run_on_shell, f"megals {self.config} /Root/")
        ):
            await run_partial(
                run_on_shell, f'megamkdir {self.config} "/Root/{to_path}"'
            )
        # Upload
        await run_partial(self.__shellExec, cmd, chat_id=chat_id, msg_id=message_id)
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

    def __shellExec(self, cmd: str, chat_id: int = None, msg_id: int = None):
        print(cmd)
        run = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            encoding="utf-8",
        )
        try:
            # Live process info update
            while run.poll() is None:
                out = run.stdout.readline()
                if out != "":
                    self.client.edit_message_text(
                        chat_id, msg_id, f"**Process info:** \n`{out}`"
                    )
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
