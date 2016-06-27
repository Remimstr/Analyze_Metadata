#!/usr/bin/env python

# Original Method: James Robertson as test.php
# Python Version: Remi Marchand - June 20, 2016

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from intelligent_suggest import intelligent_suggest

word_size = 3
word_targets = "../Resources/Original_Serovars.txt"
word_list_file = "../Resources/Standard_Serovars.txt"
word_index_file = "../Resources/Standard_Serovars_Index.txt"
item_suggest = intelligent_suggest(word_list_file, word_index_file)


def openFile(filename):
    match_dict = {}
    with open(filename, "rU") as open_file:
        for i, line in enumerate(open_file):
            match_dict[i] = line.strip("\n")
    return match_dict


def run():
    targets = openFile(word_targets)
    out_data = {}
    for target in targets.values():
        suggestions = item_suggest.suggest(target)
        for suggest, score in suggestions.iteritems():
            if score > 34:
                continue
            # print target + "\t" + suggest + "\t" + str(score) + "\n"
            out_data[target] = [suggest, score]
    return out_data


if __name__ == "__main__":
    run()
