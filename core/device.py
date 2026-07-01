import platform
import torch


def get_device() -> torch.device:
    """
    Select the best available compute device.
    """

    if torch.backends.mps.is_available():
        return torch.device("mps")

    if torch.cuda.is_available():
        return torch.device("cuda")

    return torch.device("cpu")


def get_device_name() -> str:
    """
    Return a human-readable device name.

    Returns:
        str: Device description.
    """

    device = get_device()

    if device.type == "mps":
        return f"Apple Silicon ({platform.machine()})"

    if device.type == "cuda":
        return torch.cuda.get_device_name(0)

    return "CPU"
