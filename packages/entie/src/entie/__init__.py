"""Public Entie API — MongoDB helpers on **entei-core** only (no native Rust stack).

Mirrors the role of `moltres`_ relative to ``moltres-core``: **entei-core** holds
Mongo materialization; **entie** adds connection helpers and a small Python
table API.

.. _moltres: https://github.com/eddiethedean/moltres
"""

from __future__ import annotations

from entei_core import MongoRoot, materialize_root_data, mongo_root_to_column_dict

from .client import EntieDatabase, EntieMongoClient, connect
from .dataframe import EnteiDataFrame
from .expressions import col, column, lit

__version__ = "0.1.0"

__all__ = [
    "EnteiDataFrame",
    "EntieDatabase",
    "EntieMongoClient",
    "MongoRoot",
    "materialize_root_data",
    "mongo_root_to_column_dict",
    "__version__",
    "col",
    "column",
    "connect",
    "lit",
]
