from pathlib import Path


class BackgroundEngine:
    def __init__(self, engine: str = "birefnet"):
        self.engine = engine

    def load(self) -> None:
        print(f"Loading engine: {self.engine}")

    def remove(self, input_path: str, output_dir: str) -> Path:
        input_path = Path(input_path)
        output_dir = Path(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"Input : {input_path}")
        print(f"Output: {output_dir}")

        # TODO: Implement BiRefNet inference.

        return output_dir
