#!/usr/bin/env python

# Author: Remi Marchand
# Date: June 9, 2016
# Description: Parses metadata of various kinds into a new csv

import os
import sys
import csv
import importlib


# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Get the relative path of the script
path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/Resources/"

# Global Variables
# *Important: set modules to the ones you want to include in your desired order
# scripts of these titles must be in the same folder as this one for the
# function to run properly
modules = ["RUN", "collection_date", "geographic_location",
           "serovar", "isolation_source", "organization_name"]

file_ext = "_standardized.csv"

replacements = path + "Null_Replacements.txt"


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
    def run(self, headers):
        self.headers = [[] for _ in xrange(len(self.cols))]
        self.find_positions(headers)
        self.deep_selection_sort()
        self.fill_list()
    def find_positions(self, headers):
        for c in range(0, len(self.cols)):
            for h in headers:
                if self.cols[c] in h:
                    self.headers[c].append({h: self.parse_number(h)})
    def parse_number(self, number):
        num = [int(s) for s in number.split("_") if s.isdigit()]
        if len(num) > 1:
            raise Exception("Multiple Header Numbers Were Found")
        elif len(num) == 0:
            return num
        else:
            return num[0]
    def fill_list(self):
        # Extend the columns which are not the full length
        longest = max([len(i) for i in self.headers])
        for h in self.headers:
                for i in range(len(h), longest):
                    h.append("")
    def deep_selection_sort(self):
        f_list = self.headers[0]
        for p1 in range(0, len(f_list)):
            for sublist in self.headers[1:]:
                for p2 in range(0, len(sublist)):
                    if f_list[p1].values() == sublist[p2].values():
                        temp = sublist[p2]
                        sublist[p2] = sublist[p1]
                        sublist[p1] = temp
    def new_headers(self):
        new_headers = []
        for c in range(0, len(self.cols)):
            new_headers.append(self.cols[c])
            print self.mods[c]
            for k in importlib.import_module(self.mods[c]).keys:
                new_headers.append(self.cols[c] + "_" + k)
        return return_headers
    def data_columns(self):
        ret_vals = []
        for i in range(0, len(self.headers[0])):
            line_set = []
            for l in self.headers:
                if l[i] == "":
                    line_set.append("")
                else:
                    line_set.append(l[i].keys()[0])
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
        if mod == "collection_date" or mod == "RUN":
            continue
        open_mod = importlib.import_module(mod)
        ret_vals[mod] = open_mod.return_dicts()
    return ret_vals


# return_headers: (listof Str) (listof Str) -> (listof Str)
# This function returns relevant headers from the variable headers, specified
# by the variable columns.


def return_headers(cols, mods):
    new_headers = []
    for c in range(0, len(columns)):
        col_headers.append(c)
        for k in importlib.import_module():
            col_headers.append(c + "_" + k)
        new_headers.append(col_headers)
    return new_headers


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
        std_info.run(headers)
        cols = std_info.cols
        mods = std_info.mods
        new_headers = std_info.new_headers()
        data = std_info.data_columns()
        # Process each line of the file's data
        data_set = []
        for line in reader:
            print "I am on line: %s" % line
            for run in data:
                line_data = []
                for element in range(0, len(run)):
                    mod_name = mods[element]
                    position = headers.index(run[element])
                    module = importlib.import_module(mod_name)
                    extra_info = info[mod_name] if mod_name in info else None
                    string = line[position]
                    if extra_info is not None:
                        line_data.append(module.parse(string, extra_info))
                    else:
                        line_data.append(module.parse(string))
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
