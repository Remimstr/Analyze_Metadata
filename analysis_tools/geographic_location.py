#!/usr/bin/evn python

# Author: Remi Marchand
# Date: June 1, 2016
# Descrition: Parses geographic locations from .csv's into a unified format

import re
import utils

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Global variables
keys = ["LOCATION", "ORIGINAL", "COLLECTION_NOTES"]
# column_strs is a list of strings representing columns of interest
column_strs = ["country", "geo_loc_name", "geographic_location",
               "geographic_location_(country_and/or_sea,region)"]

# generic_match: Str -> Bool
# This function returs True if both items, item1, and item2 match exactly,
# except for case.


def generic_match(item1, item2):
    if item1 != "" and item2 != "":
        match = re.match((r"%s" % item1), item2, flags=re.IGNORECASE)
        return match
    else:
        return False

# parse: Str -> Dict
# This function attempts to parse the geographic location from a string,
# raw_loc. It returns a dictionary of values including the parsed location
# (if it exists) with key == keys[0] (default: "LOCATION"), the flag value,
# representing the original value if it fails to parse with key == keys[1]
# (default: "FLAG").


def parse(raw_loc, geo_info):
    # Import files that contain parsing information
    cr_data, gl_data, sp_data = geo_info

    formatted_loc = re.split(r":\s*", raw_loc)
    country, province = "", ""
    if len(formatted_loc) > 0:
        country = formatted_loc[0]
    if len(formatted_loc) > 1:
        province = formatted_loc[1]
    collection_note = ""
    # Standardize the country if it exists
    for key in cr_data.keys():
        if generic_match(key, country):
            country = cr_data[key]
            break
    # If a province is present, standardize it also
    for loc in sp_data:
        if generic_match(loc[0], province) and \
           generic_match(loc[1], country):
            province = loc[2]
            break
    # Figure out what values to add to each column of the output dictionary
    return_vals = {}
    out_string, original_string = "", ""
    for key, values in gl_data.iteritems():
        # If the country is equal to the key, add it to the output
        if country == key:
            out_string += country
            # Add the province if it is in the list of values of the country
            if province in values and province != "":
                out_string += ":" + province
    # If elements were not found, place the data in the key column
    if province != "" and province not in out_string:
        collection_note += "Province: %s" % province
    elif country != "" and country not in out_string:
        original_string = out_string
        out_string = ""
    # Set the output values
    return_vals[keys[0]] = out_string
    return_vals[keys[1]] = original_string if original_string != "" else \
        raw_loc
    return_vals[keys[2]] = collection_note
    return return_vals

if __name__ == "__main__":
    for in_file in sys.argv[1:]:
        utils.find_and_write("RUN", column_strs, keys,
                             in_file, "geographic_location", "geo_locs")
