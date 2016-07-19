#!/usr/bin/evn python

# Author: Remi Marchand
# Date: June 10, 2016
# Descrition: Parses serovar information from .csv's into a unified format

import os

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/SpellCheck/")
path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/Resources/"
from intelligent_suggest import intelligent_suggest

# Global variables
keys = ["CURATED", "VARIANT", "OTHER_INFO", "ORIGINAL", "SUGGESTION"]
# column_strs is a list of strings representing columns of interest
column_strs = ["serovar"]

list_f = path + "/Standard_Files/Standard_Serovars.txt"
index_f = path + "/Index_Files/Standard_Serovars_Index.txt"


def spellcheck(word_target, list_file=list_f, index_file=index_f):
    item_suggest = intelligent_suggest(list_file, index_file)
    suggestions = item_suggest.suggest(word_target)
    if suggestions == {}:
        return "No Suggestions"
    top_sug, min_score = min(suggestions.iteritems(), key=lambda p: p[1])
    if min_score > 34:
        return "Score Failure"
    else:
        return top_sug


def parse(raw_serovar, sero_info):
    return_vals = ["", "", "", "", ""]
    return_vals[3] = raw_serovar
    if raw_serovar == "":
        return return_vals
    raw_serovar = raw_serovar.lower().strip()
    for key in sero_info.keys():
        if raw_serovar == key.lower().strip():
            new_sero_info = sero_info[key]
            return_vals[0] = new_sero_info[0]
            return_vals[1] = new_sero_info[1]
            return_vals[2] = new_sero_info[2]
            return return_vals
    return_vals[4] = spellcheck(raw_serovar)
    return return_vals
