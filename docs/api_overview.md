# API overview

Public symbols are exported from **`entie`** (and re-exported **entei-core** helpers where noted). Source paths are relative to the repository root.

## Top-level (`entie`)

| Symbol | Description |
|--------|-------------|
| [`connect`](https://github.com/eddiethedean/entie/blob/main/packages/entie/src/entie/client.py) | Build an `EntieMongoClient` / `EntieDatabase` from a URI, optional `ENTIE_URI`, or an existing `MongoClient`. |
| [`EntieMongoClient`](https://github.com/eddiethedean/entie/blob/main/packages/entie/src/entie/client.py) | Thin wrapper around PyMongo’s `MongoClient`; use `database(name)` for `EntieDatabase`. |
| [`EntieDatabase`](https://github.com/eddiethedean/entie/blob/main/packages/entie/src/entie/client.py) | Holds a PyMongo **Database** (not a collection). `table` / `collection` return collections. |
| [`EnteiDataFrame`](https://github.com/eddiethedean/entie/blob/main/packages/entie/src/entie/dataframe.py) | Lazy, collection-backed frame: `from_collection`, `filter_rows`, `select`, `collect`. |
| [`Records`](https://github.com/eddiethedean/entie/blob/main/packages/entie/src/entie/io/records.py) | Row-oriented insert helper: `from_list`, `insert_into`. |
| [`col`](https://github.com/eddiethedean/entie/blob/main/packages/entie/src/entie/expressions/__init__.py) / [`column`](https://github.com/eddiethedean/entie/blob/main/packages/entie/src/entie/expressions/__init__.py) | Expression helpers for dataframe-style operations. |
| [`lit`](https://github.com/eddiethedean/entie/blob/main/packages/entie/src/entie/expressions/__init__.py) | Literal expression helper. |
| `__version__` | Package version string. |

## Re-exported from **entei-core** (via `entie`)

| Symbol | Description |
|--------|-------------|
| [`MongoRoot`](https://github.com/eddiethedean/entie/blob/main/packages/entei-core/src/entei_core/mongo_root.py) | Columnar root `dict[str, list]` plus metadata for a Mongo collection snapshot. |
| [`materialize_root_data`](https://github.com/eddiethedean/entie/blob/main/packages/entei-core/src/entei_core/_materialize.py) | Materialize documents into columnar form. |
| [`mongo_root_to_column_dict`](https://github.com/eddiethedean/entie/blob/main/packages/entei-core/src/entei_core/_materialize.py) | Convert a `MongoRoot` to a plain column dict. |

## Modules (for imports and reading source)

| Module | Role |
|--------|------|
| `entie.client` | `connect`, `EntieMongoClient`, `EntieDatabase`. |
| `entie.dataframe` | `EnteiDataFrame`. |
| `entie.io.records` | `Records`. |
| `entie.expressions` | `col`, `column`, `lit`. |
| `entei_core` | Core materialization only (also usable without `entie`). |

## See also

- [Getting started](getting_started.md) — minimal examples
- [Troubleshooting](troubleshooting.md) — `_id`, `fields`, database vs collection
- [Moltres comparison](moltres_comparison.md) — naming parallels with the SQL stack
