.PHONY: help test lint format format-check build build-check install-editable clean

help:
	@echo "entie monorepo — see https://github.com/eddiethedean/moltres for the SQL sibling project."
	@echo ""
	@echo "  make install-editable  pip install -e packages (entei-core then entie)"
	@echo "  make test              pytest (from repo root)"
	@echo "  make lint              ruff check packages/*/src"
	@echo "  make format            ruff format packages/*/src"
	@echo "  make format-check      ruff format --check"
	@echo "  make build             python -m build + twine check each package"
	@echo "  make clean             remove dist/ and build/ under packages/*"

install-editable:
	python -m pip install -e ./packages/entei-core -e "./packages/entie[dev]"

test:
	pytest

lint:
	ruff check packages/entei-core/src packages/entie/src

format:
	ruff format packages/entei-core/src packages/entie/src

format-check:
	ruff format --check packages/entei-core/src packages/entie/src

build-check: build

build:
	cd packages/entei-core && rm -rf dist build && python -m build && python -m twine check dist/*
	cd packages/entie && rm -rf dist build && python -m build && python -m twine check dist/*

clean:
	rm -rf packages/entei-core/dist packages/entei-core/build packages/entie/dist packages/entie/build
