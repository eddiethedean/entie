"""Tests for entie.expressions helpers."""

from __future__ import annotations

from entie.expressions import col, column, lit


def test_col_and_column() -> None:
    assert col("a") == "a"
    assert column("b") == "b"


def test_lit() -> None:
    assert lit(42) == 42
    assert lit("s") == "s"
