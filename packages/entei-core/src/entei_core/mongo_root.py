"""Typed carrier for pymongo collection roots."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class MongoRoot:
    """Reference to a MongoDB collection as lazy root data.

    Materialization produces columnar ``dict[str, list]`` (top-level fields only
    in this version).

    Parameters
    ----------
    collection:
        A :class:`pymongo.collection.Collection` (or compatible, e.g. mongomock).
    fields:
        Optional ordered column list. If omitted, keys are the union of top-level
        field names across all documents (sorted for stability). Empty collection
        requires ``fields`` to produce empty columns.
    """

    collection: Any
    fields: tuple[str, ...] | None = None

    def __post_init__(self) -> None:
        if self.fields is not None and len(self.fields) != len(set(self.fields)):
            raise ValueError("fields must not contain duplicate names")
