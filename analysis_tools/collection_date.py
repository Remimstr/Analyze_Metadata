#!/usr/bin/env python

# Author: Remi Marchand
# Date: May 24, 2016
# Description: Parses collection dates from .csv's into a unified format

import math
import utils
import calendar
import dateparser
import datetime
from datetime import date

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Global variables
keys = ["DATE", "ERROR", "FLAG"]
today = date.today()
this_year = today.year

# ambiguous_dates: datetime -> Bool
# This function consumes a datetime object and outputs True if the date
# is ambiguous (ex. 2016-01-03 could be January 3rd, 2016 or March 1st, 2016)
# Output False otherwise.


def ambiguous_dates(d):
    times = [d["date_obj"].year, d["date_obj"].month, d["date_obj"].day]
    if len([i for i in times if (i < 12)]) > 1:
        return True
    else:
        return False

# parse: Str -> Dict
# This function attempts to parse the date from a string, raw_date
# It returns a dictionary of values including the parsed date (if it exists)
# with key == keys[0] (default: "DATE"), the error value, consisting of
# the amount of error allowed for the given date value parsed with
# key == keys[1] (default: "ERROR"), the flag value, representing the
# original value if it fails to parse with key == keys[2]
# (default: "FLAG").


def parse(raw_date):
    return_vals = {}
    date_parser = dateparser.DateDataParser(languages=["en"])
    date_obj = date_parser.get_date_data(raw_date)
    new_date, error, flag = "", "", ""
    if date_obj["date_obj"] is None:
        flag = raw_date
    elif date_obj["period"] == "day" and ambiguous_dates(date_obj):
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
            leap = True if calendar.isleap(date_obj["date_obj"].year) \
                else False
            year_count = 366 if leap else 365
            error = int(math.ceil(year_count) / 2.0)
            new_date = date_obj["date_obj"].replace(day=1, month=1)
            new_date += datetime.timedelta(days=error - 1)
        new_date = new_date.strftime("%Y-%b-%d")
    return_vals[keys[0]] = new_date
    return_vals[keys[1]] = error
    return_vals[keys[2]] = flag
    return return_vals


for in_file in sys.argv[1:]:
    utils.find_and_write("RUN", ["collection_date"], keys,
                         in_file, "collection_date")
