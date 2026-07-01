from pathlib import Path


def output_filename(input_file: Path, output_dir: Path) -> Path:
    """
    Generate output filename.

    Example:
        image.jpg -> image.png
    """
    return output_dir / f"{input_file.stem}.png"


def print_header():
    print("=" * 60)
    print("BGroundRemover")
    print("Professional AI Background Removal")
    print("=" * 60)
