"""Mongo-backed table API (pure Python; uses ``entei_core`` materialization only)."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any, Literal, overload

from entei_core import MongoRoot, mongo_root_to_column_dict


def _columns_to_rows(cols: dict[str, list[Any]]) -> list[dict[str, Any]]:
    if not cols:
        return []
    keys = list(cols.keys())
    n = min(len(cols[k]) for k in keys)
    return [{k: cols[k][i] for k in keys} for i in range(n)]


def _rows_to_columns(rows: list[dict[str, Any]], keys: Sequence[str]) -> dict[str, list[Any]]:
    if not keys:
        return {}
    return {k: [r.get(k) for r in rows] for k in keys}


class EnteiDataFrame:
    """Lazy view over a MongoDB collection with in-Python filter/select on ``collect``.

    Uses :func:`entei_core.mongo_root_to_column_dict` only — no pydantable-native.
    """

    __slots__ = ("_collection", "_fields", "_filters", "_projection")

    def __init__(
        self,
        collection: Any,
        *,
        fields: tuple[str, ...] | None = None,
        filters: tuple[Callable[[dict[str, Any]], bool], ...] = (),
        projection: tuple[str, ...] | None = None,
    ) -> None:
        self._collection = collection
        self._fields = fields
        self._filters = filters
        self._projection = projection

    @classmethod
    def from_collection(
        cls,
        collection: Any,
        *,
        fields: Sequence[str] | None = None,
    ) -> EnteiDataFrame:
        """Load from a PyMongo :class:`~pymongo.collection.Collection` (or mongomock).

        ``fields`` fixes column order for empty collections and limits which keys are
        read; if omitted, keys are inferred from documents (see :class:`MongoRoot`).
        """
        fk = tuple(fields) if fields is not None else None
        return cls(collection, fields=fk)

    def select(self, *columns: str) -> EnteiDataFrame:
        """Restrict output columns (applied after filters)."""
        if not columns:
            raise ValueError("select() requires at least one column name")
        return EnteiDataFrame(
            self._collection,
            fields=self._fields,
            filters=self._filters,
            projection=tuple(columns),
        )

    def filter_rows(self, predicate: Callable[[dict[str, Any]], bool]) -> EnteiDataFrame:
        """Keep rows where ``predicate(row)`` is true (``row`` is a ``dict``)."""
        return EnteiDataFrame(
            self._collection,
            fields=self._fields,
            filters=self._filters + (predicate,),
            projection=self._projection,
        )

    @overload
    def collect(self, *, as_lists: Literal[True] = True) -> dict[str, list[Any]]: ...

    @overload
    def collect(self, *, as_lists: Literal[False]) -> list[dict[str, Any]]: ...

    def collect(
        self,
        *,
        as_lists: bool = True,
    ) -> dict[str, list[Any]] | list[dict[str, Any]]:
        """Materialize: read collection, apply filters, then projection.

        With ``as_lists=True`` (default), returns ``dict[str, list]`` columnar form.
        With ``as_lists=False``, returns ``list[dict]`` rows.
        """
        root = MongoRoot(self._collection, fields=self._fields)
        cols = mongo_root_to_column_dict(root)
        rows = _columns_to_rows(cols)
        for pred in self._filters:
            rows = [r for r in rows if pred(r)]
        proj = self._projection
        if proj is not None:
            rows = [{k: r.get(k) for k in proj} for r in rows]
            keys = list(proj)
        else:
            keys = list(cols.keys())
        if as_lists:
            return _rows_to_columns(rows, keys)
        return rows
