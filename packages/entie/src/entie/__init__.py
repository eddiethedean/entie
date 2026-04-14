"""Public API for **entie**: MongoDB helpers built on **entei-core**.

**entei-core** provides collection-to-columnar materialization; **entie** adds
PyMongo connection helpers, bulk row inserts, a small lazy **DataFrame**-style
API, and expression helpers. Pure Python on top of PyMongo (no native stack).
"""

from __future__ import annotations

from entei_core import MongoRoot, materialize_root_data, mongo_root_to_column_dict

from .client import EntieDatabase, EntieMongoClient, connect
from .dataframe import EnteiDataFrame
from .expressions import col, column, lit
from .io import Records

__version__ = "0.2.0"

__all__ = [
    "EnteiDataFrame",
    "EntieDatabase",
    "EntieMongoClient",
    "MongoRoot",
    "Records",
    "materialize_root_data",
    "mongo_root_to_column_dict",
    "__version__",
    "col",
    "column",
    "connect",
    "lit",
]
