import pandas as pd
import numpy as np
from collections import defaultdict

class UtdFormat(defaultdict):
    def __init__(self,*args):
        if args:
            super(defaultdict, self).__init__(*args)
        else:
            super(defaultdict, self).__init__(int)
        self.set_na_value()
        self.store_ranges()
        self.set_other_as_lowercase()
    
    def __missing__(self, key):
        
        if self.check_if_na(key):
            if self.set_na_value():
                return self.na_value
            
        int_str_confuse = self.int_str_confuse(key)
        if int_str_confuse:
            return int_str_confuse
        
        key_in_range = self.look_in_ranges(key)
        if key_in_range:
            return key_in_range
        
        if self.get("other", ""):
            return self.get("other", "")
        
        raise ValueError(f"{key} not in format, and no other-key is specified.")
        
    
    def store_ranges(self):
        self.ranges = {}
        for key, value in self.items():
            
            is_range = False
            if isinstance(value, str):
                if "-" in key and key.count("-") == 1:
                    bottom, top = key.split("-")[0].strip(), key.split("-")[1].strip()
                    if (bottom.isdigit() or bottom.lower() == "low") and (top.isdigit() or top.lower() == "high"):
                        if bottom.lower() == "low":
                            bottom = float("-inf")
                        else:
                            bottom = float(bottom)
                        if top.lower() == "high":
                            top = float("inf")
                        else:
                            top = float(top)
                        self.ranges[value] = (bottom, top)
    

    
    def look_in_ranges(self, key):
        #print(f"looking in ranges for {key}")
        try:
            key = float(key)
        except:
            return None
        for range_key, (bottom, top) in self.ranges.items():
            #print(f"Looking in ranges at {range_key}, {bottom=} {top=}")
            if key >= bottom and key <= top:
                return range_key      
        return None
    
    
    def int_str_confuse(self, key):
        if isinstance(key, str):
            try:
                key = int(key)
                if key in self:
                    return self[key]
            except:
                return None
        elif isinstance(key, int):
            key = str(key)
            if key in self:
                return self[key]
        return None
        
    def set_other_as_lowercase(self):
        # In case "other" has mixed large and small letters
        found = False
        for key, value in self.items():
            if key.lower() == "other":
                found = True
                break
        if found:
            del self[key]
            self["other"] = value
    
    
    
    def set_na_value(self):
        for key, value in self.items():
            if self.check_if_na(key):
                self.na_value = value
                return True
        else:
            self.na_value = None
            return False
    
    @staticmethod
    def check_if_na(key) -> bool:
        if pd.isna(key):
            return True
        if isinstance(key, str):
            if key in [".", "none", "", "NA", "<NA>", "<NaN>"]:
                return True
        return False