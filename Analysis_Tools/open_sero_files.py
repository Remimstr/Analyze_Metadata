#!/usr/bin/env python

# Author: Remi Marchand
# Date: June 10, 2016
# Description: A function to open serovar lookup files for parsing

import os
import csv

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Get the relative path of the script
path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/Resources/"

# Paths to the relevant files
paths = {"srl": path + "Serovar_Replacement_Lookup.csv",
         "lif": path + "/Standard_Files/Standard_Serovars.txt",
         "inf": path + "/Index_Files/Standard_Serovars_Index.txt"}


# return_dicts: None -> Dict
# This function is specifically designed to open and parse the file:
# "Serovar_Replacement_Lookup.txt"

def return_dicts():
    ret_vals = {}
    for key in paths.keys():
        if key == "srl":
            data = {}
            with open(paths[key], "rU") as csv_file:
                csv_reader = csv.reader(csv_file)
                for i in csv_reader:
                    data[i[0]] = [j for j in i[1:]]
            ret_vals[key] = data
        else:
            ret_vals[key] = paths[key]
    return ret_vals
