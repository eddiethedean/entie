"""Tests for entie.io.Records."""

from __future__ import annotations

import mongomock

from entie import Records
from entie.client import EntieDatabase


def test_records_insert_into() -> None:
    client = mongomock.MongoClient()
    db = EntieDatabase(client.db.app)
    Records.from_list([{"name": "Ada"}, {"name": "Bob"}], database=db).insert_into("users")
    coll = db.collection("users")
    names = sorted(doc["name"] for doc in coll.find({}, {"_id": 0}))
    assert names == ["Ada", "Bob"]


def test_records_empty_insert_returns_none() -> None:
    client = mongomock.MongoClient()
    db = EntieDatabase(client.db.app)
    assert Records.from_list([], database=db).insert_into("empty") is None
