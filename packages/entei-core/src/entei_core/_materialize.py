"""Scan collections into columnar ``dict[str, list]`` (top-level fields only)."""

from __future__ import annotations

from typing import Any

from .mongo_root import MongoRoot


def mongo_root_to_column_dict(root: MongoRoot) -> dict[str, list[Any]]:
    """Run ``find()`` on ``root.collection`` and build aligned column lists.

    Reads the entire cursor into memory. Only top-level keys participate; nested
    documents are values in a single cell.

    Parameters
    ----------
    root:
        Collection and optional ``fields`` (see :class:`MongoRoot`).

    Returns
    -------
    dict[str, list]
        Keys are field names; each value is the column in document order.

    Notes
    -----
    When ``root.fields`` is ``None``, keys are inferred from documents. When it is
    an empty tuple, returns ``{}`` for any document count.
    """
    coll = root.collection
    cursor = coll.find()
    docs: list[dict[str, Any]] = list(cursor)
    if not docs:
        keys = list(root.fields) if root.fields is not None else []
        return {k: [] for k in keys}

    if root.fields is not None:
        keys = list(root.fields)
    else:
        key_set: set[str] = set()
        for d in docs:
            key_set.update(d.keys())
        keys = sorted(key_set)

    out: dict[str, list[Any]] = {k: [] for k in keys}
    for d in docs:
        for k in keys:
            out[k].append(d.get(k))
    return out


def materialize_root_data(data: Any) -> Any:
    """Normalize pipeline data: columnarize :class:`MongoRoot`, else identity.

    Parameters
    ----------
    data:
        Any value. If it is a :class:`MongoRoot`, returns the columnar dict from
        :func:`mongo_root_to_column_dict`; otherwise returns ``data`` unchanged.

    Returns
    -------
    Any
        Columnar dict or the original ``data``.
    """
    if isinstance(data, MongoRoot):
        return mongo_root_to_column_dict(data)
    return data
