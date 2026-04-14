"""Insert helpers aligned with moltres ``Records`` + ``insert_into`` (MongoDB)."""

from __future__ import annotations

from typing import Any

from ..client import EntieDatabase


class Records:
    """Hold rows and insert them into a MongoDB collection (``insert_many``).

    Parallel to **moltres** ``Records`` + ``insert_into``, for document stores.
    """

    __slots__ = ("_database", "_rows")

    def __init__(self, rows: list[dict[str, Any]], *, database: EntieDatabase) -> None:
        """Parameters
        ----------
        rows:
            Document-shaped dicts to insert.
        database:
            Target :class:`~entie.client.EntieDatabase` (wraps a PyMongo database).
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
        """Build from a list of row dicts (copied shallowly into a new list).

        Returns
        -------
        Records
            Ready for :meth:`insert_into`.
        """
        return cls(list(rows), database=database)

    def insert_into(self, table: str) -> Any:
        """Insert all rows into collection ``table`` (MongoDB collection name).

        Returns the PyMongo :meth:`~pymongo.collection.Collection.insert_many`
        result, or ``None`` when there are zero rows.
        """
        coll = self._database.collection(table)
        if not self._rows:
            return None
        return coll.insert_many(self._rows)
