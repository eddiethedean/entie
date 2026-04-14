# entei-core

[![PyPI version](https://img.shields.io/pypi/v/entei-core.svg)](https://pypi.org/project/entei-core/)

Lightweight **MongoDB root** helpers: **`MongoRoot`** wraps a PyMongo collection; **`mongo_root_to_column_dict`** / **`materialize_root_data`** turn it into columnar ``dict[str, list]``.

Depends on **`pydantable-protocol`**, **PyMongo**, and **typing-extensions** only (no native Rust stack).

| Use case | Package |
|----------|---------|
| Columnar materialization only, minimal deps | **`entei-core`** (this package) |
| `connect`, `EnteiDataFrame`, `Records`, expressions | Install **`entie`** ([PyPI](https://pypi.org/project/entie/)) — it depends on **entei-core** |

- **Documentation:** [entie.readthedocs.io](https://entie.readthedocs.io/)
- **Changelog:** [CHANGELOG](https://github.com/eddiethedean/entie/blob/main/CHANGELOG.md)

## Install

```bash
pip install entei-core
```

From the monorepo (editable):

```bash
pip install -e ./packages/entei-core
```

## Quick example

```python
import mongomock
from entei_core import MongoRoot, mongo_root_to_column_dict

client = mongomock.MongoClient()
coll = client.db.items
coll.insert_many([{"x": 1}, {"x": 2}])

cols = mongo_root_to_column_dict(MongoRoot(coll))
assert cols == {"x": [1, 2]}
```

## Versioning

Track **pydantable-protocol** minor lines you test against (see pydantable’s VERSIONING docs).
