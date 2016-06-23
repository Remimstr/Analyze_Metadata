#!/usr/bin/env python

# Original Method: James Robertson as KmerTdf_Idf.php
# Python Version: Remi Marchand - June 14, 2016
# Description: Class to build on the functionality of kmer_similarity. It uses
#              the alphabet-based kmer array produced by kmer_similarity as a
#              reference against which to compare k-mers found in the input
#              file (filename).

import math
from kmer_similarity import Kmer_Similarity

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

msg = "It looks like this kmer has an element that is not in the \
alphabet provided: %s"


class KmerTdf_Idf(Kmer_Similarity):
    def __init__(self):
        Kmer_Similarity.__init__(self)
        self.entity_assoc = {}
        self.num_entity = 0
        self.kmer_freq = {}
        self.kmer_weights = {}
        self.entity_list = {}
        self.kSize = 3

    def init(self, filename):
        num_combinations = self.num_combinations
        for x in range(num_combinations):
            self.kmer_weights[x] = 0
            self.kmer_freq[x] = 0
        contents = self.openFile(filename)
        size = self.getkSize()
        for i, line in contents.iteritems():
            line = line.strip()
            self.addEntity(i, line)
            line = line.lower()
            kmers = self.processLine(line)
            for k in kmers.values():
                if len(k) != size:
                    continue
                pos = self.calc_position(k)
                if pos < 0:
                    print msg % k
                increment = self.getFreq(pos) + 1
                self.setFreq(pos, increment)
                if len(self.getAssoc(pos)) == 0:
                    self.setAssoc(pos, i)
                else:
                    self.setAssoc(pos, self.getAssoc(pos) + "," + str(i))
        self.calc_word_weights()

    def calc_word_weights(self):
        numDocs = len(self.entity_list)
        for pos, insts in self.entity_assoc.iteritems():
            numInstWithWord = len(str(insts).split(","))
            idf = math.log((numDocs / numInstWithWord), 10)
            self.setWeight(pos, idf)

    def setAssoc(self, pos, entity):
        self.entity_assoc[pos] = str(entity)

    def getAssoc(self, pos):
        if pos in self.entity_assoc:
            return self.entity_assoc[pos]
        else:
            return ""

    def addEntity(self, pos, entity):
        self.entity_list[pos] = entity

    def processLine(self, line):
        length = len(line)
        kmers = {}
        size = self.getkSize()
        for i in range(length):
            piece = line[i:(i + size)]
            if len(piece) == 3:
                kmers[i] = piece
        return kmers

    def setkSize(self, s):
        self.kSize = s

    def getkSize(self):
        return self.kSize

    def getWeight(self, pos):
        return self.kmer_weights[pos]

    def setWeight(self, pos, w):
        self.kmer_weights[pos] = w

    def getFreq(self, pos):
        return self.kmer_freq[pos]

    def setFreq(self, pos, count):
        self.kmer_freq[pos] = count

    def openFile(self, filename):
        match_dict = {}
        with open(filename, "rU") as open_file:
            for i, line in enumerate(open_file):
                match_dict[i] = line.strip("\n")
        return match_dict
