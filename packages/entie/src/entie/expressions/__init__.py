"""Small helpers for column names and literals (optional ergonomic use with APIs that expect names)."""

from __future__ import annotations

from typing import Any


def col(name: str) -> str:
    """Return ``name`` unchanged (readable ``select(col("x"))``-style spelling).

    Parameters
    ----------
    name:
        Column / field name.

    Returns
    -------
    str
        The same string ``name``.
    """
    return name


def column(name: str) -> str:
    """Alias of :func:`col`.

    Parameters
    ----------
    name:
        Column / field name.

    Returns
    -------
    str
        The same string ``name``.
    """
    return name


def lit(value: Any) -> Any:
    """Return ``value`` unchanged (placeholder for literal-friendly APIs).

    Parameters
    ----------
    value:
        Any object.

    Returns
    -------
    Any
        The input ``value``.
    """
    return value


__all__ = ["col", "column", "lit"]
