"""entei-core: MongoDB collection roots and columnar ``dict[str, list]`` materialization.

Exports :class:`MongoRoot`, :func:`mongo_root_to_column_dict`, and
:func:`materialize_root_data` for building columnar data from PyMongo collections
without a native extension stack.
"""

from __future__ import annotations

from ._materialize import materialize_root_data, mongo_root_to_column_dict
from .mongo_root import MongoRoot

__all__ = [
    "MongoRoot",
    "materialize_root_data",
    "mongo_root_to_column_dict",
    "__version__",
]

__version__ = "0.2.0"
