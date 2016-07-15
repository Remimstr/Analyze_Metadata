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
keys = ["CURATED", "ORIGINAL", "SUGGESTION"]
# column_strs is a list of strings representing columns of interest
column_strs = ["isolation_source"]

list_f = path + "Standard_Files/Standard_Isolation_Sources.txt"
index_f = path + "Index_Files/Standard_Isolation_Sources_Index.txt"

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

def repl_dict(eq_words):
    replacements = {}
    for key, line in eq_words.iteritems():
        items = key.split(",")
        for i in items:
            i = i.strip()
            if i not in replacements.keys():
                replacements[i] = line
            else:
                replacements[i] = replacements[i] + line
    return replacements

def replace_words(replacements, replace_string):
    # Tear the string apart by whitespace, replace words
    # that are found, and rebuild
    word_list = replace_string.split(" ")
    for pos in range(len(word_list)):
        word = word_list[pos]
        for key in replacements.keys():
            if word.lower() == key.lower():
                word_list[pos] = replacements[key]
    return " ".join(word_list)


def parse(isolation_source, iso_src_info):
    iso_src_info, eq_words = iso_src_info
    return_vals = {keys[0]: "", keys[1]: "", keys[2]: ""}
    return_vals[keys[1]] = isolation_source
    isolation_source = replace_words(repl_dict(eq_words), isolation_source)
    if isolation_source == "":
        return return_vals
    isolation_source = isolation_source.lower().strip()
    for key in iso_src_info.keys():
        if isolation_source == key.lower().strip():
            new_iso_src_info = iso_src_info[key]
            return_vals[keys[0]] = new_iso_src_info
            return return_vals
    return_vals[keys[2]] = spellcheck(isolation_source)
    return return_vals
