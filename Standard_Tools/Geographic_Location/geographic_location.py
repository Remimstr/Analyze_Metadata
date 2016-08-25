#!/usr/bin/env python

# Author: Remi Marchand
# Date: June 1, 2016
# Description: Parses geographic locations into a unified format

import os
import re

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

path = os.path.dirname(__file__) + "/"

# Global variables
keys = ["LOCATION", "ORIGINAL", "COLLECTION_NOTES"]
# column_strs is a list of strings representing columns of interest
column_strs = ["country", "geo_loc_name", "geographic_location",
               "geographic_location_(country_and/or_sea,region)"]

# Paths to the relevant files
paths = {"cr": path + "Country_Replacements.txt",
         "gl": path + "Geo_Library.txt",
         "sp": path + "State_Province.txt"}

# parse_files: openfile, Str, Str -> Dict
# This function is specifically designed to open and parse the following files:
# "Country_Replacements.txt" and "Geo_Library.txt". It returns all of the
# information found as a dictionary specific to the file being parsed.
# Country_Replacments: {key = country regex: value = std. country name}
# Geo_Library: {key = std. country name: value = listof(std. province name)}


def parse_files(open_file, regex, option):
    data = {}
    for line in open_file:
        # Use a regular expression to split each line
        split_line = re.split(r"%s" % regex, line)
        # Add the data to the dict
        if option == "cr":
            data[split_line[0]] = split_line[1].strip("\n")
        elif option == "sp":
            data[split_line[2]] = [split_line[0], split_line[1]]
        elif option == "gl":
            country = split_line[0]
            province = split_line[1]
            if country in data.keys():
                data[country].append(province)
            else:
                data[country] = [province]
    return data


# parse_sp_data: openfile, Str, Str -> (listof Str)
# This function is specifically designed to open and parse "State_Province.txt"
# It returns all of the information found as a list of state_province info.
# State_Province: {key = std. prov. name: [prov. name, std. country name]}
def parse_sp_data(open_file, regex, option):
    data = []
    for line in open_file:
        # Use a regular expression to split each line
        split_line = re.split(r"%s" % regex, line)
        data.append(split_line[:-1])
    return data

# return_dicts: None -> Dict
# This function is specifically designed to open and parse the files in paths


def return_dicts():
    # Set the regular expressions needed for each file
    cr_re, gl_re, sp_re = ":", "[\|(\n)]", "[\|(\t)(\n)]"
    cr, gl, sp = open(paths["cr"]), open(paths["gl"]), open(paths["sp"])
    cr_data = parse_files(cr, cr_re, "cr")
    gl_data = parse_files(gl, gl_re, "gl")
    sp_data = parse_sp_data(sp, sp_re, "sp")
    cr.close(), gl.close(), sp.close()
    return([cr_data, gl_data, sp_data])

# *************************************************************************** #

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
    out_string, collection_note = "", ""
    return_vals = [""] * len(keys)
    # Import files that contain parsing information
    cr_data, gl_data, sp_data = geo_info
    # Split the string according via colon and proceeding whitespace
    raw_loc = raw_loc.strip()
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
            out_string += ":" + province
        # If neither country nor province found, consider it a country failure
        else:
            collection_note += country
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
    return_vals[keys.index("LOCATION")] = out_string
    return_vals[keys.index("ORIGINAL")] = raw_loc
    return_vals[keys.index("COLLECTION_NOTES")] = collection_note
    return return_vals
