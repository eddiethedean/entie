# Troubleshooting

## `_id` and `fields`

MongoDB adds `_id` to documents. If you pass `fields=("a", "b")` to `EnteiDataFrame.from_collection`, only those keys are materialized as columns; `_id` is omitted unless you include it in `fields`. If you need the id in Python, add `"_id"` to `fields` or omit `fields` where the implementation discovers keys from documents (see API docs for your version).

## `EntieDatabase` must wrap a **Database**, not a **Collection**

`EntieDatabase` expects a PyMongo `Database`. Passing a `Collection` breaks methods like `table()` / `collection()` that index by name on the database. Create a database first, then pass `db.table("name")` into `EnteiDataFrame.from_collection` or `Records.insert_into`.

## Connection URI and `ENTIE_URI`

If you call `connect()` without `uri` and without `client=`, the default URI is read from the environment variable **`ENTIE_URI`** (see [`client.py`](https://github.com/eddiethedean/entie/blob/main/packages/entie/src/entie/client.py)). Set it in your shell or `.env` loader before running scripts.

## Empty collections and `fields`

For an empty collection, column names may not be inferable from data. Pass **`fields`** explicitly so `EnteiDataFrame` knows which columns to expect (see [entei-core `MongoRoot`](https://github.com/eddiethedean/entie/blob/main/packages/entei-core/src/entei_core/mongo_root.py) behavior).

## Tests with **mongomock**

The development extra includes **mongomock** for tests that avoid a real MongoDB server. Install editable packages with `entie[dev]` and run `pytest` from the repo root; see [Development](development.md) and [CONTRIBUTING.md](https://github.com/eddiethedean/entie/blob/main/CONTRIBUTING.md).

## Still stuck?

Open an [issue](https://github.com/eddiethedean/entie/issues) with a minimal reproducer, Python version, and `entie` / `entei-core` versions.
