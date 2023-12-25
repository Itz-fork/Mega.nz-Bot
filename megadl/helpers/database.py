from megadl.lib.aiomongo import AioMongo


class Users:
    def __init__(self) -> None:
        self.mongoc = AioMongo()
        self.coll = self.mongoc["mega_nz"]["users"]

    # <<<<<<<<<< Telegram functions >>>>>>>>>> #

    async def add(self, user_id: int):
        added = await self.is_there(user_id)
        if not added:
            await self.mongoc.insert(
                self.coll, {"_id": user_id, "email": "", "password": ""}
            )

    async def delete(self, user_id: int):
        uid = {"_id": user_id}
        added = await self.is_there(self.coll, user_id)
        if added:
            await self.mongoc.delete(self.coll, uid)

    async def is_there(self, user_id: int):
        uid = {"_id": user_id}
        return await self.mongoc.find(self.coll, uid)

    # <<<<<<<<<< Mega functions >>>>>>>>>> #

    async def mega_login(self, user_id: int, email: str, password: str):
        uid = {"_id": user_id}
        logged = await self.mongoc.find(self.coll, uid)
        if logged:
            await self.mongoc.update(
                self.coll, uid, {"email": email, "password": password}
            )
        # this should never happen but better safe than sorry
        else:
            await self.mongoc.insert(
                self.coll, {"_id": user_id, "email": email, "password": password}
            )

    async def mega_logout(self, user_id: int):
        uid = {"_id": user_id}
        logged = await self.mongoc.find(self.coll, uid)
        if logged:
            await self.mongoc.delete(self.coll, uid)

    async def how_many(self):
        return (user["user_id"] async for user in self.coll.find({}))
