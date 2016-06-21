#!/usr/bin/evn python

# Modified by: Remi Marchand
# Original Author: Peter Norvig, http://norvig.com/spell-correct.html
# Date: June 13, 2016
# Description: Creates all permutations of the input string to then compare
# against the Serovar_Replacement_Lookup file

import re
import csv
import collections


def words(text):
    return re.findall('[a-z]+', text.lower())


def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

with open("Serovar_Replacement_Lookup.csv", "rU") as csv_file:
    match_list = []
    reader = csv.reader(csv_file)
    for line in reader:
        match_list.append(line[0])
    NWORDS = train(match_list)

alphabet = "abcdefghijklmnopqrstuvwxyz123456789.() "


def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


def known(words):
    return set(w for w in words if w in NWORDS)


def correct(word):
    candidates = known([word]) or known(edits1(word)) or [word]
    return max(candidates, key=NWORDS.get)

if __name__ == "__main__":
    print correct("1,4,[5]-,12:e,h:-")
