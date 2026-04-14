"""Smoke tests for package exports and version (coverage on __init__ modules)."""

from __future__ import annotations

import entei_core
import entie
from entie.io import Records


def test_entei_core_version_and_exports() -> None:
    assert isinstance(entei_core.__version__, str)
    assert entei_core.MongoRoot is not None
    assert entei_core.mongo_root_to_column_dict is not None
    assert entei_core.materialize_root_data is not None


def test_entie_version_and_public_api() -> None:
    assert isinstance(entie.__version__, str)
    assert entie.connect is not None
    assert entie.EnteiDataFrame is not None
    assert entie.Records is not None
    assert Records is entie.Records
