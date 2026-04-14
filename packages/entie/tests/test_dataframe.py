"""Tests for EnteiDataFrame (pure Python + entei-core)."""

from __future__ import annotations

import mongomock
import pytest

from entie import EnteiDataFrame


def test_entei_dataframe_from_collection_collect() -> None:
    client = mongomock.MongoClient()
    coll = client.db.items
    coll.insert_many([{"x": 3}, {"x": 4}])
    df = EnteiDataFrame.from_collection(coll)
    out = df.collect(as_lists=True)
    assert out["x"] == [3, 4]


def test_entei_dataframe_select_filter_rows() -> None:
    client = mongomock.MongoClient()
    coll = client.db.items
    coll.insert_many([{"x": 1}, {"x": 5}, {"x": 3}])
    df = EnteiDataFrame.from_collection(coll)
    out = df.filter_rows(lambda r: (r.get("x") or 0) > 2).select("x").collect(as_lists=True)
    assert sorted(out["x"]) == [3, 5]


def test_collect_as_lists_false_returns_rows() -> None:
    client = mongomock.MongoClient()
    coll = client.db.items
    coll.insert_many([{"x": 1}, {"x": 2}])
    df = EnteiDataFrame.from_collection(coll, fields=("x",))
    rows = df.collect(as_lists=False)
    assert rows == [{"x": 1}, {"x": 2}]


def test_select_no_columns_raises() -> None:
    client = mongomock.MongoClient()
    coll = client.db.items
    coll.insert_one({"x": 1})
    df = EnteiDataFrame.from_collection(coll, fields=("x",))
    with pytest.raises(ValueError, match="at least one column"):
        df.select()


def test_select_duplicate_columns_raises() -> None:
    client = mongomock.MongoClient()
    coll = client.db.items
    coll.insert_one({"x": 1})
    df = EnteiDataFrame.from_collection(coll, fields=("x",))
    with pytest.raises(ValueError, match="unique"):
        df.select("x", "x")


def test_empty_collection_with_fields_collect() -> None:
    client = mongomock.MongoClient()
    coll = client.db.empty
    df = EnteiDataFrame.from_collection(coll, fields=("x", "y"))
    assert df.collect(as_lists=True) == {"x": [], "y": []}


def test_empty_collection_no_fields_collect_empty_dict() -> None:
    """Empty coll + no fields => empty cols => _rows_to_columns([], [])."""
    client = mongomock.MongoClient()
    coll = client.db.empty_nf
    df = EnteiDataFrame.from_collection(coll)
    assert df.collect(as_lists=True) == {}


def test_from_collection_empty_fields_non_empty_collection() -> None:
    client = mongomock.MongoClient()
    coll = client.db.items
    coll.insert_many([{"x": 1}, {"y": 2}])
    df = EnteiDataFrame.from_collection(coll, fields=[])
    assert df.collect(as_lists=True) == {}


def test_filter_removes_all_rows() -> None:
    client = mongomock.MongoClient()
    coll = client.db.items
    coll.insert_many([{"x": 1}, {"x": 2}])
    df = EnteiDataFrame.from_collection(coll, fields=("x",))
    out = df.filter_rows(lambda _r: False).collect(as_lists=True)
    assert out == {"x": []}
