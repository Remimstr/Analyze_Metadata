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

# find_positions: Str Str Str -> None or
# (listof ReaderObject, (listof Int), (listof Str))
# This function searches the headers of an input csv for the strings
# provided, acc_str, and item_str. It returns the csv_reader object,
# the positions found, and the headers of the csv file. The caller is
# responsible for closing in_file (use .close())


def find_positions(acc_str, item_str, in_file):
    # For each entry in the csv file, retrieve the accession number position(s)
    # and the item of interest position(s)
    csvin = open(in_file, "rb")
    reader = csv.reader(csvin, delimiter=",")
    headers = reader.next()
    acc_col, item_col = [], []
    # Find the indices for all of the relevant columns
    for h in range(0, len(headers)):
        if acc_str in headers[h]:
            acc_col.append(h)
        if item_str in headers[h]:
            item_col.append(h)
    if acc_col == [] or item_col == []:
        csvin.close()
        return None
    # Make a list of corresponding positions by matching
    # id headers and date headers
    pos = []
    for i in acc_col:
        acc_string = headers[i]
        acc_col_digit = [int(s) for s in acc_string.split("_") if
                         s.isdigit()]
        for j in item_col:
            item_string = headers[j]
            item_col_digit = [int(s) for s in item_string.split("_") if
                              s.isdigit()]
            if acc_col_digit == item_col_digit:
                pos.append([i, j])
    # Write the relevant information to a new csv file
    return [reader, pos, headers, csvin]


# write_to_csv: Str, csv_reader, (listof(listof Int)), (listof Str) -> None
# This function writes information given to it in the form of a csv reader to
# to a new csv file (specified by filename) with the given headers and
# relevant columns (specified by pos).


def write_to_csv(reader, pos, headers, item_key, other_keys, mod, filename):
    module = importlib.import_module(mod)
    # Write all of the information found to the new csv file
    with open(filename[:-4] + file_end, "wb") as csvout:
        csvwriter = csv.writer(csvout, delimiter=",")
        default_headers = []
        for pair in pos:
            for p in pair:
                default_headers.append(headers[p])
            for key in other_keys:
                default_headers.append(headers[pair[0]] + "_" + key)
        # Write the headers to the new csv
        csvwriter.writerow(default_headers)
        csv_data = []
        for line in reader:
            line_data = []
            for p in pos:
                item_info = module.parse(line[p[1]])
                line_data.extend([line[p[0]], item_info[item_key]])
                for key in other_keys:
                    line_data.extend([item_info[key]])
            csv_data.append(line_data)
            csvwriter.writerow(line_data)


def find_and_write(acc_str, item_str, item_key, other_keys, in_file, mod):
    result = find_positions(acc_str, item_str, in_file)
    if result is None:
        print("Could not find what you wanted")
    else:
        reader, pos, headers, csvin = result
        write_to_csv(reader, pos, headers, item_key, other_keys,
                     item_str, in_file)
    csvin.close()
