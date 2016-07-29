#!/usr/bin/env python

# Author: Remi Marchand
# Date: May 18, 2016
# Major Revision: July 29, 2016
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
        for data in metadata.values():
            print data
        #    writer.writerow(data)
    return filename


# strip_str: Str -> Str
# removes the leading id of a string (separated by "/")
# and returns the rest of the string

def strip_str(string):
    return "/".join(string.split("/")[1:])


# unique_headers: (listof Dict) -> (listof Str)
# iterates through a collection of dictionaries and constructs
# a list of unique headers found within the dictionaries


def unique_headers(data):
    headers = []
    for line in data:
        for i in line["metadata"].keys():
            new_str = strip_str(i)
            if new_str not in headers:
                headers.append(new_str)
    return headers

# process_data: (listof Dict) (listof Str) Str (listof Str) -> (listof Str)
# pulls relevant information from the subset
# of data["metadata"] specified by specific_key


def process_data(data, line_data, specific_key, headers):
    for key, value in data["metadata"].iteritems():
        if specific_key in key:
            new_str = strip_str(key)
            if new_str in headers:
                line_data[headers.index(new_str)] = value
                continue
    return line_data


# correlated_sample: Str (listof Str) -> (union Str None)
# makes the connection between a run and its associated ID


def correlated_sample(run_name, data):
    query = run_name + "/" + "SAMPLE/PRIMARY_ID"
    if query in data["metadata"].keys():
        return data["metadata"][query]
    else:
        return None


# generate_metadata_csv: (listof Dict), Str
# takes in a list of metadata information in the format of a
# list of dictionaries. Decides what headers to use and formats
# the data into the csv file specified by filename.


def generate_metadata_csv(data, filename):
    with open(filename + ".csv", "wb") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        headers = unique_headers(data)
        headers.sort()
        writer.writerow(headers)
        for line in data:
            line_data = [""] * len(headers)
            for run in line["run_keys"]:
                sample = correlated_sample(run, line)
                if sample is None:
                    print "No sample correlated with run, skipping %s" % run
                    continue
                # Retrieve Run Data
                line_data = process_data(line, line_data, run, headers)
                # Get the correlated sample name for the given run
                sample = correlated_sample(run, line)
                # Retrieve Sample Data
                line_data = process_data(line, line_data, sample, headers)
                # Retrieve Study Data
                line_data = process_data(line, line_data,
                                         line["study_key"], headers)
                # Retrieve Experiment Data
                line_data = process_data(line, line_data,
                                         line["expt_key"], headers)
                # Retrieve Submission Data
                line_data = process_data(line, line_data,
                                         line["sub_key"], headers)
                writer.writerow(line_data)
