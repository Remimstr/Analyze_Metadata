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


def parse_some_dates(raw_date):
    date_parser = dateparser.DateDataParser(languages=["en"])
    if raw_date == "":
        return(None, "")
    date_obj = date_parser.get_date_data(raw_date)
    if date_obj is None:
        return(None, "Unable_To_Parse")
    # If the precision is "day" then we're good to process as is
    if date_obj["period"] == "day":
        return(date_obj["date_obj"], 0)
    # If the precision is "month", adjust accordingly
    if date_obj["period"] == "month":
        month, year = date_obj["date_obj"].month, date_obj["date_obj"].year
        accuracy = int(math.ceil(calendar.monthrange(year, month)[1] / 2.0))
        new_date = date_obj["date_obj"].replace(day=accuracy)
        return(new_date, accuracy)
    # If the precision is "year", adjust accordingly
    if date_obj["period"] == "year":
        leap = True if calendar.isleap(date_obj["date_obj"].year) else False
        year_count = 366 if leap else 365
        accuracy = int(math.ceil(year_count) / 2.0)
        new_date = date_obj["date_obj"].replace(day=1, month=1)
        new_date += datetime.timedelta(days=accuracy - 1)
        return(new_date, accuracy)


for in_file in sys.argv[1:]:
    # For each entry in the csv file, retrieve the run numbers
    # and the collection dates
    with open(in_file, "rb") as csvin:
        reader = csv.reader(csvin, delimiter=",")
        headers = reader.next()
        id_col, date_col = [], []
        IDs, DATES = [], []
        for h in range(0, len(headers)):
            if "RUN" in headers[h]:
                id_col.append(h)
            if "collection_date" in headers[h]:
                date_col.append(h)
        if id_col == [] or date_col == []:
            print("Could not find what you wanted")
            break
        # Make a list of corresponding positions
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
        with open(in_file[:-4] + "_collection_date.csv", "wb") as csvout:
            csvwriter = csv.writer(csvout, delimiter=",")
            new_headers = [headers[key] for key in flatten(pos)]
            print(new_headers)
            # Add the ACC field to the headers
            new_headers = [x for y in (new_headers[i:i + 2] + ['ACCURACY'] *
                           (i < len(new_headers) - 1) for i in xrange(0,
                           len(new_headers), 2)) for x in y]
            print(new_headers)
            csvwriter.writerow(new_headers)
            for line in reader:
                print_list = []
                for p in pos:
                    ID, DATE, ACC = None, None, None
                    ID = line[p[0]]
                    DATE = line[p[1]]
                    date_info = parse_some_dates(DATE)
                    if date_info[0] is None:
                        DATE = date_info[1]
                    else:
                        DATE = date_info[0].strftime("%Y-%b-%d")
                    ACC = date_info[1]
                    print_list.extend([ID, DATE, ACC])
                csvwriter.writerow(print_list)
