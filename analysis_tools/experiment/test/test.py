#!/usr/bin/env python

# Created by: Remi Marchand
# Date: June 20, 2016
# Descriptions: I don't know what this does yet

import sys
sys.path.append("..")

from TF_IDF_SimilaritySearch import TF_IDF_SimilaritySearch
from SpellCheck import SpellCheck
from KmerTdf_Idf import KmerTdf_Idf
from intelligent_suggest import intelligent_suggest

word_size = 3
word_targets = "incorrect_coworkers.txt"
word_list_file = "coworkers.txt"
word_index_file = "coworkers_index_php.txt"
item_suggest = intelligent_suggest(word_list_file, word_index_file)


def openFile(filename):
    match_dict = {}
    with open(filename, "rU") as open_file:
        for i, line in enumerate(open_file):
            match_dict[i] = line.strip("\n")
    return match_dict

targets = openFile(word_targets)
for target in targets.values():
    suggestions = item_suggest.suggest(target)
    for suggest, score in suggestions.iteritems():
        if score > 34:
            continue
        print target + "\t" + suggest + "\t" + str(score) + "\n"
