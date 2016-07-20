#!/usr/bin/env python

# Author: Remi Marchand
# Date: July 11, 2016
# Description: A function to open serovar lookup files for parsing

import os

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Get the relative path of the script
path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/Resources/"

# Paths to the relevant files
paths = {"isr": path + "Isolation_Source_Replacements.txt",
         "eqw": path + "Equivalent_Words.txt",
         "lif": path + "Standard_Files/Standard_Isolation_Sources.txt",
         "inf": path + "Index_Files/Standard_Isolation_Sources_Index.txt"}


# parse_isolation_source: None -> Dict
# This function is specifically designed to open and parse the files:
# "Serovar_Replacement_Lookup.txt" and "Equivalent_Words.txt"

def parse_isolation_source(filepath):
    data = {}
    with open(filepath, "rU") as open_file:
        for line in open_file:
            line = line.replace("\n", "")
            line = line.replace("\"", "").split("\t")
            data[line[1]] = line[0]
    return data


# return_dicts: None -> Dict
# This function is specifically designed to open and parse the file:
# "Serovar_Replacement_Lookup.txt"


def return_dicts():
    ret_vals = {}
    for key in paths.keys():
        if key == "isr" or key == "eqw":
            ret_vals[key] = parse_isolation_source(paths[key])
        else:
            ret_vals[key] = paths[key]
    return ret_vals
