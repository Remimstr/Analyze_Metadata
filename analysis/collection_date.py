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

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

today = date.today()
this_year = today.year

year_list = [x for x in range(this_year)]
month_list = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May",
              "06": "Jun", "07": "Jul", "08": "Aug", "09": "Sep",
              "10": "Oct", "11": "Nov", "12": "Dec"}

def parse_some_dates(raw_date):
    date_parser = dateparser.DateDataParser(languages=["en"])
    date_obj = date_parser.get_date_data(raw_date)
    # If the precision is "day" then we're good to process as is
    if date_obj["period"] == "day":
        print(date_obj["date_obj"])
        print("Day Precision")
    # If the precision is "month", adjust accordingly
    if date_obj["period"] == "month":
        month, year = date_obj["date_obj"].month, date_obj["date_obj"].year
        day = int(math.ceil(calendar.monthrange(year, month)[1] / 2.0))
        new_date = date_obj["date_obj"].replace(day=day)
        print(new_date)
        print("Accuracy = %s" % day)
        print("Month Precision")
    # If the precision is "year", adjust accordingly
    if date_obj["period"] == "year":
        leap = True if calendar.isleap(date_obj["date_obj"].year) else False
        year_count = 366 if leap else 365
        accuracy = int(math.ceil(year_count) / 2.0)
        new_date = date_obj["date_obj"].replace(day=1, month=1)
        new_date += datetime.timedelta(days=accuracy - 1)
        print(new_date)
        print("Accuracy = %s" % accuracy)
        print("Year Precision")
    # regx = re.compile('[-/]')
    # y, m, d = regx.split(raw_date)
    # new_date = "-".join((("20" + y.zfill(2) if len(y) == 2 else y),
    #                     month_list[m].zfill(2), d.zfill(2)))
    # print(new_date)




for i in sys.argv[1:]:
    # For each entry in the csv file, retrieve the run number and the collection
    # date

    with open(i, "rb") as csvfile:
        reader = csv.reader(csvfile)
        headers = reader.next()
        id_col = None
        date_col = None
        for h in range(0, len(headers)):
            if "PRIMARY_ID" == headers[h]:
                id_col = h
            if "collection_date" in headers[h]:
                date_col = h
        for i in reader:
            # Print the SRR number:
            # print[s for s in i[id_col].split(",") if "SRR" in s or "ERR" in s]
            if i[date_col] == "":
                print("None")
            else:
                parse_some_dates(i[date_col])
