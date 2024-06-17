# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Wrapper for megatools cli with extended features

import os
import re
import json
import logging
import asyncio

from humans import human_bytes
from aiohttp import ClientSession
from megadl.helpers.files import listfiles
from megadl.helpers.sysfncs import run_partial, run_on_shell, with_sub_shell
from megadl.helpers.crypt import (
    base64_to_a32,
    decrypt_attr,
    decrypt_node_key,
    base64_url_decode,
)


# regexes
class MegaRegexs:
    pub_file_folder = re.compile(r"https?:\/\/mega\.nz\/(file|folder|#)?.+")
    prv_file_folder = re.compile(r"\/Root\/((.*)|([^\s]*))\.")

    pub_file = re.compile(
        r"https://mega.nz/(?:file/([0-z-_]+)#|#!([0-z-_]+)!)([0-z-_]+)"
    )
    pub_folder = re.compile(
        r"mega.[^/]+/(?:folder/([0-z-_]+)#|(?:(?:#F!([0-z-_]+))[!#]))([0-z-_]+)(?:/folder/([0-z-_]+))*"
    )

    file_id = re.compile(r"(?<=/file/)(.*)(?=#)")
    file_key = re.compile(r"(?<=#)(.*)")
    old_f_ik = re.compile(r"(?<=!)(.*)")

    user_total = re.compile(r"Total: (.*)")
    user_used = re.compile(r"Used: (.*)")
    user_free = re.compile(r"Free: (.*)")

    proxy_regex = re.compile(r'^(http|https|socks5|socks5h)://([a-zA-Z0-9\-\.]+):(\d+)$')


Regexes = MegaRegexs()


