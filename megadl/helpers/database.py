# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Database functions

from os import getenv

from pymongo import AsyncMongoClient, ReturnDocument


class CypherDB:
    # use slots for faster var lookups
    # usually this isnt needed, like at all
    # i cant justify myself for adding this either
    # but wait maybe i can?
    # i use find_one_and_update in .add(...) maximum efficiency so i guess its not that conflicting
    __slots__ = ("mongoc", "coll_users")
    
    def __init__(self) -> None:
        self.mongoc = AsyncMongoClient(getenv("MONGO_URI"))
        self.coll_users = self.mongoc["mega_nz"]["users"]

    # <<<<<<<<<< Active user functions >>>>>>>>>> #
    async def add(self, user_id: int):
        result = await self.coll_users.find_one_and_update(
            {"_id": user_id},
            {
                "$setOnInsert": {
                    "_id": user_id,
                    "email": "",
                    "password": "",
                    "status": {"banned": False, "reason": ""},
                    "total_downloads": 0,
                    "total_uploads": 0,
                    "proxy": "",
                }
            },
            projection={"_id": 0, "status": 1},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return result["status"]

    async def plus_fl_count(
        self, user_id: int, downloads: int | None = None, uploads: int | None = None
    ):
        if downloads:
            await self.coll_users.update_one(
                {"_id": user_id},
                {"$inc": {"total_downloads": downloads}},
            )
        elif uploads:
            await self.coll_users.update_one(
                {"_id": user_id},
                {"$inc": {"total_uploads": uploads}},
            )

    async def delete(self, user_id: int):
        await self.coll_users.delete_one({"_id": user_id})

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
        docu = await self.coll_users.find_one(uid, {"_id": 0})
        if not docu:
            return None
        if use_acc:
            return docu if not "" in (docu["email"], docu["password"]) else None
        else:
            return docu

    # <<<<<<<<<< Banned user functions >>>>>>>>>> #
    async def ban_user(self, user_id: int, reason: str = "Got banned :("):
        await self.coll_users.update_one(
            {"_id": user_id},
            {"$set": {"status": {"banned": True, "reason": reason}}},
        )

    async def unban_user(self, user_id: int, reason: str = "Got unbanned :)"):
        await self.coll_users.update_one(
            {"_id": user_id},
            {"$set": {"status": {"banned": False, "reason": reason}}},
        )

    # <<<<<<<<<< Mega functions >>>>>>>>>> #
    async def mega_login(self, user_id: int, email: str, password: str):
        await self.coll_users.update_one(
            {"_id": user_id},
            {"$set": {"email": email, "password": password}},
        )

    async def mega_logout(self, user_id: int):
        await self.coll_users.update_one(
            {"_id": user_id},
            {"$set": {"email": "", "password": ""}},
        )

    # this isnt used anywhere as far as from what i can tell but im not gonna risk it by deleting anything either
    # fuck it
    async def how_many(self):
        return (user["user_id"] async for user in self.coll_users.find({}))

    # <<<<<<<<<< Proxy functions >>>>>>>>>> #
    async def update_proxy(self, user_id: int, proxy: str):
        await self.coll_users.update_one(
            {"_id": user_id},
            {"$set": {"proxy": proxy}},
        )

    async def get_proxy(self, user_id: int):
        return await self.coll_users.find_one(
            {"_id": user_id}, {"proxy": 1}
        )
