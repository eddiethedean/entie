# entie

**MongoDB table helpers** on [**entei-core**](../entei-core/): `connect`, **`EntieDatabase`** / **`EntieMongoClient`**, **`EnteiDataFrame`**, **`Records`**, and **`col` / `lit` / `column`**.

Aligned with [moltres](https://github.com/eddiethedean/moltres) ergonomics (`connect`, `table`, `Records.insert_into`) for document databases — **no** pydantable-native.

## Install

```bash
pip install entie
```

From the monorepo:

```bash
pip install -e ../entei-core
pip install -e .
```

## Features

- **`connect`** — PyMongo entrypoint; `ENTIE_URI` when `uri` is omitted (like `MOLTRES_DSN`).
- **`EntieDatabase.table` / `.collection`** — access a collection; **`tables()`** lists names.
- **`EnteiDataFrame`** — lazy read + `filter_rows` + `select` + `collect` (pure Python).
- **`Records.from_list(..., database=db).insert_into("name")`** — bulk insert (moltres-style).
- Re-exports **`MongoRoot`** and materialization helpers from **entei-core**.

## Example

```python
from entie import EnteiDataFrame, Records, connect

db = connect("mongodb://localhost:27017", database="app")

Records.from_list([{"x": 1}], database=db).insert_into("items")

df = EnteiDataFrame.from_collection(db.table("items"), fields=("x",))
df.collect(as_lists=True)  # {"x": [1]}  (+ Mongo _id if fields not fixed)
```

## License

MIT
