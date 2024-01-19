import os
from pathlib import Path


def create_folder_w_sasfiles(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    os.makedirs(path, exist_ok=True)

    # writing format 1 to sas file
    filename1 = "testfrmt1.sas"
    frmt1_dict = {"0": "00", "1": "01", "2": "02", ".": "NaN"}
    frmt1 = open(path / filename1, "w")
    frmt1.write("proc format;\n")
    frmt1.write("*-- formatnavn --*; \n")
    frmt1.write("value frmt1\n")
    for i in range(3):
        frmt1.write(f"  {i} = '0{i}'\n")
    frmt1.write(f"  . = 'NaN'\n")
    frmt1.write(";\n")

    # adding second format to first file
    frmt2_dict = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
        "key4": "value4",
    }
    frmt1.write("\n")
    frmt1.write("*-- formatnavn --*; \n")
    # testing that the parsing function can handle a '$' in front of format name
    frmt1.write("value $frmt2\n")
    for i in range(1, 5):
        frmt1.write(f"  'key{i}' = 'value{i}'\n")
    frmt1.write(";\n")
    frmt1.write("run;\n")
    frmt1.close()

    # writing two new formats to second sas file
    filename2 = "testfrmt2.sas"
    frmt3_dict = {"5": "05", "6": "06", "7": "07", "8": "08", "9": "09", ".": "NaN"}
    frmt2 = open(path / filename2, "w")
    frmt2.write("proc format;\n")
    frmt2.write("*-- formatnavn --*; \n")
    # testing that the parsing function can handle a '$' in front of format name
    frmt2.write("value $frmt3\n")
    for i in range(5, 10):
        frmt2.write(f"  {i} = '0{i}'\n")
    frmt2.write(f"  . = 'NaN'\n")
    frmt2.write(";\n")

    # adding second format to first file
    frmt4_dict = {
        "key3": "value3",
        "key4": "value4",
        "key5": "value5",
        "key6": "value6",
        "key7": "value7",
        "key8": "value8",
    }
    frmt2.write("\n")
    frmt2.write("*-- formatnavn --*; \n")
    frmt2.write("value frmt4\n")
    for i in range(3, 9):
        frmt2.write(f"  'key{i}' = 'value{i}'\n")
    frmt2.write(";\n")
    frmt2.write("run;\n")
    frmt2.close()
    return [filename1, filename2], [frmt1_dict, frmt2_dict, frmt3_dict, frmt4_dict]
