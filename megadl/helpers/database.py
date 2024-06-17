# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Database functions

from megadl.lib.aiomongo import AioMongo


class CypherDB:
    def __init__(self) -> None:
        self.mongoc = AioMongo()
        self.coll_users = self.mongoc["mega_nz"]["users"]

    # <<<<<<<<<< Active user functions >>>>>>>>>> #

    async def add(self, user_id: int):
        await self.mongoc.update_async(
            self.coll_users,
            {"_id": user_id},
            {
                "_id": user_id,
                "email": "",
                "password": "",
                "status": {"banned": False, "reason": ""},
                "total_downloads": 0,
                "total_uploads": 0,
                "proxy": "",
            },
            no_modify=True,
            upsert=True,
        )
        return (
            await self.mongoc.find_async(
                self.coll_users, {"_id": user_id}, {"_id": 0, "status": 1}
            )
        )["status"]

    async def plus_fl_count(
        self, user_id: int, downloads: int | None = None, uploads: int | None = None
    ):
        if downloads:
            await self.mongoc.update_async(
                self.coll_users,
                {"_id": user_id},
                {"$inc": {"total_downloads": downloads}},
                use_given=True,
            )
        elif uploads:
            await self.mongoc.update_async(
                self.coll_users,
                {"_id": user_id},
                {"$inc": {"total_uploads": uploads}},
                use_given=True,
            )

    async def delete(self, user_id: int):
        await self.mongoc.delete_async(self.coll_users, {"_id": user_id})

    async def is_there(self, user_id: int, use_acc: bool = False):
        """
        Returns:
            {
                "email": "",
                "password": "",
                "status": {"banned": False, "reason": ""},
                "total_downloads": 0,
                "total_uploads": 0,
                "proxy": ""
            }
        """
        uid = {"_id": user_id}
        docu = await self.mongoc.find_async(self.coll_users, uid, {"_id": 0})
        if not docu:
            return None
        if use_acc:
            return docu if not "" in {docu["email"], docu["password"]} else None
        else:
            return docu

    # <<<<<<<<<< Banned user functions >>>>>>>>>> #
    async def ban_user(self, user_id: int, reason: str):
        await self.mongoc.update_async(
            self.coll_users,
            {"_id": user_id},
            {"status": {"banned": True, "reason": reason}},
        )

    async def unban_user(self, user_id: int):
        await self.mongoc.update_async(
            self.coll_users,
            {"_id": user_id},
            {"status": {"banned": False, "reason": "Got unbanned"}},
        )

    # <<<<<<<<<< Mega functions >>>>>>>>>> #

    async def mega_login(self, user_id: int, email: str, password: str):
        await self.mongoc.update_async(
            self.coll_users,
            {"_id": user_id},
            {"email": email, "password": password},
            upsert=True,
        )

    async def mega_logout(self, user_id: int):
        await self.mongoc.delete_async(self.coll_users, {"_id": user_id})

    async def how_many(self):
        return (user["user_id"] async for user in self.coll_users.find({}))

    # <<<<<<<<<< Proxy functions >>>>>>>>>> #
    async def update_proxy(self, user_id: int, proxy: str):
        await self.mongoc.update_async(
            self.coll_users,
            {"_id": user_id},
            {"proxy": proxy},
            upsert=True,
        )

    async def get_proxy(self, user_id: int):
        return await self.mongoc.find_async(
            self.coll_users, {"_id": user_id}, {"proxy": 1}
        )
