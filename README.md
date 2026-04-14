# entie

[![Documentation Status](https://readthedocs.org/projects/entie/badge/?version=latest)](https://entie.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://img.shields.io/pypi/v/entie.svg)](https://pypi.org/project/entie/)
[![Python versions](https://img.shields.io/pypi/pyversions/entie.svg)](https://pypi.org/project/entie/)
[![CI](https://github.com/eddiethedean/entie/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/eddiethedean/entie/actions/workflows/ci.yml?query=branch%3Amain)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/eddiethedean/entie/blob/main/LICENSE)

**MongoDB helpers for Python**, built on [PyMongo](https://www.mongodb.com/docs/drivers/pymongo/). Install **`entie`** for connection utilities, bulk inserts, and a small lazy **DataFrame**-style API over collections. **`entei-core`** is the lower-level package: it materializes collection scans into columnar `dict[str, list]` data for analysis and testing.

There is no native Rust stack here—everything is pure Python on top of PyMongo and **entei-core**.

## Packages

| Package | Path | Role |
|--------|------|------|
| **entei-core** | [`packages/entei-core`](https://github.com/eddiethedean/entie/tree/main/packages/entei-core) | `MongoRoot`, `mongo_root_to_column_dict`, `materialize_root_data` |
| **entie** | [`packages/entie`](https://github.com/eddiethedean/entie/tree/main/packages/entie) | `connect`, `EntieDatabase`, `EnteiDataFrame`, `Records`, `col` / `column` / `lit` |

## Install

```bash
pip install entie
```

From a clone of this repository (editable install for contributors):

```bash
pip install -e ./packages/entei-core
pip install -e "./packages/entie[dev]"
```

## Quick start

```python
from entie import EnteiDataFrame, Records, connect

db = connect("mongodb://localhost:27017", database="app")

Records.from_list(
    [{"sku": "a1", "qty": 2}],
    database=db,
).insert_into("inventory")

df = EnteiDataFrame.from_collection(db.table("inventory"), fields=("sku", "qty"))
print(df.collect(as_lists=True))
```

Use `ENTIE_URI` when you omit the URI in `connect()`—set it in your environment the same way you would pass `uri=...` explicitly.

## Documentation

Hosted on **Read the Docs**: [entie.readthedocs.io](https://entie.readthedocs.io/en/latest/)

| | |
|--|--|
| **Home** | [entie.readthedocs.io/en/latest/](https://entie.readthedocs.io/en/latest/) |
| **Getting started** | […/getting_started/](https://entie.readthedocs.io/en/latest/getting_started/) |
| **API overview** | […/api_overview/](https://entie.readthedocs.io/en/latest/api_overview/) |
| **Troubleshooting** | […/troubleshooting/](https://entie.readthedocs.io/en/latest/troubleshooting/) |
| **Development** | […/development/](https://entie.readthedocs.io/en/latest/development/) |
| **Moltres comparison** | […/moltres_comparison/](https://entie.readthedocs.io/en/latest/moltres_comparison/) |
| **Roadmap** | […/roadmap/](https://entie.readthedocs.io/en/latest/roadmap/) |
| **Code reference** | [entie](https://entie.readthedocs.io/en/latest/reference/entie/) · [entei_core](https://entie.readthedocs.io/en/latest/reference/entei_core/) |

Repository files: [CHANGELOG](https://github.com/eddiethedean/entie/blob/main/CHANGELOG.md) · [CONTRIBUTING](https://github.com/eddiethedean/entie/blob/main/CONTRIBUTING.md) (detailed commands; the **Development** doc above links here).

## Development

```bash
make test           # pytest (100% line coverage gate via pytest-cov)
make coverage-html  # HTML report in htmlcov/
make lint           # ruff check (src + tests)
make format         # ruff format
make build          # build + twine check both packages
```

## Repository layout

```
packages/entei-core/   # PyPI: entei-core
packages/entie/        # PyPI: entie
docs/
.github/workflows/
Makefile
pyproject.toml         # pytest, ruff, uv workspace
```

## License

MIT — see [LICENSE](https://github.com/eddiethedean/entie/blob/main/LICENSE).
