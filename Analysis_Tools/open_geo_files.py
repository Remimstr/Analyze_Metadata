#!/usr/bin/evn python

# Author: Remi Marchand
# Date: June 3, 2016
# Descrition: Module to open geo location files for parsing

import re
import os

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Get the relative path of the script
path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/Resources/"

# Paths to the relevant files
paths = {"cr": path + "Country_Replacements.txt",
         "gl": path + "Geo_Library.txt",
         "sp": path + "State_Province.txt"}

# parse_files: openfile, Str, Str -> Dict
# This function is specifically designed to open and parse the following files:
# "Country_Replacements.txt" and "Geo_Library.txt". It returns all of the
# information found as a dictionary specific to the file being parsed.
# Country_Replacments: {key = country regex: value = std. country name}
# Geo_Library: {key = std. country name: value = listof(std. province name)}


def parse_files(open_file, regex, option):
    data = {}
    for line in open_file:
        # Use a regular expression to split each line
        split_line = re.split(r"%s" % regex, line)
        # Add the data to the dict
        if option == "cr":
            data[split_line[0]] = split_line[1].strip("\n")
        elif option == "sp":
            data[split_line[2]] = [split_line[0], split_line[1]]
        elif option == "gl":
            country = split_line[0]
            province = split_line[1]
            if country in data.keys():
                data[country].append(province)
            else:
                data[country] = [province]
    return data


# parse_sp_data: openfile, Str, Str -> (listof Str)
# This function is specifically designed to open and parse "State_Province.txt"
# It returns all of the information found as a list of state_province info.
# State_Province: {key = std. prov. name: [prov. name, std. country name]}
def parse_sp_data(open_file, regex, option):
    data = []
    for line in open_file:
        # Use a regular expression to split each line
        split_line = re.split(r"%s" % regex, line)
        data.append(split_line[:-1])
    return data


def return_dicts():
    # Set the regular expressions needed for each file
    cr_re, gl_re, sp_re = ":", "[\|(\n)]", "[\|(\t)(\n)]"
    cr, gl, sp = open(paths["cr"]), open(paths["gl"]), open(paths["sp"])
    cr_data = parse_files(cr, cr_re, "cr")
    gl_data = parse_files(gl, gl_re, "gl")
    sp_data = parse_sp_data(sp, sp_re, "sp")
    cr.close(), gl.close(), sp.close()
    return([cr_data, gl_data, sp_data])
