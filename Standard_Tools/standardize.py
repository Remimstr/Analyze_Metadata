#!/usr/bin/env python

# Author: Remi Marchand
# Date: June 9, 2016
# 1st Major Revision: July 20-25, 2016
# 2nd Major Revision: July 29, 2016
# Description: Parses metadata of various kinds into a new csv

import os
import csv
import importlib

# Set default processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import Standard_Tools.post_processing
from Standard_Tools import *

# Get the relative path of the script
path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/Resources/"

# Global Variables
# *Important: set modules to the ones you want to include in your desired order
# scripts of these titles must be in the same folder as this one for the
# function to run properly


modules = [["Generic", "generic"], ["Collection_Date", "collection_date"],
           ["Geographic_Location", "geographic_location"],
           ["Serovar", "serovar"], ["Isolation_Source", "isolation_source"],
           ["Organization_Name", "organization_name"], ["Host", "host"]]


# These modules don't have any additional data
simple_parse = ["Collection_Date", "Generic"]

file_ext = "_standardized.csv"

replacements = path + "Null_Replacements.txt"

# Class that contains functions to work with modules, align headers,
# and prepare csv data for parsing.


class Standard_Info:
    def __init__(self, modules):
        self.cols = []
        self.modules = []
        self.mods = []
        for mod in modules:
            for c in importlib.import_module(".".join(mod)).column_strs:
                self.cols.append(c)
                self.modules.append(mod)
                self.mods.append(mod[1])
        if len(self.cols) != len(self.mods):
            raise Exception("Something bad happened")

    # Runs the module's functions in the order that they need to be run
    def run(self, headers):
        self.pos = [None] * (len(self.cols))
        self.find_positions(headers)
        return self.pos

    # Takes in a list of headers and finds the positions of interest
    # Requirements: __init__ must have been run initially
    #                self.headers must have been declared
    def find_positions(self, headers):
        for c in range(0, len(self.cols)):
            for h in headers:
                if self.cols[c] == h:
                    self.pos[c] = headers.index(h)

    # new_headers: produces a list of headers to print as the first line
    # of the output csv file.
    def new_headers(self):
        new_headers = []
        for c in range(0, len(self.cols)):
            for k in importlib.import_module(".".join(self.modules[c])).keys:
                if k != "":
                    new_headers.append(self.cols[c] + "_" + k)
                else:
                    new_headers.append(self.cols[c])
        return new_headers

    # data_columns: prints the columns that the caller should use to
    # pull out relevant data from the csv file.
    # Requirements: self.headers must have been declared
    # * Should only be called after the run method has been called
    def data_columns(self):
        ret_vals = []
        for i in range(0, len(self.headers)):
            line_set = []
            if i is None:
                line_set.append("")
            else:
                line_set.append(i.keys()[0])
            ret_vals.append(line_set)
        return ret_vals


# open_replacements: Str -> (listof Str)
# This function opens the replacements file and returns all values
# found in a list.


def open_replacements():
    ret_vals = []
    with open(replacements, "rU") as in_file:
        for line in in_file:
            ret_vals.append(line.strip("\n"))
    return ret_vals


# open_info_files: None -> Dict
# This function opens files that the various parsing modules
# will need in order to parse correctly.


def open_info_files(modules):
    ret_vals = {}
    for mod in modules:
        if mod[0] in simple_parse:
            continue
        open_mod = importlib.import_module(".".join(mod))
        ret_vals[mod[1]] = open_mod.return_dicts()
    return ret_vals

# return_vals: Int, (listof Str), (listof Str), (listof Str), (listof Str),
#              (listof (listof Str)), (listof Str) -> (listof Str)
# This is a specialized function used to call and return parsed data


def return_vals(s, mod, info):
    module = importlib.import_module(".".join(mod))
    extra_info = info[mod[1]] if mod[1] in info else None
    if extra_info is not None:
        return module.parse(s, extra_info)
    else:
        return module.parse(s)


def standardize(files, modules=modules):
    null_vals = open_replacements()
    info = open_info_files(modules)
    # lookup is an empty dictionary that contains
    # items which have been previously parsed
    lookup = {}
    for in_file in files:
        csvin = open(in_file, "rU")
        # Set up the output csv for writing
        filename = in_file[:-4] + file_ext
        print "Working on %s" % filename
        reader = csv.reader(csvin, delimiter=",")
        headers = reader.next()
        # Create a new object for working with csv data
        std_info = Standard_Info(modules)
        positions = std_info.run(headers)
        new_headers = std_info.new_headers()
        mods = std_info.modules
        # Process each line of the file's data
        data_set = []
        for line in reader:
            line_data = []
            for p in range(0, len(positions)):
                s = line[positions[p]] if positions[p] is not None else ""
                # Replace the null_vals with an empty string
                s = "" if s.lower() in null_vals else s
                lookup_key = mods[p][1] + "." + s
                if lookup_key in lookup.keys():
                    line_data.extend(lookup[lookup_key])
                    # print "%s:%s" % (mods[p], lookup[s])
                else:
                    vals = return_vals(s, mods[p], info)
                    # print "%s:%s" % (mods[p], vals)
                    line_data.extend(vals)
                    if s != "":
                        lookup[lookup_key] = vals
            if not all(i == "" for i in line_data):
                data_set.append(line_data)
        # Write all of the newfound data to the csv
        if data_set != []:
            csvout = open(filename, "wb")
            csvwriter = csv.writer(csvout, delimiter=",")
            csvwriter.writerow(new_headers)
            for line in data_set:
                csvwriter.writerow(line)
            csvout.close()
            csvin.close()

            # Run the post-processing script
            Standard_Tools.post_processing.process_file(filename)


if __name__ == "__main__":
    file_list = []
    modules = []
    # Open the csv files of interest
    for i in sys.argv[1:]:
        if i[-4:] == ".csv":
            file_list.append(i)
        else:
            modules.append(i)
    if modules != []:
        standardize(file_list, modules)
    else:
        standardize(file_list)
