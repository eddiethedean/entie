# Changelog

All notable changes to this project are documented here. Versions follow the
tags on this repository; **entei-core** and **entie** release versions are kept
in lockstep (same as [moltres](https://github.com/eddiethedean/moltres) /
moltres-core).

## Unreleased

Nothing yet.

## 0.2.0

PyPI alignment: **entie** depends on **entei-core>=0.2.0,<2**. Both packages ship at the same version.

### Documentation

- Documentation hub ([`docs/index.md`](docs/index.md)), getting started, API overview, troubleshooting, development guide, moltres comparison (historical naming), and **roadmap**.
- **MkDocs** (Material) + **mkdocstrings** at repo root; **Read the Docs** ([`.readthedocs.yaml`](.readthedocs.yaml)).
- **README** and package READMEs: badges, Read the Docs links, PyPI `project.urls.Documentation`.
- Expanded **NumPy-style docstrings** across public APIs in `entie` and `entei_core`.

### CI and tooling

- **Ruff** (lint/format), **pytest** with 100% line coverage gate, **`ty`** typecheck on library and tests.
- **`mkdocs build --strict`** and optional **GitHub Pages** docs workflow.
- **`entie[dev]`** includes `ty`; **`entie[docs]`** includes MkDocs stack.

### Fixed and changed

- **Breaking:** `EnteiDataFrame.from_collection(..., fields=[])` or `fields=()` means **no columns** for materialization. Previously an empty sequence was treated like “infer all keys” because `()` was falsy in the materializer (`root.fields is not None` is now used consistently).
- **`connect()`** raises if both `uri` and `client` are passed.
- **`MongoRoot`** rejects duplicate names in `fields`.
- **`EnteiDataFrame.select()`** rejects duplicate column names.

## 0.1.0

- Initial **entei-core**: `MongoRoot`, `mongo_root_to_column_dict`,
  `materialize_root_data` (PyMongo + pydantable-protocol).
- Initial **entie**: `connect`, `EntieDatabase` / `EntieMongoClient`, `EnteiDataFrame`,
  `Records`, `col` / `lit` / `column`, pure-Python filter/select on collect.
