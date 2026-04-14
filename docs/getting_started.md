# Getting started with entie

**entie** is the umbrella package; **entei-core** holds MongoDB root
materialization. Together they mirror the split between
[moltres](https://github.com/eddiethedean/moltres) and **moltres-core**, but for
MongoDB instead of SQL.

## Install

```bash
pip install entie
```

This installs **entie** and pulls in **entei-core** and **PyMongo**.

## Connect

Like moltres `connect(dsn)`, use a MongoDB URI or pass a client. The environment
variable `ENTIE_URI` is read when `uri` is omitted (similar to `MOLTRES_DSN`).

```python
from entie import connect

db = connect("mongodb://localhost:27017", database="app")
# or: connect(client=existing_client, database="app")
```

## Query with EnteiDataFrame

`EnteiDataFrame` is a small lazy view: it reads the collection through
**entei-core**, then applies Python `filter_rows` / `select` before `collect`.

```python
from entie import EnteiDataFrame

coll = db.table("orders")
df = EnteiDataFrame.from_collection(coll, fields=("amount", "country"))
result = (
    df.filter_rows(lambda r: (r.get("amount") or 0) > 100)
    .select("amount", "country")
    .collect(as_lists=True)
)
```

## Insert rows (Records)

Same idea as moltres `Records.from_list(...).insert_into("table")`, using a
MongoDB collection name:

```python
from entie import Records

Records.from_list(
    [{"name": "Alice"}, {"name": "Bob"}],
    database=db,
).insert_into("users")
```

## entei-core only

If you only need column materialization (no `entie` helpers):

```python
from entei_core import MongoRoot, mongo_root_to_column_dict

cols = mongo_root_to_column_dict(MongoRoot(collection))
```

See each package’s README under `packages/` for full API details.
