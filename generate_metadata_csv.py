#!/usr/bin/env python

# Author: Remi Marchand
# Date: May 18, 2016
# Description: This script generates a csv file from dictionaries
# provided to it.

import csv

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# write_data: (list of Str) (listof Dict) Str -> Str
# writes metadata data to a csvfile using information stored
# in the header and metadata files. Returns the csv filename.


def write_data(headers, metadata, filename):
    with open(filename + ".csv", "wb") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=",")
        writer.writeheader()
        for data in metadata:
            writer.writerow(data)
    return filename

# make_headers: (listof Dict) -> (list of Str)
# takes in a list of metadata in dictionary format, extracts
# all of the keys (representing headers) and constructs a
# list of the keys.

def make_headers(metadata):
    headers = []
    for i in metadata:
        for j in i.keys():
            if j not in headers:
                headers.append(j)
    headers.sort()
    return headers

# generate_metadata_csv: (listof Dict), Str
# takes in a list of metadata information in the format of a
# list of dictionaries. Decides what headers to use and formats
# the data into the csv file specified by filename.

def generate_metadata_csv(metadata, filename):
    headers = make_headers(metadata)
    write_data(headers, metadata, filename)
