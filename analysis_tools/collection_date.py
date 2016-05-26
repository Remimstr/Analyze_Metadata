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
    if date_obj is None:
        return(None, 0)
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
    # regx = re.compile('[-/]')
    # y, m, d = regx.split(raw_date)
    # new_date = "-".join((("20" + y.zfill(2) if len(y) == 2 else y),
    #                     month_list[m].zfill(2), d.zfill(2)))
    # print(new_date)


for i in sys.argv[1:]:
    # For each entry in the csv file, retrieve the run number
    # and the collection date

    with open(i, "rb") as csvin:
        reader = csv.reader(csvin)
        headers = reader.next()
        id_col = None
        date_col = None
        for h in range(0, len(headers)):
            if "PRIMARY_ID" == headers[h]:
                id_col = h
            if "collection_date" in headers[h]:
                date_col = h
        if id_col is None or date_col is None:
            break
        with open(i[:-4] + "_collection_date.csv", "wb") as csvout:
            headers = ["Run Number (DRR/ERR/SRR)", "Date", "Accuracy"]
            csvwriter = csv.writer(csvout, delimiter=",")
            csvwriter.writerow(headers)
            for i in reader:
                DATE = None
                ACC = None
                # Print the SRR number:
                SRR = [s for s in i[id_col].split(", ") if "SRR" in s or
                       "ERR" in s or "DRR" in s][0]
                if i[date_col] != "":
                    date_info = parse_some_dates(i[date_col])
                    if date_info[0] is None:
                        DATE = "UNABLE_TO_PARSE"
                    else:
                        DATE = date_info[0].strftime("%Y-%b-%d")
                    ACC = date_info[1]
                csvwriter.writerow([SRR, DATE, ACC])
