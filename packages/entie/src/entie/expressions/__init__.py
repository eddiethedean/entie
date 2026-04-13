"""Lightweight column / literal helpers (no pydantable dependency)."""

from __future__ import annotations

from typing import Any


def col(name: str) -> str:
    """Return a column name (string identity; for familiar ``select(col(\"x\"))`` style)."""
    return name


def column(name: str) -> str:
    """Alias of :func:`col`."""
    return name


def lit(value: Any) -> Any:
    """Return a literal value unchanged."""
    return value


__all__ = ["col", "column", "lit"]
