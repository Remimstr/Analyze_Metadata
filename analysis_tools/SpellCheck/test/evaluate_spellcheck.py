#!/usr/bin/env python

# Written by: Remi Marchand - June 20, 2016

import csv

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append("..")
sys.path.append("~/Desktop")
from intelligent_suggest import intelligent_suggest

word_size = 3

fileSet = {"Countries": ["Messed_Countries.txt",
                         "../../Resources/Standard_Countries.txt",
                         "../../Resources/Standard_Countries_Index.txt",
                         "Tested_Countries.csv"],

           "Provinces": ["Messed_Provinces.txt",
                         "../../Resources/Standard_Provinces.txt",
                         "../../Resources/Standard_Provinces_Index.txt",
                         "Tested_Provinces.csv"],

           "Serovars": ["Messed_Serovars.txt",
                        "../../Resources/Standard_Serovars.txt",
                        "../../Resources/Standard_Serovars_Index.txt",
                        "Tested_Serovars.csv"]}


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


def run(word_targets, list_file, index_file, csv_file):
    targets = openFile(word_targets, delimiter="\t")
    out_data = []
    item_suggest = intelligent_suggest(list_file, index_file)
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
    if sys.argv[1] in fileSet.keys():
        files = fileSet[sys.argv[1]]
    else:
        files = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    run(*files)
