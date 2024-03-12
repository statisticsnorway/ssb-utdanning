def get_version(path: str) -> int:
    fileparts = path.split("/")
    filename = file_parts[-1]
    filename_ext = filename.split(".")
    filename_parts = filename_ext[0].split("_")
    version = filename_parts[-1]
    if version.startswith("v"):
            version = version[1:]
        if not version.isdigit():
            error_msg = f"{version} is not a digit, cant bump."
            raise ValueError(error_msg)
    return int(version)

def bump_path(path: str, n: int = 1) -> str:
    new_version = get_version(path) + n
    undersc_parts = path.split(".")[0].split("_")[:-1]
    undersc_parts += [f"v{new_version}", path.split(".")[1]]
    return "/".join(undersc_parts)
    