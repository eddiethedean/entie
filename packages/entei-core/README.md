# entei-core

Lightweight **MongoDB root** helpers: **`MongoRoot`** wraps a PyMongo collection; **`mongo_root_to_column_dict`** / **`materialize_root_data`** turn it into columnar ``dict[str, list]``.

Depends on **`pydantable-protocol`**, **PyMongo**, and **typing-extensions** only (no native Rust stack).

For **`EnteiDataFrame`** and connection helpers, install the umbrella package **`entie`**.

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
