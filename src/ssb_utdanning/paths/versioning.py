from pathlib import Path
from string import digits

from cloudpathlib import CloudPath


def get_version(path: str | Path | CloudPath) -> int:
    """Extracts version number.
    
    Extracts the version number from a file path where the version is expected to be encoded
    in the filename, typically at the end of the filename just before the file extension and
    prefixed by 'v'. For example, in 'file_v2.txt', the version number is 2.

    Args:
        path (Union[str, Path, CloudPath]): The file path or path object. The path can be a string, 
                                            or an object from pathlib.Path or a cloud path object that 
                                            implements similar functionality.

    Returns:
        int: The version number extracted from the file name.

    Examples:
        - Given a path 'folder/subfolder/file_v10.txt', it will return 10.
        - Given a path 'dataset_v3.parquet', it will return 3.

    Note:
        The function is dependent on a strict naming convention and will not correctly interpret
        file names that do not follow the expected pattern ('prefix_v<number>.extension'). It will
        raise an error if the version part is malformed or absent.
    """
    version = str(path).split(".")[0].split("_")[-1]
    if version.startswith("v"):
        version = version[1:]
        if not version.isdigit():
            error_msg = f"{version} is not a digit, cant bump."
            raise ValueError(error_msg)
    return int(version)


def bump_path(path: str | Path | CloudPath, n: int = 1) -> str | Path | CloudPath:
    """Bumps version.
    
    Increments the version number encoded in the file name of the specified path by a given amount. The version number is expected
    to be at the end of the filename, immediately preceding the file extension and prefixed with 'v', such as 'file_v2.txt'. 

    This function can handle both string paths and Path-like objects (pathlib.Path, CloudPath), updating the version accordingly.

    Args:
        path (Union[str, Path, CloudPath]): The original file path whose version needs to be incremented. Can be a string or
                                            a Path-like object.
        n int: The amount by which the version number should be incremented. Defaults to 1.

    Returns:
        Union[str, Path, CloudPath]: The new file path with the incremented version number. The type of the returned path matches
                                     the type of the input path.

    Examples:
        - Given a path 'data/file_v2.txt' and n=1, it returns 'data/file_v3.txt'.
        - For a pathlib.Path object representing 'output/report_v12.csv' and n=2, it returns a Path object for 'output/report_v14.csv'.

    Note:
        The function assumes that the file name ends with a version number formatted as '_v<number>'. If this is not the case,
        a ValueError is raised. It also assumes that the file name contains only one period, which separates the name from the extension.
    """
    new_version = get_version(path) + n
    if isinstance(path, str):
        undersc_parts = path.split(".")[0].split("_")[:-1]
        undersc_parts += [f"v{new_version}"]
        return "_".join(undersc_parts) + "." + path.split(".")[1]
    return path.parent / (path.stem.rstrip(digits) + str(new_version) + path.suffix)
