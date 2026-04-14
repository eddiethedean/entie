# Changelog

All notable changes to this project are documented here. Versions follow the
tags on this repository; **entei-core** and **entie** release versions are kept
in lockstep (same as [moltres](https://github.com/eddiethedean/moltres) /
moltres-core).

## Unreleased

- **Breaking:** `EnteiDataFrame.from_collection(..., fields=[])` (or `fields=()`)
  now means “no columns” for materialization. Previously an empty sequence was
  treated like “infer all keys” because `()` was falsy in the materializer.
- `connect()` raises if both `uri` and `client` are passed.
- `MongoRoot` rejects duplicate names in `fields`.
- `EnteiDataFrame.select()` rejects duplicate column names.

## 0.2.0

- Version alignment for PyPI / release workflow; dependency **entie** → **entei-core>=0.2.0**.

## 0.1.0

- Initial **entei-core**: `MongoRoot`, `mongo_root_to_column_dict`,
  `materialize_root_data` (PyMongo + pydantable-protocol).
- Initial **entie**: `connect`, `EntieDatabase` / `EntieMongoClient`, `EnteiDataFrame`,
  `Records`, `col` / `lit` / `column`, pure-Python filter/select on collect.
