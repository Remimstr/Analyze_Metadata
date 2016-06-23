#!/usr/bin/env python

# Original Method: James Robertson as test.php
# Python Version: Remi Marchand - June 20, 2016
# Description: I don't know what this does yet

import sys
sys.path.append("..")

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
