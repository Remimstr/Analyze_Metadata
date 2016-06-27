#!/usr/bin/env python

# Written by: Remi Marchand - June 20, 2016

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import csv
from intelligent_suggest import intelligent_suggest

word_size = 3
word_targets = "../Resources/Messed_Serovars.txt"
word_list_file = "../Resources/Standard_Serovars.txt"
word_index_file = "../Resources/Standard_Serovars_Index.txt"
csv_file = "../Tested_Serovars.csv"
item_suggest = intelligent_suggest(word_list_file, word_index_file)


def openFile(filename, delimiter=None):
    match_dict = {}
    with open(filename, "rU") as open_file:
        for i, line in enumerate(open_file):
            match_dict[i] = line.strip("\n").split(delimiter)
    return match_dict

def write_to_csv(filename, data):
    with open(filename, "w") as csvfile:
        headers = ["Original", "Mutated", "Spellchecked", "Score"]
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(headers)
        for line in data:
            writer.writerow(line)

def run():
    targets = openFile(word_targets, delimiter="\t")
    out_data = []
    for target in targets.values():
        suggestions = item_suggest.suggest(target[1])
        if suggestions == {}:
            out_data.append([target[0], target[1], None, None])
            continue
        lowest_score, top_suggestion = 1000000, ""
        for suggest, score in suggestions.iteritems():
            if score < lowest_score:
                lowest_score = score
                top_suggestion = suggest
            # out_data.append([target[0], target[1], suggest, str(score)])
        out_data.append([target[0], target[1], top_suggestion, str(lowest_score)])
    write_to_csv(csv_file, out_data)


if __name__ == "__main__":
    run()
