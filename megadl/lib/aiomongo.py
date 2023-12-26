from os import getenv
from typing import Any
from bson.codec_options import TypeRegistry
from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient

from megadl.helpers.sysfncs import run_partial


class AioMongo(MongoClient):
    client = None

    def __init__(
        self,
        port: int | None = None,
        document_class: type | None = None,
        tz_aware: bool | None = None,
        connect: bool | None = None,
        type_registry: TypeRegistry | None = None,
        **kwargs: Any
    ) -> None:
        self.atlas_host = getenv("MONGO_URI")
        super().__init__(
            self.atlas_host, port, document_class, tz_aware, connect, type_registry, **kwargs
        )

    async def insert(self, coll: Collection, query: dict, *args, **kwargs):
        """
        Perform `insert_one` operation on the given collection
        """
        return await run_partial(coll.insert_one, query, *args, **kwargs)

    async def find(self, coll: Collection, query: dict, *args, **kwargs):
        """
        Perform `find_one` operation on the given collection
        """
        return await run_partial(coll.find_one, query, *args, **kwargs)

    async def update(self, coll: Collection, query: dict, value: dict, *args, **kwargs):
        """
        Perform `update_one` operation on the given collection
        """
        return await run_partial(
            coll.update_one, query, {"$set": value}, *args, **kwargs
        )

    async def delete(self, coll: Collection, query: dict, *args, **kwargs):
        """
        Perform `delete_one` operation on the given collection
        """
        return await run_partial(coll.delete_one, query, *args, **kwargs)
