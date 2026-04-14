"""Bulk insert helpers: build rows in memory then ``insert_many`` into a collection."""

from __future__ import annotations

from typing import Any

from ..client import EntieDatabase


class Records:
    """Rows staged for insertion into a MongoDB collection via PyMongo ``insert_many``."""

    __slots__ = ("_database", "_rows")

    def __init__(self, rows: list[dict[str, Any]], *, database: EntieDatabase) -> None:
        """Parameters
        ----------
        rows:
            BSON-compatible document dicts to insert.
        database:
            Target database; collection is chosen in :meth:`insert_into`.
        """
        self._rows = rows
        self._database = database

    @classmethod
    def from_list(
        cls,
        rows: list[dict[str, Any]],
        *,
        database: EntieDatabase,
    ) -> Records:
        """Copy ``rows`` into a new list and wrap with ``database``.

        Parameters
        ----------
        rows:
            Documents to insert (shallow-copied list; dicts are not deep-copied).
        database:
            :class:`~entie.client.EntieDatabase` backing the target collections.

        Returns
        -------
        Records
            Call :meth:`insert_into` to perform the insert.
        """
        return cls(list(rows), database=database)

    def insert_into(self, table: str) -> Any:
        """Insert all rows into the named collection.

        Parameters
        ----------
        table:
            Collection name on ``database`` (MongoDB collection, not SQL table).

        Returns
        -------
        InsertManyResult or None
            PyMongo ``insert_many`` result, or ``None`` if there are zero rows.
        """
        coll = self._database.collection(table)
        if not self._rows:
            return None
        return coll.insert_many(self._rows)
