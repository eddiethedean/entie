# entie documentation

**entie** is the umbrella package for MongoDB helpers in Python; **entei-core** provides low-level collection materialization. Together they mirror the split between [moltres](https://github.com/eddiethedean/moltres) (SQL) and **moltres-core**, but for MongoDB.

## Browse

| Document | Description |
|----------|-------------|
| [Getting started](getting_started.md) | Install, connect, query, insert rows |
| [API overview](api_overview.md) | Public symbols and modules |
| [Moltres comparison](moltres_comparison.md) | SQL vs Mongo API mapping |
| [Development](development.md) | Monorepo dev workflow (links to contributing guide) |
| [Troubleshooting](troubleshooting.md) | Common issues and fixes |

## Project links

- **Hosted docs:** [entie.readthedocs.io](https://entie.readthedocs.io/) (Read the Docs; see `.readthedocs.yaml`)
- **Repository:** [github.com/eddiethedean/entie](https://github.com/eddiethedean/entie)
- **PyPI:** [entie](https://pypi.org/project/entie/), [entei-core](https://pypi.org/project/entei-core/)
- **Changelog:** [CHANGELOG.md](https://github.com/eddiethedean/entie/blob/main/CHANGELOG.md) (repo root)

## Packages

| PyPI | Role |
|------|------|
| `entie` | `connect`, `EntieDatabase`, `EnteiDataFrame`, `Records`, expressions |
| `entei-core` | `MongoRoot`, `mongo_root_to_column_dict`, `materialize_root_data` |
