"""Tests for EntieDatabase helpers (moltres-shaped API)."""

from __future__ import annotations

import mongomock

from entie.client import EntieDatabase


def test_table_is_collection_alias() -> None:
    client = mongomock.MongoClient()
    db = EntieDatabase(client["app"])
    assert db.table("c") is db.collection("c")


def test_tables_lists_collections() -> None:
    client = mongomock.MongoClient()
    db = EntieDatabase(client["testdb"])
    db.collection("a").insert_one({"x": 1})
    db.collection("b").insert_one({"y": 2})
    assert set(db.tables()) == {"a", "b"}
