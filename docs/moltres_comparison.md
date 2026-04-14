# Moltres comparison

[moltres](https://github.com/eddiethedean/moltres) targets **SQL** (via database drivers); **entie** targets **MongoDB** (via PyMongo). The APIs are shaped so concepts carry across.

## Umbrella vs core

| Concept | SQL (moltres) | Mongo (entie) |
|---------|----------------|---------------|
| Umbrella package | moltres | entie |
| Core materialization | moltres-core | entei-core |

## Connection and “database”

| moltres | entie |
|---------|--------|
| `connect(dsn)` / DSN env | `connect(uri, database=...)` / **`ENTIE_URI`** |
| `Database` object | `EntieDatabase` wrapping PyMongo **`Database`** |

You always choose a **logical database name** in Mongo; collections live under it.

## Tables vs collections

| moltres | entie |
|---------|--------|
| SQL table name | Mongo **collection** name |
| `db.table("orders")` (concept) | `db.table("orders")` → PyMongo `Collection` |

`EntieDatabase.table` is an alias for `collection`, mirroring moltres wording.

## Inserts

| moltres | entie |
|---------|--------|
| `Records.from_list(rows).insert_into("table")` | Same pattern with a **collection** name string |

Rows are plain dicts; Mongo stores them as documents (with optional `_id`).

## DataFrame-style reads

| moltres | entie |
|---------|--------|
| Lazy frame over SQL result | `EnteiDataFrame.from_collection(coll, fields=...)` |
| Filter / select / collect | `filter_rows`, `select`, `collect` |

**entei-core** turns collection scans into columnar structures that `EnteiDataFrame` uses; there is no pydantable-native stack in this repo.

## Environment variables (rough parallel)

| moltres | entie |
|---------|--------|
| DSN-style env (e.g. app config) | **`ENTIE_URI`** when `uri` is omitted |

Exact variable names differ by project; always check the current `connect` docstring in [`entie.client`](https://github.com/eddiethedean/entie/blob/main/packages/entie/src/entie/client.py).

## When to use **entei-core** alone

If you only need **`MongoRoot`** / **`materialize_root_data`** and no connection helpers or `EnteiDataFrame`, depend on **`entei-core`** only. Use **`entie`** when you want the full moltres-like surface (`connect`, `Records`, dataframe API).
