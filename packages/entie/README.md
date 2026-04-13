# Entie

**MongoDB helpers on [entei-core](../entei-core/)** — PyMongo plus column materialization. This package does **not** use **pydantable-native** or the pydantable Rust executor.

## Install

```bash
pip install entie
```

From the monorepo (install core first, then entie):

```bash
pip install -e ./packages/entei-core
pip install -e ./packages/entie
```

## Quick start

```python
from entie import EnteiDataFrame, connect

db = connect("mongodb://localhost:27017", database="app")
coll = db.collection("items")
coll.insert_many([{"x": 1}, {"x": 2}])

df = EnteiDataFrame.from_collection(coll)
assert df.collect(as_lists=True)["x"] == [1, 2]

filtered = df.filter_rows(lambda r: r.get("x", 0) > 1).select("x")
assert filtered.collect(as_lists=True) == {"x": [2]}
```

Connection string can be omitted if `ENTIE_URI` is set (similar to `MOLTRES_DSN` for moltres).

## What this package provides

- **`connect`** — `EntieMongoClient` / `EntieDatabase` wrappers
- **`EnteiDataFrame`** — lazy view; **`collect`**, **`filter_rows`**, **`select`** (pure Python)
- Re-exports **`MongoRoot`** and materialization helpers from **entei-core**
- **`col`**, **`lit`**, **`column`** — lightweight helpers

## License

MIT
