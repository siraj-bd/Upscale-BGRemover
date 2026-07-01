from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff",
}


def is_image(path: Path) -> bool:
    return path.suffix.lower() in SUPPORTED_EXTENSIONS


def collect_images(path: str):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(path)

    if path.is_file():
        if not is_image(path):
            raise ValueError(f"Unsupported image: {path}")
        return [path]

    images = sorted(
        p for p in path.rglob("*")
        if p.is_file() and is_image(p)
    )

    if not images:
        raise FileNotFoundError("No supported images found.")

    return images


def ensure_output(path: str) -> Path:
    output = Path(path)
    output.mkdir(parents=True, exist_ok=True)
    return output
