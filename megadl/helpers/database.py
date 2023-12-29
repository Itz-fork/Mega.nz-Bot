# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Database functions

from megadl.lib.aiomongo import AioMongo


class Users:
    def __init__(self) -> None:
        self.mongoc = AioMongo()
        self.coll_users = self.mongoc["mega_nz"]["users"]

    # <<<<<<<<<< Active user functions >>>>>>>>>> #

    async def add(self, user_id: int):
        added = await self.is_there(user_id)
        if not added:
            await self.mongoc.insert_async(
                self.coll_users,
                {
                    "_id": user_id,
                    "email": "",
                    "password": "",
                    "status": {"banned": False, "reason": ""},
                    "total_downloads": 0,
                    "total_uploads": 0,
                },
            )

    async def plus_fl_count(
        self, user_id: int, downloads: int | None = None, uploads: int | None = None
    ):
        dl_up = await self.is_there(user_id)
        if downloads:
            await self.mongoc.update_async(
                self.coll_users,
                {"_id": user_id},
                {"total_downloads": dl_up["total_downloads"] + downloads},
            )
        elif uploads:
            await self.mongoc.update_async(
                self.coll_users,
                {"_id": user_id},
                {"total_uploads": dl_up["total_uploads"] + uploads},
            )

    async def delete(self, user_id: int):
        uid = {"_id": user_id}
        added = await self.is_there(self.coll_users, user_id)
        if added:
            await self.mongoc.delete_async(self.coll_users, uid)

    async def is_there(self, user_id: int, use_acc: bool = False):
        """
        Returns:
            {
                "email": "",
                "password": "",
                "status": {"banned": False, "reason": ""},
                "total_downloads": 0,
                "total_uploads": 0,
            }
        """
        uid = {"_id": user_id}
        docu = await self.mongoc.find_async(self.coll_users, uid)
        if not docu:
            return None
        docu.pop("_id")
        if use_acc:
            return docu if not "" in docu.values() else None
        else:
            return docu

    # <<<<<<<<<< Banned user functions >>>>>>>>>> #
    async def ban_user(self, user_id: int, reason: str):
        uid = {"_id": user_id}
        to_ban = await self.mongoc.find_async(self.coll_users, uid)
        if to_ban:
            await self.mongoc.update_async(
                self.coll_users,
                {"_id": user_id},
                {"status": {"banned": True, "reason": reason}},
            )

    async def unban_user(self, user_id: int):
        uid = {"_id": user_id}
        to_ban = await self.mongoc.find_async(self.coll_users, uid)
        if to_ban:
            await self.mongoc.update_async(
                self.coll_users,
                {"_id": user_id},
                {"status": {"banned": False, "reason": "Got unbanned"}},
            )

    # <<<<<<<<<< Mega functions >>>>>>>>>> #

    async def mega_login(self, user_id: int, email: str, password: str):
        uid = {"_id": user_id}
        logged = await self.mongoc.find_async(self.coll_users, uid)
        if logged:
            await self.mongoc.update_async(
                self.coll_users, uid, {"email": email, "password": password}
            )
        # this should never happen but better safe than sorry
        else:
            await self.mongoc.insert_async(
                self.coll_users, {"_id": user_id, "email": email, "password": password}
            )

    async def mega_logout(self, user_id: int):
        uid = {"_id": user_id}
        logged = await self.mongoc.find_async(self.coll_users, uid)
        if logged:
            await self.mongoc.delete_async(self.coll_users, uid)

    async def how_many(self):
        return (user["user_id"] async for user in self.coll_users.find({}))
