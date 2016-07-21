#!/usr/bin/env python

# Author: Remi Marchand
# Date: June 10, 2016
# Description: Parses a given serovar into a unified format

import os
import csv
from common_funs import *

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/Resources/"

# Global variables
keys = ["CURATED", "VARIANT", "OTHER_INFO", "ORIGINAL", "SUGGESTION"]
# column_strs is a list of strings representing columns of interest
column_strs = ["serovar"]

# Paths to the relevant files
paths = {"complex_replace": path + "Serovar_Replacement_Lookup.csv",
         "std_file": path + "Standard_Files/Standard_Serovars.txt",
         "ind_file": path + "Index_Files/Standard_Serovars_Index.txt"}


# return_dicts: None -> Dict
# This function is specifically designed to open and parse the files in paths


def return_dicts():
    ret_vals = {}
    for key in paths.keys():
        if key == "complex_replace":
            ret_vals[key] = complex_replace(paths[key])
        else:
            ret_vals[key] = paths[key]
    return ret_vals

# *************************************************************************** #


def parse(raw_serovar, info):
    return_vals = [""] * len(keys)
    return_vals[keys.index("ORIGINAL")] = raw_serovar
    if raw_serovar == "":
        return return_vals
    raw_serovar = raw_serovar.lower().strip()
    for key in info["complex_replace"].keys():
        if raw_serovar == key.lower().strip():
            new_info = info["complex_replace"][key]
            return_vals[keys.index("CURATED")] = new_info[0]
            return_vals[keys.index("VARIANT")] = new_info[1]
            return_vals[keys.index("OTHER_INFO")] = new_info[2]
            return return_vals
    return_vals[keys.index("SUGGESTION")] = spellcheck(raw_serovar,
                                                       info, 34)
    return return_vals
