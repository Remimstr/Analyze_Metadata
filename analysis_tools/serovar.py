#!/usr/bin/evn python

# Author: Remi Marchand
# Date: June 10, 2016
# Descrition: Parses serovar information from .csv's into a unified format

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Global variables
keys = ["CURATED", "ORIGINAL", "VARIANT", "OTHER_INFO"]
# column_strs is a list of strings representing columns of interest
column_strs = ["serovar"]


def parse(raw_serovar, sero_info):
    return_vals = {keys[0]: "", keys[1]: "", keys[2]: "", keys[3]: ""}
    for key in sero_info.keys():
        if raw_serovar == key:
            new_sero_info = sero_info[key]
            return_vals[keys[0]] = new_sero_info[0]
            return_vals[keys[1]] = raw_serovar
            return_vals[keys[2]] = new_sero_info[1]
            return_vals[keys[3]] = new_sero_info[2]
            return return_vals
        
