#!/usr/bin/evn python

# Author: Remi Marchand
# Date: June 1, 2016
# Descrition: A collection of funcions for generic csv manipulation

import csv
import importlib

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

file_end = "_standardized.csv"

# find_positions: Str (listof Str) Str -> [] or (listof Int)
# This function searches headers provided, headers, for the strings
# provided, acc_str, and item_strs. It returns the positions found.


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
    # Make a list of corresponding positions by matching
    # id headers and item headers
    pos = []
    for a in acc_col:
        acc_string = headers[a]
        acc_col_digit = [int(s) for s in acc_string.split("_") if
                         s.isdigit()]
        pos.append([a])
        corr_cols = []
        for i in item_col:
            item_string = headers[i]
            item_col_digit = [int(s) for s in item_string.split("_") if
                              s.isdigit()]
            if acc_col_digit == item_col_digit:
                corr_cols.append(i)
        pos[pos.index([a])].extend(corr_cols)
    return pos


# write_to_csv: Str, csv_reader, (listof(listof Int)), (listof Str) -> None
# This function writes information given to it in the form of a csv reader to
# to a new csv file (specified by filename) with the given headers and
# relevant columns (specified by pos).


def write_body(line, pos, headers, keys, mod, geo_info):
    module = importlib.import_module(mod)
    # Write all of the information found to the new csv file
    default_headers = []
    for my_tuple in pos:
        default_headers.append(headers[my_tuple[0]])
        for item in my_tuple[1:]:
            for key in keys:
                default_headers.append(headers[item] + "_" + key)
    line_data = []
    for p in pos:
        line_data.append(line[p[0]])
        for c in p[1:]:
            if geo_info is None:
                item_info = module.parse(line[c])
            else:
                item_info = module.parse(line[c], geo_info)
            for key in keys:
                line_data.append(item_info[key])
    return line_data


def find_and_write(acc_str, item_strs, keys, in_file, mod, file_end):
    filename = in_file[:-4] + "_" + file_end + ".csv"
    result = find_positions(acc_str, item_strs, in_file)
    if result is None:
        print("Could not find what you wanted")
    else:
        print("Writing %s" % filename)
        reader, pos, headers, csvin = result
        if mod == "geographic_location":
            open_geo_files = importlib.import_module("open_geo_files")
            geo_info = open_geo_files.return_dicts()
            write_to_csv(reader, pos, headers, keys, mod, filename, geo_info)
        else:
            write_to_csv(reader, pos, headers, keys, mod, filename, None)
        csvin.close()
