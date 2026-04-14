# entie

**MongoDB operations layer for Python** — the [moltres](https://github.com/eddiethedean/moltres)-shaped twin for **MongoDB** instead of SQL: connect to a database, work with collection “tables”, insert rows with **`Records`**, and run a small **DataFrame**-style API backed by **entei-core** materialization (no pydantable-native).

| | SQL stack | Mongo stack (this repo) |
|--|-----------|-------------------------|
| Umbrella | [moltres](https://github.com/eddiethedean/moltres) | **entie** |
| Core | moltres-core | **entei-core** |

## Packages

| Package | Path | Role |
|--------|------|------|
| **entei-core** | [`packages/entei-core`](packages/entei-core/) | `MongoRoot`, `mongo_root_to_column_dict` — columnar `dict[str, list]` from collections |
| **entie** | [`packages/entie`](packages/entie/) | `connect`, `EntieDatabase`, `EnteiDataFrame`, `Records`, expressions |

## Install

```bash
pip install entie
```

Editable monorepo:

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

- **Getting started**: [docs/getting_started.md](docs/getting_started.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

## Development

```bash
make test          # pytest
make lint          # ruff check
make format        # ruff format
make build         # build + twine check both packages
```

## Layout

```
packages/entei-core/   # PyPI: entei-core
packages/entie/        # PyPI: entie
docs/
.github/workflows/
Makefile
pyproject.toml         # pytest + ruff + uv workspace
```

## License

MIT — see [LICENSE](LICENSE).
