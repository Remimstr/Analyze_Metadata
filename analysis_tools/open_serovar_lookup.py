#!/usr/bin/evn python

# Author: Remi Marchand
# Date: June 10, 2016
# Descrition: A function to open serovar lookup files for parsing

import os
import csv

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Get the relative path of the script
path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/Resources/"

# Paths to the relevant files
paths = {"sl": path + "Serovar_Replacement_Lookup.csv"}


# return_dicts: None -> Dict
# This function is specifically designed to open and parse the file:
# "Serovar_Replacement_Lookup.txt"

def return_dicts():
    data = {}
    print paths["sl"]
    with open(paths["sl"], "rU") as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in csv_reader:
            data[i[0]] = [j for j in i[1:]]
    return data
