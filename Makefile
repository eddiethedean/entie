.PHONY: help test coverage coverage-html lint format format-check build build-check install-editable clean

help:
	@echo "entie monorepo — see https://github.com/eddiethedean/moltres for the SQL sibling project."
	@echo ""
	@echo "  make install-editable  pip install -e packages (entei-core then entie)"
	@echo "  make test              pytest with coverage (100% line gate)"
	@echo "  make coverage          pytest with coverage (requires pytest-cov; see entie[dev])"
	@echo "  make coverage-html       same + htmlcov/"
	@echo "  make lint              ruff check packages/*/src"
	@echo "  make format            ruff format packages/*/src"
	@echo "  make format-check      ruff format --check"
	@echo "  make build             python -m build + twine check each package"
	@echo "  make clean             remove dist/ and build/ under packages/*"

install-editable:
	python -m pip install -e ./packages/entei-core -e "./packages/entie[dev]"

test:
	pytest

coverage:
	pytest --cov=packages/entei-core/src/entei_core --cov=packages/entie/src/entie --cov-report=term-missing --cov-fail-under=100

coverage-html:
	pytest --cov=packages/entei-core/src/entei_core --cov=packages/entie/src/entie --cov-report=term-missing --cov-report=html --cov-fail-under=100

lint:
	ruff check packages/entei-core/src packages/entie/src packages/entei-core/tests packages/entie/tests

format:
	ruff format packages/entei-core/src packages/entie/src packages/entei-core/tests packages/entie/tests

format-check:
	ruff format --check packages/entei-core/src packages/entie/src packages/entei-core/tests packages/entie/tests

build-check: build

build:
	cd packages/entei-core && rm -rf dist build && python -m build && python -m twine check dist/*
	cd packages/entie && rm -rf dist build && python -m build && python -m twine check dist/*

clean:
	rm -rf packages/entei-core/dist packages/entei-core/build packages/entie/dist packages/entie/build