class MegaTools:
    """
    Helper class for pyrogram bots to interact with megatools cli

    Author: https://github.com/Itz-fork
    Project: https://github.com/Itz-fork/Mega.nz-Bot
    """

    def __init__(self, tg_client, pre_conf=None) -> None:
        if pre_conf:
            self.config = f"--config {tg_client.cwd}/mega.ini {pre_conf}"
        elif os.getenv("USE_ENV") in ["True", "true"]:
            self.config = "--username $MEGA_EMAIL --password $MEGA_PASSWORD"
        elif os.path.isfile(f"{tg_client.cwd}/mega.ini"):
            self.config = f"--config {tg_client.cwd}/mega.ini"
        else:
            self.config = ""
        self.client = tg_client

    async def download(
        self,
        url: str,
        user_id: int,
        chat_id: int,
        message_id: int,
        path: str = "MegaDownloads",
        **kwargs,
    ) -> list:
        """
        Download file/folder from given link

        Arguments:
            - url: string - Mega.nz link of the content
            - user_id: integer - Telegram user id of the user
            - chat_id: integer - Telegram chat id of the user
            - message_id: integer - Id of the progress message
            - path (optional): string - Custom path to where the files need to be downloaded
        """
        # Public link download: Supports both file and folders
        if Regexes.pub_file_folder.match(url):
            cmd = f'megadl {self.config} --path "{path}" {url}'

        # Private link downloads: Supports both file and folders
        elif Regexes.prv_file_folder.match(url):
            cmd = f'megaget --no-ask-password {self.config} --path "{path}" {url}'

        else:
            cmd = f'megacopy --no-ask-password {self.config} -l "{path}" -r "{url}" --download'
        await run_partial(
            self.__shellExec,
            cmd,
            user_id=user_id,
            chat_id=chat_id,
            msg_id=message_id,
            **kwargs,
        )
        return listfiles(path)

    async def upload(
        self,
        path: str,
        user_id: int,
        chat_id: int,
        message_id: int,
        to_path: str = "MegaBot",
        **kwargs,
    ) -> str:
        """
        Upload files/folders

        Arguments:

            - path: string - Path to the file or folder
            - user_id: integer - Telegram user id of the user
            - chat_id: integer - Telegram chat id of the process (could be either private or group id)
            - message_id: integer - Id of the progress message
            - to_path (optional): string - Custom path to where the files need to be uploaded
        """
        cmd = ""
        # check if the file is already present
        


        
        # For files
        if os.path.isfile(path):
            cmd = f'megaput {self.config} --no-ask-password --path "/Root/{to_path}/" "{path}"'
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
            self.__shellExec,
            cmd,
            user_id=user_id,
            chat_id=chat_id,
            msg_id=message_id,
            **kwargs,
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

    async def user_fs(self):
        """ """
        _sh_dta = await with_sub_shell(f"megadf -h {self.config}")
        if _sh_dta:
            _total = Regexes.user_total.search(_sh_dta).group(1)
            _used = Regexes.user_used.search(_sh_dta).group(1)
            _free = Regexes.user_free.search(_sh_dta).group(1)
            return _total, _used, _free
        else:
            raise LoginError

    @staticmethod
    async def get_info(url: str) -> list[str]:
        """
        Return basic info of a public file/folder

        Arguments:
            - url: string - Mega.nz link of the file / folder

        Returns:
            - File:
                - (file_size, file_name)

            - Folder:
                - string of all the files and sub dirs in the url

            - Otherwise:
                - (undefined, undefined)
        """
        is_file = Regexes.pub_file.search(url)
        is_folder = Regexes.pub_folder.search(url)

        if is_file:
            file_id = None
            file_key = None
            data = None
            # for mega.nz/file/
            if "/file/" in url:
                file_id = Regexes.file_id.search(url)[0]
                file_key = Regexes.file_key.search(url)[0]
            # for mega.nz/#!...!....
            elif "/#!" in url:
                file_id, file_key = Regexes.old_f_ik.search(url)[0].split("!")
            else:
                return "undefined", "undefined"

            async with ClientSession() as session:
                async with session.post(
                    "https://g.api.mega.co.nz/cs",
                    json=[{"a": "g", "ad": 1, "p": file_id}],
                ) as resp:
                    data = (await resp.json())[0]
            key = base64_to_a32(file_key)
            tk = (key[0] ^ key[4], key[1] ^ key[5], key[2] ^ key[6], key[3] ^ key[7])
            fsize = human_bytes(data["s"])
            fname = decrypt_attr(base64_url_decode(data["at"]), tk)["n"]
            return [fsize, fname]

        elif is_folder:
            root_folder, shared_enc_key = tuple(
                [x for x in is_folder.groups() if x is not None]
            )
            shared_key = base64_to_a32(shared_enc_key)

            # get nodes in a the folder
            nodes = None
            data = [{"a": "f", "c": 1, "ca": 1, "r": 1}]
            # print(nodes)
            session = ClientSession()
            resp = await session.post(
                "https://g.api.mega.co.nz/cs",
                params={"id": 0, "n": root_folder},
                data=json.dumps(data),
            )
            nodes = (await resp.json())[0]["f"]

            if not nodes:
                return "undefined", "undefined"

            # get nodes in a sub dir
            async def get_sub_dir_nodes(root_folder, sub_dir):
                resp = await session.post(
                    "https://g.api.mega.co.nz/cs",
                    params={"id": 0, "n": root_folder},
                    data=json.dumps(data),
                )
                json_resp = await resp.json()
                if (
                    isinstance(json_resp, list)
                    and isinstance(json_resp[0], dict)
                    and "f" in json_resp[0]
                ):
                    all_nodes = json_resp[0]["f"]
                    sub_dir_nodes = [node for node in all_nodes if node["p"] == sub_dir]
                    return sub_dir_nodes
                else:
                    return []

            # make string
            to_return = ""
            num = 1

            async def prepare_string(nodes, shared_key, depth=0):
                nonlocal to_return
                nonlocal num
                for node in nodes:
                    key = decrypt_node_key(node["k"], shared_key)
                    file_id = node["h"]
                    if key:
                        file_size = node["s"] if "s" in node else ""
                        if node["t"] == 0:  # file
                            k = (
                                key[0] ^ key[4],
                                key[1] ^ key[5],
                                key[2] ^ key[6],
                                key[3] ^ key[7],
                            )
                            attrs = decrypt_attr(base64_url_decode(node["a"]), k)
                            file_name = attrs["n"]
                            to_return += f"{' ' * depth}├── {file_name} ({human_bytes(file_size)})\n"
                        elif node["t"] == 1:  # folder
                            k = key
                            attrs = decrypt_attr(base64_url_decode(node["a"]), k)
                            file_name = attrs["n"]
                            to_return += f"{' ' * depth}├─ {file_name}\n"
                            await prepare_string(
                                await get_sub_dir_nodes(root_folder, file_id),
                                shared_key,
                                depth + 1,
                            )
                    if len(nodes) == num:
                        break
                    num += 1

            await prepare_string(nodes, shared_key)
            await session.close()
            return to_return

        else:
            return "undefined", "undefined"

    async def __shellExec(
        self, cmd: str, user_id: int, chat_id: int = None, msg_id: int = None, **kwargs
    ):
        run = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=self.client.environs,
        )
        self.client.mega_running[user_id] = run.pid

        async def read_stream(stream, handler):
            while True:
                line = await stream.readline()
                if line:
                    await handler(
                        line.decode("utf-8") if isinstance(line, bytes) else line
                    )
                else:
                    break

        async def handle_stdout(out):
            try:
                await self.client.edit_message_text(
                    chat_id, msg_id, f"**Process info:** \n`{out}`", **kwargs
                )
            except Exception as e:
                logging.warning(e)

        async def handle_stderr(err):
            if run.returncode is None:
                await self.__checkErrors(err)

        stdout = read_stream(run.stdout, handle_stdout)
        stderr = read_stream(run.stderr, handle_stderr)

        try:
            await asyncio.gather(stdout, stderr)
        except asyncio.CancelledError:
            asyncio.create_task(self.__terminate_sub(run))

        await run.wait()

    async def __terminate_sub(run):
        run.terminate()
        await run.wait()

    def __genErrorMsg(self, bs):
        return f"""
>>> {bs}

Please make sure that you've provided the correct username and password.

You can open a new issue if the problem persists - https://github.com/Itz-fork/Mega.nz-Bot/issues
        """

    async def __checkErrors(self, out):
        if "command not found" in out:
            raise MegatoolsNotFound()

        elif "Remote directory not found" in out:
            raise RemoteContentNotFound()

        elif "File already exists" in out:
            raise FileAlreadyExists()

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


class RemoteContentNotFound(Exception):
    def __init__(self) -> None:
        super().__init__(
            "The file or folder you're trying to download doesn't exist in your account"
        )


class FileAlreadyExists(Exception):
    def __init__(self) -> None:
        super().__init__(
            "File you're trying to upload already exists in your account under 'MegaBot' folder"
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
