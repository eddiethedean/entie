"""MongoDB root materialization for columnar ``dict[str, list]`` roots (no native stack)."""

from __future__ import annotations

from ._materialize import materialize_root_data, mongo_root_to_column_dict
from .mongo_root import MongoRoot

__all__ = [
    "MongoRoot",
    "materialize_root_data",
    "mongo_root_to_column_dict",
    "__version__",
]

__version__ = "0.1.0"
