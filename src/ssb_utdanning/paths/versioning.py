from pathlib import Path
from string import digits

from cloudpathlib import CloudPath


def get_version(path: str | Path | CloudPath) -> int:
    version = str(path).split(".")[0].split("_")[-1]
    if version.startswith("v"):
        version = version[1:]
        if not version.isdigit():
            error_msg = f"{version} is not a digit, cant bump."
            raise ValueError(error_msg)
    return int(version)


def bump_path(path: str | Path | CloudPath, n: int = 1) -> str | Path | CloudPath:
    new_version = get_version(path) + n
    if isinstance(path, str):
        undersc_parts = path.split(".")[0].split("_")[:-1]
        undersc_parts += [f"v{new_version}"]
        return "_".join(undersc_parts) + "." + path.split(".")[1]
    return path.parent / (path.stem.rstrip(digits) + str(new_version) + path.suffix)
