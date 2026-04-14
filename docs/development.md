# Development

Work happens in this **monorepo**: `packages/entei-core` and `packages/entie` are separate distributions with aligned versions.

## Quick setup

```bash
pip install -e ./packages/entei-core -e "./packages/entie[dev]"
pytest
```

From the repository root, **pytest** runs with the coverage configuration in the root [`pyproject.toml`](https://github.com/eddiethedean/entie/blob/main/pyproject.toml) (100% line coverage gate on library code).

## Make targets

See the root [README — Development](https://github.com/eddiethedean/entie/blob/main/README.md#development) for `make test`, `make lint`, `make format`, `make coverage-html`, and `make build`.

## Canonical contributor guide

**Commands, releases, design notes, and the documentation checklist** live in **[CONTRIBUTING.md](https://github.com/eddiethedean/entie/blob/main/CONTRIBUTING.md)**. Prefer that file as the single source of truth so CI and docs stay aligned.

## Documentation site

**Read the Docs** builds from [`.readthedocs.yaml`](https://github.com/eddiethedean/entie/blob/main/.readthedocs.yaml) using the root [`mkdocs.yml`](https://github.com/eddiethedean/entie/blob/main/mkdocs.yml). Connect the GitHub repository in the RTD dashboard (project slug `entie` matches the published URL).

Local build (same as CI):

```bash
pip install -e ./packages/entei-core -e "./packages/entie[docs]"
mkdocs build --strict
```

See [docs/index.md](index.md) for the table of contents of Markdown docs.
