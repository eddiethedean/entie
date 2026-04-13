"""Tests for entie connect and EnteiDataFrame."""

from __future__ import annotations

import mongomock
import pytest
from entie import EnteiDataFrame, connect


def test_connect_requires_uri_or_client() -> None:
    with pytest.raises(ValueError, match="Provide uri"):
        connect()


def test_connect_with_in_memory_mock() -> None:
    client = mongomock.MongoClient()
    mc = connect(client=client)
    db = mc.database("db")
    coll = db.collection("c")
    coll.insert_many([{"x": 1}, {"x": 2}])
    df = EnteiDataFrame.from_collection(coll, fields=("x",))
    assert df.collect(as_lists=True) == {"x": [1, 2]}


def test_connect_database_kwarg_returns_entie_database() -> None:
    client = mongomock.MongoClient()
    db = connect(client=client, database="app")
    coll = db.collection("items")
    coll.insert_many([{"x": 7}])
    df = EnteiDataFrame.from_collection(coll, fields=("x",))
    assert df.collect(as_lists=True) == {"x": [7]}
