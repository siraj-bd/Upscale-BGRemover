from pathlib import Path

import torch

from .base import BaseEngine
from core.device import get_device

import sys

ROOT = Path(__file__).resolve().parent.parent
BIREFNET_ROOT = ROOT / "BiRefNet"

if str(BIREFNET_ROOT) not in sys.path:
    sys.path.insert(0, str(BIREFNET_ROOT))

from models.birefnet import BiRefNet


class BiRefNetEngine(BaseEngine):
    """
    BiRefNet inference engine.
    """

    name = "birefnet"

    def __init__(self):
        self.device = get_device()
        self.model = None

    def load(self):
        if self.model is not None:
            return

        print(f"Loading BiRefNet on {self.device}...")

        # Official BiRefNet loading will be connected here.
        self.model = True

    def remove(self, input_path, output_path):
        self.load()

        input_path = Path(input_path)
        output_path = Path(output_path)

        print(f"Input : {input_path}")
        print(f"Output: {output_path}")

        raise NotImplementedError(
            "BiRefNet inference is not connected yet."
        )
