#!/usr/bin/env python

# Author: Remi Marchand
# Date: June 10, 2016
# Description: Perfoms multi-level parsing of a data type of interest.
# This starts with a query word and undergoes the following steps:
# 1. Single Word Replacement: (replace_words)
# 2. Standardized List Querying
# 3. Full Query Spellchecking: (spellcheck)

import os

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/SpellCheck/")
from intelligent_suggest import intelligent_suggest

# Global variables
keys = ["CURATED", "ORIGINAL", "SUGGESTION"]


def spellcheck(word_target, info):
    list_file, index_file = info["lif"], info["inf"]
    item_suggest = intelligent_suggest(list_file, index_file)
    suggestions = item_suggest.suggest(word_target)
    if suggestions == {}:
        return "No Suggestions"
    top_sug, min_score = min(suggestions.iteritems(), key=lambda p: p[1])
    if min_score > 24:
        return "Score Failure"
    else:
        return top_sug

# repl_dict: Dict -> Dict
# This function takes in a dictionary of equivalent words and splits
# up the terms, returning them int a new dictionary.


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

# replace_words: Dict, Str -> Str
# This function takes in a string, replace_string, splits into its
# individual words by whitespace, and replaces each word if found
# in the replacements dictionary.


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


def parse(source, info):
    replacements, eq_words = info["isr"], info["eqw"]
    return_vals = ["", "", ""]
    return_vals[1] = source
    source = replace_words(repl_dict(eq_words), source)
    if source == "":
        return return_vals
    source = source.lower().strip()
    for key in replacements.keys():
        if source == key.lower().strip():
            return_vals[0] = replacements[key]
            return return_vals
    return_vals[2] = spellcheck(source, info)
    return return_vals
