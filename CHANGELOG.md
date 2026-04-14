# Changelog

All notable changes to this project are documented here. Versions follow the
tags on this repository; **entei-core** and **entie** release versions are kept
in lockstep (same as [moltres](https://github.com/eddiethedean/moltres) /
moltres-core).

## 0.2.0

- Version alignment for PyPI / release workflow; dependency **entie** → **entei-core>=0.2.0**.

## 0.1.0

- Initial **entei-core**: `MongoRoot`, `mongo_root_to_column_dict`,
  `materialize_root_data` (PyMongo + pydantable-protocol).
- Initial **entie**: `connect`, `EntieDatabase` / `EntieMongoClient`, `EnteiDataFrame`,
  `Records`, `col` / `lit` / `column`, pure-Python filter/select on collect.
