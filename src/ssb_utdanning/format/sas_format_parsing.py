import glob
import re
from pathlib import Path

from ssb_utdanning import logger
from ssb_utdanning.config import FORMATS_PATH
from ssb_utdanning.format.formats import UTDFORMAT_INPUT_TYPE
from ssb_utdanning.format.formats import UtdFormat


def batch_process_folder_sasfiles(
    sas_files_path: str | Path, output_path: str | Path = FORMATS_PATH
) -> None:
    """Finds all .sas files in folder, tries to extract formats from these.

    Args:
        sas_files_path (str): The path to the folder containing the .sas files.
        output_path (str): The path to the folder where the formats will be stored.
            Not including the filename itself, only the base folder.
    """
    if not isinstance(sas_files_path, Path):
        sas_files_path = Path(sas_files_path)
    if not isinstance(output_path, Path):
        output_path = Path(output_path)

    for file in glob.glob(str(sas_files_path) + "/*.sas"):
        logger.info("Processing %s.", file)
        process_single_sasfile(file, output_path)


def process_single_sasfile(
    file: str | Path, output_path: str | Path = FORMATS_PATH
) -> None:
    """Get a single .sas file from storage, extracts formats and stores to disk as timestamped jsonfiles.

    Args:
        file (str): The path to the .sas file.
        output_path (str): The path to the folder where the formats will be stored.
            Not including the filename itself, only the base folder.

    Raises:
        ValueError: If file path sent in is not a .sas file.
    """
    if not isinstance(file, Path):
        file = Path(file)
    if not isinstance(output_path, Path):
        output_path = Path(output_path)

    if not str(file).endswith(".sas"):
        raise ValueError("Dude, you gotta send in a .sas file.")
    with open(file, encoding="latin1") as sas_file:
        content = sas_file.read()
    format_content: UTDFORMAT_INPUT_TYPE
    for format_name, format_content in parse_sas_script(content).items():
        form = UtdFormat(format_content)
        form.cached = False
        form.store(format_name, output_path)


def parse_sas_script(sas_script_content: str) -> dict[str, dict[str, str]]:
    """Extract a format as a Python dictionary from a SAS script.

    Args:
        sas_script_content (str): The content of the SAS script.

    Returns:
        dict[str, dict[str, str]]: A nested dictionary containing the format-name as key,
            and the format-content as value.
    """
    formats_in_file: dict[str, dict[str, str]] = {}
    for proc_step in sas_script_content.split("proc format;")[1:]:
        proc_step = proc_step.split("run;")[0]
        for value_part in proc_step.split("value ")[1:]:
            format_name, format_content = parse_value_part(value_part)
            formats_in_file[format_name] = format_content
    if not formats_in_file:
        logger.info("%s", str(sas_script_content))
    return formats_in_file


def parse_value_part(value_part: str) -> tuple[str, dict[str, str]]:
    """Parse a single "format value part" of a sas-script.

    Args:
        value_part (str): The value part to parse.

    Returns:
        tuple[str, dict[str, str]]: A tuple containing the format-name and the format-content.
    """
    value_part = value_part.split(";")[0]
    value_part = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", value_part)
    format_content = {}
    for line in value_part.split("\n"):
        line = line.strip(" ")
        if line.startswith("$") and "=" not in line and line:
            format_name = line[1:]
        elif line.startswith("$") is False and "=" not in line and line:
            format_name = line
        elif not line:
            continue
        else:
            key = line.split("=")[0].replace("\t", "").strip().strip("'").strip('"')
            value = line.split("=")[1].replace("\t", "").strip().strip("'").strip('"')
            format_content[key] = value
    return format_name, format_content
