#!/usr/bin/env python

# Author: Remi Marchand
# Date: August 11, 2016
# Description: Parses host sources into a unified format

from Standard_Tools.common_funs import *

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

path = os.path.dirname(__file__) + "/"
parent = os.path.abspath(os.path.dirname(sys.argv[0])) + "/"

# Global variables
keys = ["CURATED", "ORIGINAL", "SUGGESTION"]
# column_strs is a list of strings representing columns of interest
column_strs = ["host", "specific_host", "host_scientific_name"]

# Paths to relevant files
paths = {"simple_replace" : path + "Host_Replacements.txt",
         "equivalent_words" : parent + "Equivalent_Words.txt",
         "std_file" : path + "Standard_Hosts.txt",
         "ind_file" : path + "Standard_Hosts_Index.txt"}


# return_dicts: None -> Dict
# This function is specifically designed to open and parse the files in paths


def return_dicts():
    ret_vals = {}
    for key in paths.keys():
        if key == "simple_replace" or key == "equivalent_words":
            ret_vals[key] = simple_replace(paths[key])
        else:
            ret_vals[key] = paths[key]
    return ret_vals

# *************************************************************************** #


def parse(host, info):
    replacements, eq_words = info["simple_replace"], info["equivalent_words"]
    return_vals = [""] * len(keys)
    return_vals[keys.index("ORIGINAL")] = host
    host = replace_words(repl_dict(eq_words), host)
    if host == "":
        return return_vals
    host = host.lower().strip()
    for key in replacements.keys():
        if host == key.lower().strip():
            return_vals[keys.index("CURATED")] = replacements[key]
            return return_vals
    return_vals[keys.index("SUGGESTION")] = spellcheck(host, info, 24)
    return return_vals
