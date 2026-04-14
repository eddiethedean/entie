"""PyMongo connection helpers: :func:`connect`, :class:`EntieMongoClient`, :class:`EntieDatabase`."""

from __future__ import annotations

import os
from typing import Any, overload

from pymongo import MongoClient

_DEFAULT_URI_ENV = "ENTIE_URI"


class EntieMongoClient:
    """Thin wrapper around :class:`pymongo.mongo_client.MongoClient`.

    Use :meth:`database` to get an :class:`EntieDatabase`, then
    :meth:`EntieDatabase.collection` or :meth:`EntieDatabase.table` for
    :meth:`EnteiDataFrame.from_collection` and inserts.
    """

    __slots__ = ("_client",)

    def __init__(self, client: MongoClient[Any]) -> None:
        """Wrap an existing PyMongo client.

        Parameters
        ----------
        client:
            Connected :class:`~pymongo.mongo_client.MongoClient` instance.
        """
        self._client = client

    @property
    def raw(self) -> MongoClient[Any]:
        """The underlying :class:`~pymongo.mongo_client.MongoClient`."""
        return self._client

    def database(self, name: str, *, codec_options: Any | None = None) -> EntieDatabase:
        """Return a database by name.

        Parameters
        ----------
        name:
            MongoDB database name.
        codec_options:
            Optional BSON :class:`~bson.codec_options.CodecOptions` for this database.

        Returns
        -------
        EntieDatabase
            Wrapper around ``client[name]`` or ``get_database(...)``.
        """
        if codec_options is not None:
            return EntieDatabase(self._client.get_database(name, codec_options=codec_options))
        return EntieDatabase(self._client[name])

    def close(self) -> None:
        """Close the underlying PyMongo client (releases sockets)."""
        self._client.close()

    def __enter__(self) -> EntieMongoClient:
        """Enter context: returns ``self`` (caller should ``close()`` on exit)."""
        return self

    def __exit__(self, *_args: object) -> None:
        """Exit context: calls :meth:`close`."""
        self.close()


class EntieDatabase:
    """Handle for a single MongoDB database (PyMongo ``Database``).

    Must wrap a PyMongo :class:`~pymongo.database.Database`, not a
    :class:`~pymongo.collection.Collection`. Use :meth:`collection` / :meth:`table`
    to obtain collections by name.
    """

    __slots__ = ("_db",)

    def __init__(self, db: Any) -> None:
        """Parameters
        ----------
        db:
            PyMongo :class:`~pymongo.database.Database` (e.g. ``client["app"]``).
        """
        self._db = db

    @property
    def raw(self) -> Any:
        """The underlying PyMongo :class:`~pymongo.database.Database`."""
        return self._db

    def collection(self, name: str) -> Any:
        """Return the named :class:`~pymongo.collection.Collection`."""
        return self._db[name]

    def table(self, name: str) -> Any:
        """Alias for :meth:`collection` (collection-as-table naming)."""
        return self.collection(name)

    def list_collection_names(self) -> list[str]:
        """List collection names in this database (see PyMongo ``list_collection_names``)."""
        return list(self._db.list_collection_names())

    def tables(self) -> list[str]:
        """Same as :meth:`list_collection_names`."""
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
    """Open a MongoDB connection or wrap an existing client.

    If ``client`` is omitted, builds a new :class:`~pymongo.mongo_client.MongoClient`
    from ``uri``, or from the ``ENTIE_URI`` environment variable when ``uri`` is omitted.

    Parameters
    ----------
    uri:
        MongoDB connection URI. Ignored when ``client`` is passed. If omitted and
        ``client`` is omitted, ``ENTIE_URI`` is read.
    database:
        If set, returns :class:`EntieDatabase` for that database; otherwise returns
        :class:`EntieMongoClient`.
    client:
        Existing client to wrap. Do not pass ``uri`` at the same time.
    **client_kwargs:
        Forwarded to :class:`~pymongo.mongo_client.MongoClient` only when a new
        client is constructed (``client`` is ``None``).

    Returns
    -------
    EntieMongoClient or EntieDatabase
        Client wrapper, or database handle when ``database`` is not ``None``.

    Raises
    ------
    ValueError
        If neither a resolvable URI nor ``client`` is given; or if both ``uri``
        and ``client`` are passed.
    """
    if client is not None and uri is not None:
        raise ValueError("Pass only one of uri=... or client=..., not both.")
    if client is None:
        resolved = uri if uri is not None else os.environ.get(_DEFAULT_URI_ENV)
        if not resolved:
            raise ValueError("Provide uri=..., set ENTIE_URI, or pass client=... to connect().")
        client = MongoClient(resolved, **client_kwargs)

    wrapped = EntieMongoClient(client)
    if database is not None:
        return wrapped.database(database)
    return wrapped
