#!/usr/bin/env python

# Author: Remi Marchand
# Date: June 9, 2016
# 1st Major Revision: July 20-25, 2016
# 2nd Major Revision: July 29, 2016
# Description: Parses metadata of various kinds into a new csv

import os
import sys
import csv
import importlib


# Set default s processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Get the relative path of the script
path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/Resources/"

# Global Variables
# *Important: set modules to the ones you want to include in your desired order
# scripts of these titles must be in the same folder as this one for the
# function to run properly
modules = ["ID", "collection_date", "geographic_location",
           "serovar", "isolation_source", "organization_name"]

file_ext = "_standardized.csv"

replacements = path + "Null_Replacements.txt"

# Class that contains functions to work with modules, align headers,
# and prepare csv data for parsing.


class Standard_Info():
    def __init__(self, modules):
        self.cols = []
        self.mods = []
        for mod in modules:
            for c in importlib.import_module(mod).column_strs:
                self.cols.append(c)
                self.mods.append(mod)
        if len(self.cols) != len(self.mods):
            raise Exception("Something bad happened")

    # Runs the module's functions in the order that they need to be run
    def run(self, headers):
        self.pos = [None] * (len(self.cols))
        self.find_positions(headers)
        return self.pos

    # Takes in a list of headers and finds the positions of interest
    # Requiremenets: __init__ must have been run initially
    #                self.headers must have been declared
    def find_positions(self, headers):
        for c in range(0, len(self.cols)):
            for h in headers:
                if self.cols[c] in h:
                    self.pos[c] = headers.index(h)

    # new_headers: produces a list of headers to print as the first line
    # of the output csv file.
    def new_headers(self):
        new_headers = []
        for c in range(0, len(self.cols)):
            for k in importlib.import_module(self.mods[c]).keys:
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
        # These modules don't have any additional data
        if mod == "collection_date" or mod == "ID":
            continue
        open_mod = importlib.import_module(mod)
        ret_vals[mod] = open_mod.return_dicts()
    return ret_vals

# return_vals: Int, (listof Str), (listof Str), (listof Str), (listof Str),
#              (listof (listof Str)), (listof Str) -> (listof Str)
# This is a specialized function used to call and return parsed data


def return_vals(s, mod, info, null_vals):
    module = importlib.import_module(mod)
    extra_info = info[mod] if mod in info else None
    if extra_info is not None:
        return module.parse(s, extra_info)
    else:
        return module.parse(s)


def main(file_list, modules=modules):
    null_vals = open_replacements()
    info = open_info_files(modules)
    for in_file in file_list:
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
        mods = std_info.mods
        # Process each line of the file's data
        data_set = []
        # lookup is an empty dictionary that contains
        # items which have been previously parsed
        lookup = {}
        for line in reader:
            line_data = []
            for p in range(0, len(positions)):
                s = line[positions[p]] if positions[p] is not None else ""
                # Replace the null_vals with an empty string
                s = "" if s.lower() in null_vals else s
                if s in lookup.keys():
                    line_data.extend(lookup[s])
                else:
                    vals = return_vals(s, mods[p], info, null_vals)
                    line_data.extend(vals)
                    if s != "":
                        lookup[s] = vals
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
        main(file_list, modules)
    else:
        main(file_list)
