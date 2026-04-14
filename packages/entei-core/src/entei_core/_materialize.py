"""Materialize MongoDB collections to columnar ``dict[str, list]``."""

from __future__ import annotations

from typing import Any

from .mongo_root import MongoRoot


def mongo_root_to_column_dict(root: MongoRoot) -> dict[str, list[Any]]:
    """Read all documents from ``root.collection`` into columnar form.

    Parameters
    ----------
    root:
        Collection root and optional ``fields`` ordering (see :class:`MongoRoot`).

    Returns
    -------
    dict[str, list]
        One list per column key, aligned by row index.
    """
    coll = root.collection
    cursor = coll.find()
    docs: list[dict[str, Any]] = list(cursor)
    if not docs:
        keys = list(root.fields) if root.fields else []
        return {k: [] for k in keys}

    if root.fields:
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
    """If ``data`` is :class:`MongoRoot`, return columnar dict; else pass through.

    Parameters
    ----------
    data:
        A :class:`MongoRoot` or any other value.

    Returns
    -------
    Any
        Columnar dict from :func:`mongo_root_to_column_dict` if ``data`` is
        :class:`MongoRoot`; otherwise ``data`` unchanged.
    """
    if isinstance(data, MongoRoot):
        return mongo_root_to_column_dict(data)
    return data
