#!/usr/bin/evn python

# Author: Remi Marchand
# Date: June 9, 2016
# Descrition: Parses metadata of various kinds into a new csv

import sys
import csv
import utils
import importlib


# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# Global Variables
# *Important: set modules to the ones you want to include in your desired order
# scripts of these titles must be in the same folder as this one for the
# function to run properly
temp = ["collection_date", "geographic_location"]
modules = ["serovar"]
file_ext = "_serovar.csv"


# return_body: (listof Str) (listof Str) (listof Str) Str Str -> (listof Str)
# This function takes a line of data and returns parsed data, the location
# (or column) of which is specified by pos, and the parser specified by mod.


def return_body(line, pos, keys, mod, extra_info):
    module = importlib.import_module(mod)
    line_data = []
    for p in pos:
        line_data.append(line[p[0]])
        for c in p[1:]:
            if extra_info is None:
                item_info = module.parse(line[c])
            else:
                item_info = module.parse(line[c], extra_info)
            for key in keys:
                line_data.append(item_info[key])
    return line_data

# return_headers: (listof Str) (listof Str) (listof Str) -> (listof Str)
# This function returns relevant headers from the variable headers, specified
# by pos. The extra information to include at each position is specified by
# keys.


def return_headers(pos, headers, keys):
    default_headers = []
    for my_tuple in pos:
        default_headers.append(headers[my_tuple[0]])
        for item in my_tuple[1:]:
            for key in keys:
                default_headers.append(headers[item] + "_" + key)
    return default_headers

# main: (listof Str) -> None
# This function processes relevant metadata from all input files according
# to modules specified by the variable modules. It runs each module on every
# input file, concatenating the results into a single output file.


if __name__ == "__main__":
    open_serovar_files = importlib.import_module("open_serovar_lookup")
    sero_info = open_serovar_files.return_dicts()
    open_geo_files = importlib.import_module("open_geo_files")
    geo_info = open_geo_files.return_dicts()
    # Open the csv files of interest
    for in_file in sys.argv[1:]:
        csvin = open(in_file, "rb")
        # Set up the output csv for writing
        filename = in_file[:-4] + file_ext
        reader = csv.reader(csvin, delimiter=",")
        headers = reader.next()
        data = [i for i in reader]
        # Import the column_strs from each of the modules
        new_headers, data_set = [], []
        for mod in modules:
            lines = []
            columns = importlib.import_module(mod).column_strs
            keys = importlib.import_module(mod).keys
            pos = utils.find_positions("RUN", columns, headers)
            if pos == []:
                break
            new_headers.extend(return_headers(pos, headers, keys))
            for line in data:
                if mod == "geographic_location":
                    lines.append(return_body(line, pos, keys, mod, geo_info))
                elif mod == "serovar":
                    print mod
                    lines.append(return_body(line, pos, keys, mod, sero_info))
                else:
                    lines.append(return_body(line, pos, keys, mod, None))
            data_set.append(lines)
        # For each RUN number, find all data and append it
        if data_set != []:
            print "Working on %s" % filename
            csvout = open(filename, "wb")
            csvwriter = csv.writer(csvout, delimiter=",")
            csvwriter.writerow(new_headers)
            for x in range(0, len(data_set[0])):
                line = []
                for mod in data_set:
                    line.extend(mod[x])
                csvwriter.writerow(line)
            csvout.close()
        csvin.close()
