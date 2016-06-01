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

today = date.today()
this_year = today.year

# Global variables
item_key = "DATE"
other_keys = ["FLAG", "ERROR"]


def ambiguous_dates(d):
    times = [d["date_obj"].year, d["date_obj"].month, d["date_obj"].day]
    if len([i for i in times if (i < 12)]) > 1:
        return True
    else:
        return False


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
    return_vals[item_key] = new_date
    return_vals[other_keys[0]] = flag
    return_vals[other_keys[1]] = error
    return return_vals


# This script takes in a list of metadata csv files, parses the collection
# dates out of each one, and produces a new csv containing those dates
for in_file in sys.argv[1:]:
    utils.find_and_write("RUN", "collection_date", item_key, other_keys,
                         in_file, "collection_date")
