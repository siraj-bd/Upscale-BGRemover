"""
Engine registry.
"""

from __future__ import annotations

from engines.birefnet import BiRefNetEngine

from engines.base import BaseEngine

ENGINES: dict[str, type[BaseEngine]] = {
    "birefnet": BiRefNetEngine,
}


def get_engine(name: str) -> BaseEngine:
    """
    Return an engine instance by name.

    Args:
        name: Engine name.

    Returns:
        BaseEngine instance.

    Raises:
        ValueError: If the engine does not exist.
    """

    try:
        return ENGINES[name]()
    except KeyError as exc:
        raise ValueError(f"Unknown engine: {name}") from exc
