# Contributing

Thanks for helping improve **entie** and **entei-core**.

## Setup

```bash
pip install -e ./packages/entei-core -e "./packages/entie[dev]"
```

Run tests from the repository root:

```bash
pytest
```

Lint and format (see also `Makefile`):

```bash
ruff check packages/entei-core/src packages/entie/src
ruff format packages/entei-core/src packages/entie/src
```

## Design notes

This project is the MongoDB-oriented counterpart to
[moltres](https://github.com/eddiethedean/moltres) (SQL + moltres-core). Prefer
APIs and module names that feel familiar to moltres users (`connect`, `Records`,
`insert_into`, `table`, etc.), adapted for document collections rather than SQL
tables.

## Releases

- Bump **both** `packages/entei-core/pyproject.toml` and `packages/entie/pyproject.toml`
  to the same `[project].version`.
- Tag `vX.Y.Z` and push; the release workflow builds both packages and uploads
  to PyPI (requires `PYPI_API_TOKEN`).
