#!/usr/bin/evn python

# Author: Remi Marchand
# Date: June 9, 2016
# Descrition: Parses metadata of various kinds into a new csv

import csv
import utils
import operator
import importlib


# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# write_body: Str, csv_reader, (listof(listof Int)), (listof Str) -> None
# This function writes information given to it in the form of a csv reader to
# to a new csv file (specified by filename) with the given headers and
# relevant columns (specified by pos).


def return_body(line, pos, keys, mod, geo_info):
    module = importlib.import_module(mod)
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


def return_headers(pos, headers, keys):
    # Write all of the information found to the new csv file
    default_headers = []
    for my_tuple in pos:
        default_headers.append(headers[my_tuple[0]])
        for item in my_tuple[1:]:
            for key in keys:
                default_headers.append(headers[item] + "_" + key)
    return default_headers

# Global Variables
# *Important: set modules to the ones you want to include in your desired order
# scripts of these titles must be in the same folder as this one for the
# function to run properly
modules = ["collection_date", "geographic_location"]

if __name__ == "__main__":
    open_geo_files = importlib.import_module("open_geo_files")
    geo_info = open_geo_files.return_dicts()
    # Open the csv files of interest
    for in_file in sys.argv[1:]:
        csvin = open(in_file, "rb")
        # Set up the output csv for writing
        csvout = open(in_file[:-4] + "_standardized2.csv", "wb")
        csvwriter = csv.writer(csvout, delimiter=",")
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
            new_headers.extend(return_headers(pos, headers, keys))
            for line in data:
                if mod == "geographic_location":
                    lines.append(return_body(line, pos, keys, mod, geo_info))
                else:
                    lines.append(return_body(line, pos, keys, mod, None))
            data_set.append(lines)
        # For each RUN number, find all data and append it
        csvwriter.writerow(new_headers)
        x = 0
        while(x < len(data_set[0])):
            line = []
            for set in data_set:
                print set
                line.extend(set[x])
            csvwriter.writerow(line)
            x += 1

        csvin.close()
        csvout.close()
