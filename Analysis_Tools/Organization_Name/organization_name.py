#!/usr/bin/env python

# Author: Remi Marchand
# Date: July 20, 2016
# Description: A wrapper to parse isolation_source information

from Analysis_Tools.common_funs import *

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

path = os.path.dirname(__file__) + "/"
parent = os.path.abspath(os.path.dirname(sys.argv[0])) + "/"

# Global variables
keys = ["CURATED", "ORIGINAL", "SUGGESTION", "COUNTRY", "PROVINCE"]
# column_strs is a list of strings representing columns of interest
column_strs = ["Organization_Name"]

# Paths to the relevant files
paths = {"complex_replace": path + "Organization_Replacement_Lookup.csv",
         "equivalent_words": parent + "Equivalent_Words.txt",
         "std_file": path + "Standard_Organization_Names.txt",
         "ind_file": path + "Standard_Organization_Names_Index.txt"}


# return_dicts: None -> Dict
# This function is specifically designed to open and parse the files in paths


def return_dicts():
    ret_vals = {}
    for key in paths.keys():
        if key == "complex_replace":
            ret_vals[key] = complex_replace(paths[key])
        elif key == "equivalent_words":
            ret_vals[key] = simple_replace(paths[key])
        else:
            ret_vals[key] = paths[key]
    return ret_vals

# *************************************************************************** #


def parse(orgn_name, info):
    return_vals = [""] * len(keys)
    return_vals[keys.index("ORIGINAL")] = orgn_name
    if orgn_name == "":
        return return_vals
    orgn_name = orgn_name.lower().strip()
    for key in info["complex_replace"].keys():
        if orgn_name == key.lower().strip():
            new_info = info["complex_replace"][key]
            return_vals[keys.index("CURATED")] = new_info[0]
            return_vals[keys.index("COUNTRY")] = new_info[1]
            return_vals[keys.index("PROVINCE")] = new_info[2]
            return return_vals
    return_vals[keys.index("SUGGESTION")] = spellcheck(orgn_name,
                                                       info, 34)
    return return_vals
