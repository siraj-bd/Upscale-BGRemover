"""
Base engine interface for all background removal engines.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class BaseEngine(ABC):
    """Abstract base class for all background removal engines."""

    @abstractmethod
    def load(self) -> None:
        """Load the model into memory."""

    @abstractmethod
    def predict(self, input_path: Path, output_path: Path) -> None:
        """
        Remove the background from an image.

        Args:
            input_path: Input image path.
            output_path: Output image path.
        """

    @abstractmethod
    def unload(self) -> None:
        """Release model resources."""
