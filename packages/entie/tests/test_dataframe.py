"""Tests for EnteiDataFrame (pure Python + entei-core)."""

from __future__ import annotations

import mongomock
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
    out = (
        df.filter_rows(lambda r: (r.get("x") or 0) > 2)
        .select("x")
        .collect(as_lists=True)
    )
    assert sorted(out["x"]) == [3, 5]
