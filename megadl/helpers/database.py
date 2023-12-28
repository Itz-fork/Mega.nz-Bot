# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Database functions

from megadl.lib.aiomongo import AioMongo


class Users:
    def __init__(self) -> None:
        self.mongoc = AioMongo()
        self.mdb = self.mongoc["mega_nz"]
        self.coll_users = self.mdb["users"]
        self.coll_banned = self.mdb["banned"]

    # <<<<<<<<<< Active user functions >>>>>>>>>> #

    async def add(self, user_id: int):
        added = await self.is_there(user_id)
        if not added:
            await self.mongoc.insert(
                self.coll_users,
                {
                    "_id": user_id,
                    "email": "",
                    "password": "",
                    "total_downloads": 0,
                    "total_uploads": 0,
                },
            )

    async def plus_fl_count(
        self, user_id: int, downloads: int | None = None, uploads: int | None = None
    ):
        _, _, ctdl, cuptl = await self.is_there(user_id)
        if downloads:
            await self.mongoc.update(
                self.coll_users, {"_id": user_id}, {"total_downloads": ctdl + downloads}
            )
        elif uploads:
            await self.mongoc.update(
                self.coll_users, {"_id": user_id}, {"total_uploads": cuptl + uploads}
            )

    async def delete(self, user_id: int):
        uid = {"_id": user_id}
        added = await self.is_there(self.coll_users, user_id)
        if added:
            await self.mongoc.delete(self.coll_users, uid)

    async def is_there(self, user_id: int, use_acc: bool = False):
        uid = {"_id": user_id}
        docu = await self.mongoc.find(self.coll_users, uid)
        if use_acc:
            email = docu["email"]
            password = docu["password"]
            tdl = docu["total_downloads"]
            tupld = docu["total_uploads"]
            return (
                [email, password, tdl, tupld] if not "" in {email, password} else None
            )
        else:
            return docu

    # <<<<<<<<<< Banned user functions >>>>>>>>>> #
    async def ban_user(self, user_id: int):
        uid = {"_id": user_id}
        await self.delete(user_id)
        banned = await self.mongoc.find(self.coll_banned, user_id)
        if not banned:
            await self.mongoc.insert(self.coll_banned, {"_id": user_id})

    async def unban_user(self, user_id: int):
        await self.mongoc.delete(self.coll_banned, {"_id": user_id})

    # <<<<<<<<<< Mega functions >>>>>>>>>> #

    async def mega_login(self, user_id: int, email: str, password: str):
        uid = {"_id": user_id}
        logged = await self.mongoc.find(self.coll_users, uid)
        if logged:
            await self.mongoc.update(
                self.coll_users, uid, {"email": email, "password": password}
            )
        # this should never happen but better safe than sorry
        else:
            await self.mongoc.insert(
                self.coll_users, {"_id": user_id, "email": email, "password": password}
            )

    async def mega_logout(self, user_id: int):
        uid = {"_id": user_id}
        logged = await self.mongoc.find(self.coll_users, uid)
        if logged:
            await self.mongoc.delete(self.coll_users, uid)

    async def how_many(self):
        return (user["user_id"] async for user in self.coll_users.find({}))
