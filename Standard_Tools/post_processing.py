#!/usr/bin/env python

# Author: Remi Marchand
# Date: August 9, 2016
# Description: Processes files that have been standardized by
# the standardization script.

from Standard_Tools.common_funs import *

import csv
import dateparser
import datetime
# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

path = os.path.dirname(__file__) + "/"

paths = {"date_replace": path + "Standard_Dates.txt"}

def return_dicts():
    ret_vals = {}
    for key in paths.keys():
        if key == "date_replace":
            # Using the simple_replace function even though this isn't
            # a replacement dictionary -> Does the job for us though.
            ret_vals[key] = simple_replace(paths[key])
        else:
            ret_vals[key] = paths[key]
    return ret_vals

# location: (listof Str) (listof Str) -> (listof Str)
# This function provides a suggested location based on the geographic
# location of the organization if no location is provided.


def location(headers, data):
    new_loc = ""
    location_pos = []
    extra_pos = {}
    for h in range(0, len(headers)):
        if headers[h] == "Organization_Name_COUNTRY":
            extra_pos["ONC"] = h
        elif "LOCATION" in headers[h]:
            location_pos.append(h)

    if extra_pos != {}:
        for line in data:
            # Check that no date data currently exists
            if ''.join([line[i] for i in location_pos]) == '':
                for p in location_pos:
                    if line[p] == '':
                        new_loc = line[extra_pos["ONC"]]
                        break
            line.append(new_loc)


# amb_dates: (listof Str) (listof Str) -> (listof Str)
# This function provides a suggested date for all dates that
# are flagged as ambiguous based on their geographic location.


def amb_dates(headers, data):
    standard_dates = return_dicts()["date_replace"]
    format = "DMY"
    location_pos = []
    pos = {}
    for h in range(0, len(headers)):
        # Grab all headers with location data
        if "LOCATION" in headers[h]:
            location_pos.append(h)
        # Organization name also has location data
        elif headers[h] == "Organization_Name_COUNTRY":
            location_pos.append(h)
        elif headers[h] == "collection_date_AMBIGUOUS":
            pos["AMB"] = h
        elif headers[h] == "collection_date_ORIGINAL":
            pos["ORI"] = h

    for line in data:
        # Check if the date is ambiguous
        if line[pos["AMB"]] == "True":
            date = line[pos["ORI"]]
            for location in location_pos:
                # Grab just the country part of location
                if line[location].split(":")[0] in standard_dates.keys():
                    format = standard_dates[line[location]]
                    break
            new_date = dateparser.parse(date, settings={'DATE_ORDER': format})
            line.append(new_date.strftime("%Y-%b-%d"))


def process_file(in_file):
    csvin = open(in_file, "rU")
    reader = csv.reader(csvin, delimiter=",")
    headers = reader.next()
    data = [i for i in reader]
    # Process Putative Location
    location(headers, data)
    headers.append("putative_LOCATION")
    # Process Ambiguous Dates
    amb_dates(headers, data)
    headers.append("putative_DATE")
    csvin.close()
    with open(in_file, 'w') as csvout:
        csvwriter = csv.writer(csvout, delimiter=',')
        csvwriter.writerow(headers)
        for d in data:
            csvwriter.writerow(d)


if __name__ == "__main__":
    for i in sys.argv[1:]:
        process_file(i)
