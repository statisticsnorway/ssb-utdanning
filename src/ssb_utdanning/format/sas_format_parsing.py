import glob
import re

from ssb_utdanning.config import PROD_FORMATS_PATH
from ssb_utdanning.format.formats import UTDFORMAT_INPUT_TYPE
from ssb_utdanning.format.formats import UtdFormat


def batch_process_folder_sasfiles(
    sas_files_path: str, output_path: str = PROD_FORMATS_PATH
) -> None:
    """Finds all .sas files in folder, tries to extract formats from these.

    Parameters
    ----------
    sas_files_path: str
        The path to the folder containing the .sas files.
    output_path: str
        The path to the folder where the formats will be stored.
        Not including the filename itself, only the base folder.

    Returns:
    -------
    None
        Only writes to disk (side effect).
    """
    for file in glob.glob(sas_files_path + "*.sas"):
        print(f"Processing {file}.")
        process_single_sasfile(file, output_path)


def process_single_sasfile(file: str, output_path: str = PROD_FORMATS_PATH) -> None:
    """Get a single .sas file from storage, extracts formats and stores to disk as timestamped jsonfiles.

    Parameters
    ----------
    file: str
        The path to the .sas file.
    output_path: str
        The path to the folder where the formats will be stored.
        Not including the filename itself, only the base folder.

    Returns:
    -------
    None
        Only writes to disk (side effect).

    Raises:
    ------
    ValueError
        If the file is not a .sas file.
    """
    if not file.endswith(".sas"):
        raise ValueError("Dude, you gotta send in a .sas file.")
    with open(file, encoding="latin1") as sas_file:
        content = sas_file.read()
    format_content: UTDFORMAT_INPUT_TYPE
    for format_name, format_content in parse_sas_script(content).items():
        # print(format_name, format_content)
        form = UtdFormat(format_content)
        form.cached = False
        form.store(format_name)


def parse_sas_script(sas_script_content: str) -> dict[str, dict[str, str]]:
    """Extract a format as a Python dictionary from a SAS script.

    Parameters
    ----------
    sas_script_content: str
        The content of the SAS script.

    Returns:
    -------
    dict[str, dict[str, str]]
        A nested dictionary containing the format-name as key, and the format-content as value.
    """
    formats_in_file: dict[str, dict[str, str]] = {}
    for proc_step in sas_script_content.split("proc format;")[1:]:
        proc_step = proc_step.split("run;")[0]
        for value_part in proc_step.split("value ")[1:]:
            value_part = value_part.split(";")[0]
            value_part = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", value_part)
            format_content = {}
            for line in value_part.split("\n"):
                line = line.strip(" ")
                # print(line)
                if line.startswith("$") or "=" not in line and line:
                    format_name = line[1:]
                elif not line:
                    pass
                else:
                    try:
                        key = (
                            line.split("=")[0]
                            .replace("\t", "")
                            .strip()
                            .strip("'")
                            .strip('"')
                        )
                        value = (
                            line.split("=")[1]
                            .replace("\t", "")
                            .strip()
                            .strip("'")
                            .strip('"')
                        )
                        format_content[key] = value
                    except Exception as e:
                        print(value_part, line)
                        raise e
            formats_in_file[format_name] = format_content
    if formats_in_file:
        # print(formats_in_file)
        ...
    else:
        print(sas_script_content)
    return formats_in_file
