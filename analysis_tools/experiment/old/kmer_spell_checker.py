#!/usr/bin/evn python

# Created by: Remi Marchand
# Date: June 13, 2016
# Description: Divides the query string into all possible permutations of
# length k and compares against a list of original serovars.

import csv

class Kmer_info:
    def __init__(self):
        self.entity_assoc = {}
        self.num_entity = 0
        self.entity_list = {}
        self.kmer_weights = {}
        self.kmer_freq = {}
        self.kmer_entity_list = {}
        self.kSize = 3

    def run(self, contents):
        q_kmers = processLine(query)
        for i in q_kmers.keys():
            self.kmer_weights[i] = 0
            self.kmer_freq[i] = 0
        size = getkSize()
        for i, line in contents:
            line = line.strip()
            addEntity(i, line)
            line = line.lower()
            kmers = processLine(line)
            for k in kmers.keys():
                pos = q_kmers

    def processLine(line):
        kmers = {}
        for i in range(len(string)):
            kmer = string[i:i + kSize]
            if len(kmer) == kSize:
                kmers[i] = kmer
        return kmers


with open("Serovar_Replacement_Lookup.csv", "rU") as csv_file:
    match_dict = {}
    reader = csv.reader(csv_file)
    for pos in range(len(reader)):
        match_dict[pos] = reader[pos]
