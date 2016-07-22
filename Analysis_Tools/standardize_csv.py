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


# flatten: (listof Any) -> generator Object
# This function takes in a list and produces a generator object which
# can be called on the elements.


def flatten(lst):
    for x in lst:
        if hasattr(x, '__iter__'):
            for y in flatten(x):
                yield y
        else:
            yield x

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
        if mod == "collection_date":
            continue
        open_mod = importlib.import_module(mod)
        ret_vals[mod] = open_mod.return_dicts()
    return ret_vals


# find_positions: Str (listof Str) Str -> (listof Dict, listof Str)
# This function comprehensively searches headers for instances of
# acc_str and item_strs. For each set found (ex. RUN_10, collection_date_10,
# isolation_source_10), it creates a dictionary with each header name
# and its corresponding position. This is the first argument. The second
# argument returned is a list of unique headers found by the function.


def find_positions(acc_str, item_strs, headers):
    acc_col, item_col = [], []
    # Find the indices for all of the relevant columns
    for h in range(0, len(headers)):
        if acc_str in headers[h]:
            acc_col.append(h)
        for i in item_strs:
            if i in headers[h] and h not in item_col:
                item_col.append(h)
    if acc_col == [] or item_col == []:
        return []
    print acc_col, item_col
    # Make a list of corresponding positions by matching
    # id headers and item headers
    pos = []
    unique_keys = [acc_str]
    for a in acc_col:
        acc_string = headers[a]
        acc_col_digit = [int(s) for s in acc_string.split("_") if
                         s.isdigit()]
        cor_cols = [{acc_str: a}]
        for i in item_col:
            item_string = headers[i]
            item_col_digit = [int(s) for s in item_string.split("_") if
                              s.isdigit()]
            item_string = "_".join([s for s in item_string.split("_") if not
                                   (s.isdigit() or s == "SAMPLE")])
            # Compare only the numbers found to determine if the fields
            # are related
            if acc_col_digit == item_col_digit:
                for s in item_strs:
                    if s == item_string:
                        cor_cols.append({s: i})
                        if s not in unique_keys:
                            unique_keys.append(s)
        pos.append(cor_cols)
    return [pos, unique_keys]


# parse_single: (listof Str) Dict (listof Str) (listof Str) -> (listof Str)
# This function returns the data from p parsed out of line using the modules
# pointed to by the information in the variable modules and additional
# information found in info.


def parse_single(line, p, columns, info, null_vals):
    data = []
    for col in columns.keys():
        mod = columns[col]
        column_strs = importlib.import_module(mod).column_strs
        keys = importlib.import_module(mod).keys
        if p.keys()[0] in column_strs:
            line_data = line[p[p.keys()[0]]]
            # If the value is among those in the null list, don't process it
            if line_data.lower() in null_vals:
                data.extend([""] * len(keys))
                continue
            module = importlib.import_module(mod)
            # If the module needs extra info, provide it
            if mod in info.keys():
                data.extend(module.parse(line[p[p.keys()[0]]], info[mod]))
            else:
                data.extend(module.parse(line[p[p.keys()[0]]]))
    return data

# return_headers: (listof Str) (listof Str) -> (listof Str)
# This function returns relevant headers from the variable headers, specified
# by the variable columns.


def return_headers(keys, columns):
    new_headers = []
    for c in columns:
        col_headers = [c]
        for k in keys:
            col_headers.append(c + "_" + k)
        new_headers.append(col_headers)
    return new_headers

# main: (listof Str) -> None
# This function processes relevant metadata from all input files according
# to modules specified by the variable modules. It runs each module on every
# input file, concatenating the results into a single output file.


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
        data = [i for i in reader]

        # Set the relevant information based on modules of interest
        data_set = []
        new_headers = [["RUN", "RUN"]]
        keys = []
        columns = {}
        for mod in modules:
            mod_keys = importlib.import_module(mod).keys
            mod_cols = importlib.import_module(mod).column_strs
            keys.extend(mod_keys)
            for c in mod_cols:
                columns[c] = mod
            new_headers.extend(return_headers(mod_keys, mod_cols))
        cols = [c for c in columns.keys()]
        print cols
        try:
            positions, unique_keys = find_positions("RUN", cols, headers)
        except:
            print "No relevant information found"
            csvin.close()
            continue
        # Filter the list of new_headers against positions to only include
        # those headers which were actually found
        # Make a list of abbreviated headers for easier indexing
        abbr_headers = [i[0] for i in new_headers]

        for line in data:
            for collection in positions:
                line_data = [""] * len(abbr_headers)
                for p in collection:
                    if p.keys()[0] == "RUN":
                        line_data[abbr_headers.index("RUN")] = line[p["RUN"]]
                    else:
                        data = parse_single(line, p, columns, info, null_vals)
                        line_data[abbr_headers.index(p.keys()[0])] = data
                # Flatten line_data using the flatten generator function
                print line_data
                line_data = [x for x in flatten(line_data)]
                print len(line_data)
                if line_data[0] != "" and \
                        not all(i == "" for i in line_data[1:]):
                    data_set.append(line_data)
        # Flatten headers using the flatten generator function
        new_headers = [x for x in flatten([i[1:] for i in new_headers])]
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
