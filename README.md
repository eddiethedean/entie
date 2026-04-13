# entie (monorepo)

Python packages for MongoDB column materialization and helpers:

| Package | Path | Description |
|--------|------|-------------|
| **entei-core** | [`packages/entei-core`](packages/entei-core/) | `MongoRoot`, columnar materialization (`pydantable-protocol` + PyMongo) |
| **entie** | [`packages/entie`](packages/entie/) | Connection helpers, `EnteiDataFrame`, re-exports |

## Development

Install both packages in editable mode (core first):

```bash
pip install -e ./packages/entei-core
pip install -e ./packages/entie
```

Or with [uv](https://docs.astral.sh/uv/) (workspace members are declared in root `pyproject.toml`):

```bash
uv sync
```

Run tests from the repository root:

```bash
pytest
```

## Layout

```
packages/
  entei-core/
    pyproject.toml
    README.md
    src/entei_core/
    tests/
  entie/
    pyproject.toml
    README.md
    src/entie/
    tests/
pyproject.toml   # pytest, ruff, uv workspace
README.md        # this file
```

## License

MIT
