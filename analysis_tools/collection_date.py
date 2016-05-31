#!/usr/bin/env python

# Author: Remi Marchand
# Date: May 24, 2016
# Description: Parses collection dates from .csv's into a unified format

import csv
import math
import calendar
import dateparser
import datetime
from datetime import date
from compiler.ast import flatten


# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

today = date.today()
this_year = today.year


def ambiguous(d):
    times = [d["date_obj"].year, d["date_obj"].month, d["date_obj"].day]
    if len([i for i in times if (i < 12)]) > 1:
        return True
    else:
        return False



def parse_some_dates(raw_date):
    return_vals = {}
    date_parser = dateparser.DateDataParser(languages=["en"])
    date_obj = date_parser.get_date_data(raw_date)
    new_date, error, flag = "", "", ""
    if date_obj["date_obj"] is None:
        flag = raw_date
    elif ambiguous(date_obj):
        flag = raw_date
    else:
        # If the precision is "day" then we're good to process as is
        if date_obj["period"] == "day":
            new_date = date_obj["date_obj"]
            error = 0
        # If the precision is "month", adjust accordingly
        if date_obj["period"] == "month":
            month, year = date_obj["date_obj"].month, date_obj["date_obj"].year
            error = int(math.ceil(calendar.monthrange(year, month)[1] / 2.0))
            new_date = date_obj["date_obj"].replace(day=error)
        # If the precision is "year", adjust accordingly
        if date_obj["period"] == "year":
            leap = True if calendar.isleap(date_obj["date_obj"].year) else False
            year_count = 366 if leap else 365
            error = int(math.ceil(year_count) / 2.0)
            new_date = date_obj["date_obj"].replace(day=1, month=1)
            new_date += datetime.timedelta(days=error - 1)
        new_date = new_date.strftime("%Y-%b-%d")
    return_vals["DATE"] = new_date
    return_vals["FLAG"] = flag
    return_vals["ERROR"] = error
    return(return_vals)

# write_date_csv: Str, csv_reader, (listof(listof Int)), (listof Str) -> None
# This function writes information given to it in the form of a csv reader to
# to a new csv file (specified by filename) with the given headers and
# relevant columns (specified by pos).


def write_date_csv(filename, reader, pos, headers):
    # Write all of the information found to the new csv file
    with open(filename[:-4] + "_collection_date.csv", "wb") as csvout:
        csvwriter = csv.writer(csvout, delimiter=",")
        new_headers = [headers[key] for key in flatten(pos)]
        # Add the ERROR_MARGIN field to the headers
        new_headers = [x for y in (new_headers[i:i + 2] +
                       ['ERROR_MARGIN', 'FLAG'] * (i < len(new_headers) - 1)
                       for i in xrange(0, len(new_headers), 2)) for x in y]
        # Write the headers to the new csv
        csvwriter.writerow(new_headers)
        for line in reader:
            print_list = []
            for p in pos:
                date_info = parse_some_dates(line[p[1]])
                print_list.extend([line[p[0]], date_info["DATE"],
                                  date_info["ERROR"], date_info["FLAG"]])
            csvwriter.writerow(print_list)


# This script takes in a list of metadata csv files, parses the collection
# dates out of each one, and produces a new csv containing those dates
for in_file in sys.argv[1:]:
    # For each entry in the csv file, retrieve the run numbers
    # and the collection dates
    with open(in_file, "rb") as csvin:
        reader = csv.reader(csvin, delimiter=",")
        headers = reader.next()
        id_col, date_col = [], []
        IDs, DATES = [], []
        # Find the indices for all of the relevant columns
        for h in range(0, len(headers)):
            if "RUN" in headers[h]:
                id_col.append(h)
            if "collection_date" in headers[h]:
                date_col.append(h)
        if id_col == [] or date_col == []:
            print("Could not find what you wanted")
            break
        # Make a list of corresponding positions by matching
        # id headers and date headers
        pos = []
        for i in id_col:
            id_string = headers[i]
            id_col_digit = [int(s) for s in id_string.split("_") if
                            s.isdigit()]
            for j in date_col:
                date_string = headers[j]
                date_col_digit = [int(s) for s in date_string.split("_") if
                                  s.isdigit()]
                if id_col_digit == date_col_digit:
                    pos.append([i, j])
        # Write the relevant information to a new csv file
        write_date_csv(in_file, reader, pos, headers)
