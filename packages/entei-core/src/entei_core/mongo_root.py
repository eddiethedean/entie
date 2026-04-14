"""MongoDB collection root type for columnar materialization."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class MongoRoot:
    """Carrier for a collection plus optional fixed column list for materialization.

    Used with :func:`~entei_core.mongo_root_to_column_dict` to produce
    ``dict[str, list]`` with one list per top-level field.

    Parameters
    ----------
    collection:
        A PyMongo :class:`~pymongo.collection.Collection` or compatible (e.g. mongomock).
    fields:
        Column order and membership for output. If ``None``, field names are the
        union of top-level keys in all documents (sorted). If ``()`` (empty tuple),
        no columns are emitted even when documents exist. If non-empty, names must
        be unique. For an **empty** collection with ``fields is None``, the result
        has no columns.

    Raises
    ------
    ValueError
        If ``fields`` contains duplicate names.
    """

    collection: Any
    fields: tuple[str, ...] | None = None

    def __post_init__(self) -> None:
        """Validate ``fields`` invariants."""
        if self.fields is not None and len(self.fields) != len(set(self.fields)):
            raise ValueError("fields must not contain duplicate names")
