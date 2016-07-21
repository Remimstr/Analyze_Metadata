#!/usr/bin/env python

# Author: Remi Marchand
# Date: July 21, 2016
# Description: Functions that are universally used by Analysis Tools

import os
import csv

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/SpellCheck/")
from intelligent_suggest import intelligent_suggest


def spellcheck(target, info, score):
    list_file, index_file = info["std_file"], info["ind_file"]
    item_suggest = intelligent_suggest(list_file, index_file)
    suggestions = item_suggest.suggest(target)
    if suggestions == {}:
        return "No Suggestions"
    top_sug, min_score = min(suggestions.iteritems(), key=lambda p: p[1])
    if min_score > score:
        return "Score Failure"
    else:
        return top_sug

# *************************************************************************** #

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

# *************************************************************************** #


# simple_replace: None -> Dict
# This function is specifically designed to open and parse simple files in
# which there is one query value and one value returned.


def simple_replace(filepath):
    data = {}
    with open(filepath, "rU") as open_file:
        for line in open_file:
            line = line.replace("\n", "")
            line = line.replace("\"", "").split("\t")
            data[line[1]] = line[0]
    return data


# complex_replace: None -> Dict
# This function is specifically designed to open and parse files in which
# there is one query value with multiple values returned.


def complex_replace(filepath):
    data = {}
    with open(filepath, "rU") as csv_file:
        next(csv_file)
        csv_reader = csv.reader(csv_file)
        for i in csv_reader:
            data[i[0]] = [j for j in i[1:]]
    return data
