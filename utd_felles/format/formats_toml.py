"""""Formats" at SSB is a kind of dictionary which can switch between values in cells.
Sometime aggregate numbers up, and even create categories within previews/tables."""


import toml
import os
import re


def load_formater(path: str = None) -> dict[dict]:
    """A function for loading a toml-file to a dict really..."""
    if not path:
        curr_dir = os.getcwd()
        for _ in range(40):
            if "formater.toml" in os.listdir():
                formater = toml.load("formater.toml")
                os.chdir(curr_dir)
                break
            os.chdir("../")
        else:
            raise IOError("Couldnt find format-file")
    elif path:
        formater = toml.load(path)
    print(formater.keys())
    return formater


def toml_from_proc_format(text: str, path: str) -> dict[dict]:
    result = parse_proc_format(text)
    with open(path, "w") as toml_location:
        toml.dump(result, toml_location)
    return result


def parse_proc_format(text: str) -> dict[dict]:
    result = (re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" , text)
             .replace("\t","")
             .replace("(notsorted)","")
             .replace("VALUE $","[")
             .replace("PROC FORMAT", "")
             .replace("RUN;", "")
             .replace(";", ""))
    new_result = ""
    for line in result.split("\n"):
        #print(line)
        line = line.strip()
        if len(line) > 0:
            if line[0] == "[":
                line = "\n" + line.lower() + "]"
                new_result += line + "\n"
            else:
                keys = line.split("=")[0].strip().split(",")
                for key in keys:
                    new_key = key.lower().replace("'","").replace('"',"").strip()
                    if new_key == "":
                        new_key = " "
                    new_result += ('"' + new_key  + '" =' + "=".join(line.split("=")[1:]) + "\n")
    return toml.loads(new_result)


