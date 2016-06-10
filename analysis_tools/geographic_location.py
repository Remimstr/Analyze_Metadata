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
# ingnoring differences in case (upper and lower) if there are any.


def generic_match(item1, item2):
    if item1 != "" and item2 != "":
        match = re.match((r"%s$" % item1), item2, flags=re.IGNORECASE)
        return match
    else:
        return False

# standardize_country: Str Dict -> Str
# This function standardizes a query_country against a dict of standardized
# countries, cr_data. If query_country is found in cr_data, it returns the
# standardized country, otherwise it returns query_country.


def standardize_country(query_country, cr_data):
    for key in cr_data.keys():
        if generic_match(key, query_country):
            return cr_data[key]
    return query_country

# standardize_province: Str Str Dict -> Str
# This function standardizes a query_province using a dict of standardized
# provinces, sp_data. If query_province is found in sp_data, it returns the
# standardized province, otherwise it returns query_province. If a country is
# specified, it will ensure that the country and province match, otherwise
# we skip this step.


def standardize_province(query_province, sp_data, country=None):
    for loc in sp_data:
        if country is not None:
            if generic_match(loc[0], query_province) and \
                    generic_match(loc[1], country):
                return loc[2]
        else:
            if generic_match(loc[0], query_province):
                return loc[2]
    return query_province

# search_for_country: Str Dict -> Str or False
# This function searches for a country in a standardized dict of countries,
# gl_data. If the country is found, it returns the country, otherwise it
# returns false.


def search_for_country(country, gl_data):
    for key in gl_data.keys():
        if country == key:
            return country
    return False

# search_for_province: Str Dict -> Str or False
# This function searches for a province in a standardized dict of countries,
# gl_data. If the province is found, it returns the province, otherwise it
# returns false. If a country is specified, it will ensure that the country
# and province match, otherwise we skip this step.


def search_for_province(province, gl_data, country=None):
    for key, values in gl_data.iteritems():
        if country is not None:
            for v in values:
                if country == key and v == province:
                    return province
        else:
            for v in values:
                if v == province:
                    return province
    return False

# parse: Str -> Dict
# This function attempts to parse the geographic location from a string,
# raw_loc. It returns a dictionary of values including the parsed location
# (if it exists) with key == keys[0] (default: "LOCATION"), the flag value,
# representing the original value if it fails to parse with key == keys[1]
# (default: "FLAG").


def parse(raw_loc, geo_info):
    out_string, collection_note, return_vals = "", "", {}
    # Import files that contain parsing information
    cr_data, gl_data, sp_data = geo_info
    # Split the string according via colon and proceeding whitespace
    formatted_loc = re.split(r":\s*", raw_loc)
    # Remove whitespace characters on either end of the string
    formatted_loc = [i.strip() for i in formatted_loc]
    # If there is only one location, we will attempt to figure out what it is
    if len(formatted_loc) == 1:
        loc_str = formatted_loc[0]
        # Attempt to standardize the string and then search for the country
        country = standardize_country(loc_str, cr_data)
        province = standardize_province(loc_str, sp_data)
        if search_for_country(country, gl_data):
            out_string += country
        # Search for the province
        elif search_for_province(province, gl_data):
            out_string += province
            collection_note += ":" + province
        # See if it's formatted as "Province, Country" ex. New York, USA
        '''
        else:
            split_string = re.split(r"\,\s*", formatted_loc[0])
            if len(split_string) == 2:
                x = comma_except(split_string, out_string, collection_note)
                out_string, collection_note = x
        '''
    # If there are multiple locations, check if the first one is a country
    # and if the province exists in any piece of the remaining string
    else:
        # Attempt to standardize the country part of the formatted_loc string
        # and add to the out_string if it is a valid country
        country = standardize_country(formatted_loc[0], cr_data)
        if (search_for_country(country, gl_data)):
            out_string += country
        # Split the remaining section of formatted_loc by comma and whitespace
        for sub in re.split(r"\,\s*", formatted_loc[1]):
            province = standardize_province(sub, sp_data, country)
            # Search for the province
            if (search_for_province(province, gl_data, country)):
                out_string += ":" + province
                break
            else:
                collection_note += ":" + province
    # Set the output values
    return_vals[keys[0]] = out_string
    return_vals[keys[1]] = raw_loc
    return_vals[keys[2]] = collection_note
    return return_vals

if __name__ == "__main__":
    for in_file in sys.argv[1:]:
        utils.find_and_write("RUN", column_strs, keys,
                             in_file, "geographic_location", "geo_locs")
