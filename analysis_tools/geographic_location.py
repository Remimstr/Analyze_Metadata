#!/usr/bin/evn python

# Author: Remi Marchand
# Date: June 1, 2016
# Descrition: Parses geographic locations from .csv's into a unified format

import utils

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Global variables
item_key = "LOCATION"
other_keys = ["FLAG"]

# This script takes in a list of metadata csv files, parses the collection
# dates out of each one, and produces a new csv containing those dates
for in_file in sys.argv[1:]:
    utils.find_and_write("RUN", "collection_date", item_key, other_keys,
                         in_file, "collection_date")
