#!/usr/bin/env python

# Author: Remi Marchand
# Date: May 24, 2016
# Description: Parses collection dates from .csv's into a unified format

import re
import math
import calendar
import dateparser
import datetime

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Global variables
keys = ["DATE", "ERROR", "ORIGINAL", "AMBIGUOUS"]
# column_strs is a list of strings representing columns of interest
column_strs = ["collection_date"]
today = datetime.date.today()
this_year = today.year

# ambiguous_dates: datetime -> Bool
# This function consumes a datetime object and outputs True if the date
# is ambiguous (ex. 2016-01-03 could be January 3rd, 2016 or March 1st, 2016)
# Output False otherwise.


def ambiguous_dates(d, ambiguity=False):
    if d["date_obj"] is not None and d["period"] == "day":
        times = [d["date_obj"].year, d["date_obj"].month, d["date_obj"].day]
        if len([i for i in times if (i <= 12)]) > 1:
            ambiguity = True
    return ambiguity

# parse_other: Str -> [Str, Str]
# This function handles exceptions by parsing dates that fail the dateparser
# but can be interpreted manually


def date_exceptions(raw_date):
    match_year = "[1, 2][0-9]{3}"
    # This code parses two dates separated by a dash(-) or foreward slash (/)
    # ex. 2008/2010
    if re.match(r"%s[-/]%s" % (match_year, match_year), raw_date):
        two_years = re.split(r"[-/]", raw_date)
        two_years = [int(i) for i in two_years]
        for i in two_years:
            if i > this_year:
                return ["", ""]
            two_years[two_years.index(i)] = datetime.datetime(i, 1, 1)
        diff = abs((two_years[0] - two_years[1]) / 2)
        new_date = (two_years[0] + diff).strftime("%Y-%b-%d")
        return [diff.days, new_date]
    return ["", ""]


# parse: Str -> Dict
# This function attempts to parse the date from a string, raw_date
# It returns a dictionary of values including the parsed date (if it exists)
# with key == keys[0] (default: "DATE"), the error value, consisting of
# the amount of error allowed for the given date value parsed with
# key == keys[1] (default: "ERROR"), the flag value, representing the
# original value if it fails to parse with key == keys[2]
# (default: "FLAG").


def parse(raw_date):
    return_vals = []
    date_parser = dateparser.DateDataParser(languages=["en"])
    date_obj = date_parser.get_date_data(raw_date)
    new_date, error = "", ""
    valid = date_obj["date_obj"] is not None
    flag, ambiguous = raw_date, ambiguous_dates(date_obj)
    if valid:
        # If the precision is "day" then we're good to process as is
        if date_obj["period"] == "day":
            error = 0
            new_date = date_obj["date_obj"]
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
            error = int(math.floor(year_count) / 2.0)
            new_date = date_obj["date_obj"].replace(day=1, month=1)
            new_date += datetime.timedelta(days=error - 1)
        new_date = new_date.strftime("%Y-%b-%d")
    # If the date has failed to parse so far, run custom parsers on it
    else:
        error, new_date = date_exceptions(raw_date)
    return_vals.append(new_date)
    return_vals.append(error)
    return_vals.append(flag)
    return_vals.append(ambiguous if ambiguous is True else "")
    return return_vals
