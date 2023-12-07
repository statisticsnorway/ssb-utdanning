import os
import glob
import re
import datetime
import json

from utd_felles.config import PROD_FORMATS_PATH



def store_format_prod(formats: dict[str, dict[str, str]],
                      output_path: str = PROD_FORMATS_PATH) -> None:
    if all([isinstance(x, dict) for x in formats.values()]):
        nested = True
    elif all([isinstance(x, str) for x in formats.values()]):
        nested = False
        format_name = input("Please specify the name of the format: ")
    else:
        raise NotImplemented("Expecting a nested or unnested dict of strings.")
               
    now = datetime.datetime.now().isoformat("T", "seconds")
    if nested:
        for format_name, format_content in formats.items():
            with open(os.path.join(output_path, f"{format_name}_{now}.json"), "w") as json_file:
                json.dump(format_content, json_file)
    elif not nested:
        with open(os.path.join(output_path, f"{format_name}_{now}.json"), "w") as json_file:
                json.dump(formats, json_file)
 

def batch_process_folder_sasfiles(sas_files_path: str, output_path: str = PROD_FORMATS_PATH) -> None:
    formats = {}
    for file in glob.glob(sas_files_path + "*.sas"):
        k, v = process_single_sasfile(file, output_path)
        formats[k] = v
        
def process_single_sasfile(file: str, output_path: str = PROD_FORMATS_PATH) -> None:
    if not file.endswith(".sas"):
        raise ValueError("Dude, you gotta send in a .sas file.)
    with open(sas_files_path + "/" + file, "r", encoding="latin1") as sas_file:
        content = sas_file.read()
    store_format_prod(parse_sas_script(content), output_path)
    
def parse_sas_script(sas_script_content: str) -> dict[str, dict[str, str]]:
    formats_in_file = {}
    for proc_step in content.split("proc format;")[1:]:
        proc_step = proc_step.split("run;")[0]
        for value_part in proc_step.split("value ")[1:]:
            value_part = value_part.split(";")[0]
            value_part = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" , value_part)
            format_content = {}
            for line in value_part.split("\n"):
                line = line.strip(" ")
                #print(line)
                if line.startswith("$") or "=" not in line and line:
                    format_name = line[1:]
                elif not line:
                    pass
                else:
                    try:
                        key = line.split("=")[0].strip(" '").strip('"')
                        value = line.split("=")[1].strip(" '").strip('"')
                        format_content[key] = value
                    except Exception as e:
                        print(file, value_part, line)
                        raise e
            formats_in_file[format_name] = format_content
    return formats_in_file