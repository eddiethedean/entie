# entie

**MongoDB helpers for Python**, built on [PyMongo](https://www.mongodb.com/docs/drivers/pymongo/). Install **`entie`** for connection utilities, bulk inserts, and a small lazy **DataFrame**-style API over collections. **`entei-core`** is the lower-level package: it materializes collection scans into columnar `dict[str, list]` data for analysis and testing.

There is no native Rust stack here—everything is pure Python on top of PyMongo and **entei-core**.

## Packages

| Package | Path | Role |
|--------|------|------|
| **entei-core** | [`packages/entei-core`](packages/entei-core/) | `MongoRoot`, `mongo_root_to_column_dict`, `materialize_root_data` |
| **entie** | [`packages/entie`](packages/entie/) | `connect`, `EntieDatabase`, `EnteiDataFrame`, `Records`, `col` / `column` / `lit` |

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

- **Read the Docs:** [entie.readthedocs.io](https://entie.readthedocs.io/) (import this repo in RTD with slug `entie` to enable builds)
- **Index** (Markdown in repo): [docs/index.md](docs/index.md)
- **Tutorial**: [docs/getting_started.md](docs/getting_started.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

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

MIT — see [LICENSE](LICENSE).
