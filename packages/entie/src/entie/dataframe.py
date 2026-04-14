"""Lazy MongoDB collection views with in-Python filter, select, and collect."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any, Literal, overload

from entei_core import MongoRoot, mongo_root_to_column_dict


def _columns_to_rows(cols: dict[str, list[Any]]) -> list[dict[str, Any]]:
    """Turn columnar dict into row dicts (aligned by index)."""
    if not cols:
        return []
    keys = list(cols.keys())
    n = min(len(cols[k]) for k in keys)
    return [{k: cols[k][i] for k in keys} for i in range(n)]


def _rows_to_columns(rows: list[dict[str, Any]], keys: Sequence[str]) -> dict[str, list[Any]]:
    """Turn row dicts into columnar dict using ``keys`` order."""
    if not keys:
        return {}
    return {k: [r.get(k) for r in rows] for k in keys}


class EnteiDataFrame:
    """Lazy view over a collection; filters and projection run in Python on :meth:`collect`.

    Reads the collection once via :func:`entei_core.mongo_root_to_column_dict`
    (full ``find()``), then applies ``filter_rows`` predicates and ``select``
    column order. Not a streaming or server-side aggregation API.
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
        """Use :meth:`from_collection` to construct; constructor is for chaining.

        Parameters
        ----------
        collection:
            PyMongo collection (or compatible) scanned on ``collect``.
        fields:
            Column names passed to :class:`~entei_core.mongo_root.MongoRoot`; ``None``
            means infer keys from documents.
        filters:
            Predicates applied in order to row dicts after materialization.
        projection:
            If set, output columns are restricted to these names (after filters).
        """
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
        """Build a frame from a PyMongo (or mongomock) collection.

        Parameters
        ----------
        collection:
            Collection whose documents are read when :meth:`collect` runs.
        fields:
            Ordered top-level field names. If ``None``, keys are inferred from
            documents (union, sorted). If ``()`` or ``[]`` (normalized to ``()``),
            no columns are materialized. Names must be unique.

        Returns
        -------
        EnteiDataFrame
            Lazy frame; call :meth:`collect` to load data.

        See Also
        --------
        entei_core.mongo_root.MongoRoot : Semantics of ``fields`` and empty collections.
        """
        fk = tuple(fields) if fields is not None else None
        return cls(collection, fields=fk)

    def select(self, *columns: str) -> EnteiDataFrame:
        """Keep only the given output columns (applied after ``filter_rows``).

        Parameters
        ----------
        *columns:
            One or more distinct field names.

        Returns
        -------
        EnteiDataFrame
            New frame with projection set.

        Raises
        ------
        ValueError
            If no columns, or if any name is duplicated.
        """
        if not columns:
            raise ValueError("select() requires at least one column name")
        if len(columns) != len(set(columns)):
            raise ValueError("select() column names must be unique")
        return EnteiDataFrame(
            self._collection,
            fields=self._fields,
            filters=self._filters,
            projection=tuple(columns),
        )

    def filter_rows(self, predicate: Callable[[dict[str, Any]], bool]) -> EnteiDataFrame:
        """Return a frame that keeps rows where ``predicate(row)`` is true.

        Parameters
        ----------
        predicate:
            Called with each row as a ``dict[str, Any]`` (top-level fields).

        Returns
        -------
        EnteiDataFrame
            New frame with ``predicate`` appended to the filter chain.
        """
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
        """Materialize: scan collection, apply filters, then optional projection.

        Parameters
        ----------
        as_lists:
            If ``True`` (default), return ``dict[str, list]`` columnar data. If
            ``False``, return ``list[dict]`` rows.

        Returns
        -------
        dict[str, list] or list[dict]
            Columnar or row-oriented result consistent with ``as_lists``.
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
