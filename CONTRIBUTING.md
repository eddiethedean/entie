# Contributing

Thanks for helping improve **entie** and **entei-core**.

## Setup

```bash
pip install -e ./packages/entei-core -e "./packages/entie[dev]"
```

Run tests from the repository root (includes **pytest-cov** and **100% line coverage** gate via [pyproject.toml](pyproject.toml)):

```bash
pytest
```

HTML report: `make coverage-html` (writes `htmlcov/`).

Lint, format, and type-check (same paths as [Makefile](Makefile) and CI):

```bash
make lint          # ruff check on src + tests
make format        # ruff format on src + tests
```

Or explicitly:

```bash
ruff check packages/entei-core/src packages/entie/src packages/entei-core/tests packages/entie/tests
ruff format packages/entei-core/src packages/entie/src packages/entei-core/tests packages/entie/tests
ty check packages/entei-core/src packages/entie/src packages/entei-core/tests packages/entie/tests
```

## Documentation checklist

When you change **public API** behavior or signatures:

1. Update **docstrings** in `packages/*/src/`.
2. Update **[CHANGELOG.md](CHANGELOG.md)** under a new or unreleased section.
3. Update relevant **[docs/](docs/)** pages (API overview, getting started, troubleshooting) if users need new guidance.
4. If you add optional **docs-site** dependencies, run `mkdocs build --strict` locally before pushing.

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
