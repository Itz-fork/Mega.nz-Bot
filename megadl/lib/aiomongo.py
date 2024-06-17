# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Async wrapper for pymongo's insert, find, update and delete operations

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
            self.atlas_host,
            port,
            document_class,
            tz_aware,
            connect,
            type_registry,
            **kwargs
        )

    async def insert_async(self, coll: Collection, query: dict, *args, **kwargs):
        """
        Perform `insert_one` operation on the given collection
        """
        return await run_partial(coll.insert_one, query, *args, **kwargs)

    async def find_async(self, coll: Collection, query: dict, *args, **kwargs):
        """
        Perform `find_one` operation on the given collection
        """
        return await run_partial(coll.find_one, query, *args, **kwargs)

    async def update_async(
        self,
        coll: Collection,
        query: dict,
        value: dict,
        no_modify: bool = False,
        use_given: bool = False,
        *args,
        **kwargs
    ):
        """
        Perform `update_one` operation on the given collection
        """
        if no_modify:
            return await run_partial(
                coll.update_one, query, {"$setOnInsert": value}, *args, **kwargs
            )
        elif use_given:
            return await run_partial(coll.update_one, query, value, *args, **kwargs)
        else:
            return await run_partial(
                coll.update_one, query, {"$set": value}, *args, **kwargs
            )

    async def delete_async(self, coll: Collection, query: dict, *args, **kwargs):
        """
        Perform `delete_one` operation on the given collection
        """
        return await run_partial(coll.delete_one, query, *args, **kwargs)

    async def count_documents_async(
        self, coll: Collection, query: dict, *args, **kwargs
    ):
        """
        Perform `count_documents` operation on the given collection
        """
        return await run_partial(coll.count_documents, query, *args, **kwargs)

    async def find_many_async(self, coll: Collection, query: dict, *args, **kwargs):
        """
        Perform `find` operation on the given collection
        """
        return await run_partial(coll.find, query, *args, **kwargs)
