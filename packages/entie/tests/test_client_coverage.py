"""Extra tests for client helpers (coverage for branches)."""

from __future__ import annotations

from unittest.mock import MagicMock

import mongomock
import pytest
from bson.codec_options import CodecOptions

from entie.client import EntieDatabase, EntieMongoClient, connect


def test_entie_mongo_client_raw_and_close() -> None:
    c = mongomock.MongoClient()
    mc = EntieMongoClient(c)
    assert mc.raw is c
    mc.close()


def test_entie_database_raw() -> None:
    c = mongomock.MongoClient()
    db = EntieDatabase(c["mydb"])
    assert db.raw is c["mydb"]


def test_connect_context_manager() -> None:
    c = mongomock.MongoClient()
    with connect(client=c) as mc:
        assert isinstance(mc, EntieMongoClient)
        assert mc.raw is c


def test_connect_via_uri_monkeypatched(monkeypatch: pytest.MonkeyPatch) -> None:
    created: list[str] = []

    def fake_mongo(uri: str, **kwargs: object) -> mongomock.MongoClient:
        created.append(uri)
        return mongomock.MongoClient()

    monkeypatch.setattr("entie.client.MongoClient", fake_mongo)
    mc = connect("mongodb://localhost:27017")
    assert created == ["mongodb://localhost:27017"]
    assert isinstance(mc, EntieMongoClient)


def test_connect_via_entie_uri_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENTIE_URI", "mongodb://env.example")
    monkeypatch.setattr("entie.client.MongoClient", lambda uri, **kw: mongomock.MongoClient())
    mc = connect()
    assert isinstance(mc, EntieMongoClient)


def test_database_with_codec_options() -> None:
    mock_client = MagicMock()
    mock_inner_db = MagicMock()
    mock_client.get_database.return_value = mock_inner_db
    emc = EntieMongoClient(mock_client)
    co = CodecOptions()
    db = emc.database("name", codec_options=co)
    assert isinstance(db, EntieDatabase)
    mock_client.get_database.assert_called_once_with("name", codec_options=co)


def test_database_without_codec_options_uses_getitem() -> None:
    mock_client = MagicMock()
    sentinel = object()
    mock_client.__getitem__.return_value = sentinel
    emc = EntieMongoClient(mock_client)
    db = emc.database("name")
    assert db.raw is sentinel
    mock_client.__getitem__.assert_called_once_with("name")
