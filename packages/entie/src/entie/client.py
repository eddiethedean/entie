"""MongoDB connection helpers (moltres ``connect`` / ``Database`` analogue)."""

from __future__ import annotations

import os
from typing import Any, overload

from pymongo import MongoClient

_DEFAULT_URI_ENV = "ENTIE_URI"


class EntieMongoClient:
    """Thin wrapper around :class:`pymongo.mongo_client.MongoClient`.

    Use :meth:`database` to obtain an :class:`EntieDatabase` and then
    :meth:`EntieDatabase.collection` for use with
    :meth:`EnteiDataFrame.from_collection`.
    """

    __slots__ = ("_client",)

    def __init__(self, client: MongoClient[Any]) -> None:
        """Parameters
        ----------
        client:
            An existing PyMongo :class:`~pymongo.mongo_client.MongoClient`.
        """
        self._client = client

    @property
    def raw(self) -> MongoClient[Any]:
        """Underlying PyMongo client."""
        return self._client

    def database(self, name: str, *, codec_options: Any | None = None) -> EntieDatabase:
        """Open a database by name.

        Parameters
        ----------
        name:
            MongoDB database name.
        codec_options:
            Optional :class:`~bson.codec_options.CodecOptions` for this database.

        Returns
        -------
        EntieDatabase
            Handle backed by ``client[name]`` or ``get_database``.
        """
        if codec_options is not None:
            return EntieDatabase(self._client.get_database(name, codec_options=codec_options))
        return EntieDatabase(self._client[name])

    def close(self) -> None:
        """Close the underlying PyMongo client."""
        self._client.close()

    def __enter__(self) -> EntieMongoClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class EntieDatabase:
    """Reference to a MongoDB database (moltres ``Database``-shaped entry point).

    Wrap a PyMongo :class:`~pymongo.database.Database`, not a
    :class:`~pymongo.collection.Collection`.
    """

    __slots__ = ("_db",)

    def __init__(self, db: Any) -> None:
        """Parameters
        ----------
        db:
            PyMongo ``Database`` instance (e.g. ``client["app"]``).
        """
        self._db = db

    @property
    def raw(self) -> Any:
        """Underlying PyMongo ``Database``."""
        return self._db

    def collection(self, name: str) -> Any:
        """Return a :class:`~pymongo.collection.Collection` by name."""
        return self._db[name]

    def table(self, name: str) -> Any:
        """Same as :meth:`collection` — moltres-style name for a logical table."""
        return self.collection(name)

    def list_collection_names(self) -> list[str]:
        """Return collection names in this database (delegates to PyMongo)."""
        return list(self._db.list_collection_names())

    def tables(self) -> list[str]:
        """Collection names in this database (alias for :meth:`list_collection_names`)."""
        return self.list_collection_names()


@overload
def connect(
    uri: str | None = None,
    *,
    database: str,
    client: MongoClient[Any] | None = None,
    **client_kwargs: Any,
) -> EntieDatabase: ...


@overload
def connect(
    uri: str | None = None,
    *,
    database: None = None,
    client: MongoClient[Any] | None = None,
    **client_kwargs: Any,
) -> EntieMongoClient: ...


def connect(
    uri: str | None = None,
    *,
    database: str | None = None,
    client: MongoClient[Any] | None = None,
    **client_kwargs: Any,
) -> EntieMongoClient | EntieDatabase:
    """Connect to MongoDB (moltres :func:`connect` analogue).

    Parameters
    ----------
    uri:
        MongoDB connection URI. If omitted, uses the ``ENTIE_URI`` environment
        variable (parallel to moltres ``MOLTRES_DSN``).
    database:
        If set, returns an :class:`EntieDatabase` for that database instead of
        :class:`EntieMongoClient`.
    client:
        An existing :class:`~pymongo.mongo_client.MongoClient`. If provided,
        ``uri`` must be ``None`` (URI is ignored).
    **client_kwargs:
        Forwarded to :class:`~pymongo.mongo_client.MongoClient` when ``client``
        is not provided.

    Returns
    -------
    EntieMongoClient or EntieDatabase
        Client wrapper, or a database handle when ``database`` is set.

    Raises
    ------
    ValueError
        If no URI is available and ``client`` is not passed.
    """
    if client is None:
        resolved = uri if uri is not None else os.environ.get(_DEFAULT_URI_ENV)
        if not resolved:
            raise ValueError("Provide uri=..., set ENTIE_URI, or pass client=... to connect().")
        client = MongoClient(resolved, **client_kwargs)

    wrapped = EntieMongoClient(client)
    if database is not None:
        return wrapped.database(database)
    return wrapped
