"""Tests for entei-core (Mongo root materialization only; no native stack)."""

from __future__ import annotations

import mongomock
from entei_core import MongoRoot, materialize_root_data, mongo_root_to_column_dict


def test_mongo_root_to_column_dict_orders_fields() -> None:
    client = mongomock.MongoClient()
    coll = client.db.t
    coll.insert_many([{"x": 2, "y": "b"}, {"x": 1, "y": "a"}])
    got = mongo_root_to_column_dict(MongoRoot(coll))
    assert got["x"] == [2, 1]
    assert got["y"] == ["b", "a"]


def test_mongo_root_empty_with_explicit_fields() -> None:
    client = mongomock.MongoClient()
    coll = client.db.empty
    got = mongo_root_to_column_dict(MongoRoot(coll, fields=("x", "y")))
    assert got == {"x": [], "y": []}


def test_materialize_root_data_passthrough() -> None:
    d = {"a": [1]}
    assert materialize_root_data(d) is d


def test_materialize_root_data_with_mongo_root() -> None:
    client = mongomock.MongoClient()
    coll = client.db.t
    coll.insert_many([{"x": 1}])
    root = MongoRoot(coll)
    got = materialize_root_data(root)
    assert got == mongo_root_to_column_dict(root)
    assert got["x"] == [1]


def test_mongo_root_empty_no_fields() -> None:
    client = mongomock.MongoClient()
    coll = client.db.empty_no_fields
    assert mongo_root_to_column_dict(MongoRoot(coll)) == {}
