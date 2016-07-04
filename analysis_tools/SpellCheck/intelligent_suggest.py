#!/usr/bin/env python

# Original Method: James Robertson as intelligent_suggest.php
# Python Version: Remi Marchand - June 20, 2016
# Description: Class to make a suggestion for a list of words based on an index
#              file of kmers made from a reference list. It returns all
#              suggestions with their score.

from __future__ import division
import os
from Levenshtein import distance
from KmerTdf_Idf import KmerTdf_Idf
from SpellCheck import SpellCheck

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class intelligent_suggest:
    def __init__(self, word_list_fileName, word_index_fileName):
        self.word_size = 3
        self.spellCheckObj = None
        self.word_list_file = None
        self.word_index_file = None
        self.word_list = {}
        self.word_index = {}
        self.limit = 25
        self.candidates = {}
        self.lengthDiff = 50

        if not os.path.isfile(word_list_fileName):
            raise IOError("Error Word list -%s-file does not exist"
                          % word_list_fileName)
        if not os.path.isfile(word_index_fileName):
            raise IOError("Error Word list -%s-file does not exist"
                          % word_index_fileName)
        self.setWordIndexFile(word_index_fileName)
        self.setWordListFile(word_list_fileName)
        self.init()

    def sanityCheck(self):
        if not isinstance(self.spellCheckObj, SpellCheck):
            raise Exception("Error there is something wrong \
                            with the spell check object")
        if len(self.word_index) == 0:
            print "You have supplied an empty index file"
        if len(self.word_list) == 0:
            print "You have supplied an empty list file"

    def init(self):
        self.spellCheckObj = SpellCheck()
        self.spellCheckObj.build(self.getWordListFile())
        self.process_word_index()
        self.process_word_list()

    def setLimit(self, l):
        self.limit = l

    def getLimit(self):
        return self.limit

    def getWordSize(self):
        return self.word_size

    def setWordSize(self, s):
        self.word_size = s

    def setWordListFile(self, f):
        self.word_list_file = f

    def getWordListFile(self):
        return self.word_list_file

    def setWordIndexFile(self, f):
        self.word_index_file = f

    def getWordIndexFile(self):
        return self.word_index_file

    def ktuple_candidate_search(self, query):
        query = query.lower()
        kmer = KmerTdf_Idf()
        ktuples = kmer.processLine(query)
        candidates = {}
        tracker = 1
        entities = {}
        for k in ktuples.values():
            if k not in self.word_index.keys():
                continue
            entities = self.getWordAssociation(k).split(",")
            weight = self.getWordWeight(k)
            for e in entities:
                try:
                    e = int(e)
                except:
                    break
                if tracker == 1:
                    if e not in candidates.keys():
                        candidates[e] = 0
                if e not in candidates.keys():
                    continue
                candidates[e] = candidates[e] + weight
        return candidates

    def filter_results(self, query, candidates):
        limit = self.getLimit()
        filtered = {}
        tracker = 0
        qLen = len(query)
        for c, score in candidates:
            if tracker == limit:
                break
            word = self.getWordFromList(c)
            wLen = len(word)
            lDiff = abs(wLen - qLen) / qLen * 100
            if (query[0].lower() != word[0].lower()) or \
                    lDiff > self.lengthDiff:
                if query[0] == "k" or query[0] == "K": print word, lDiff
                continue
            if word is None:
                continue
            score = self.calcDistance(word, query)
            filtered[word] = score
            tracker += 1
        return filtered

    def calcDistance(self, str1, str2):
        str1, str2 = str1.lower(), str2.lower()
        return distance(str1, str2) / len(str2) * 100

    def process_word_index(self):
        contents = self.openFile(self.getWordIndexFile(), "\t")
        for line in contents.values():
            if line[0] is None or line[1] is None or line[2] is None or \
                    line[3] is None or line[4] is None:
                continue
            else:
                self.addWordToIndex(line[1], {"weight": float(line[3]),
                                              "assoc": line[4]})

    def process_word_list(self):
        contents = self.openFile(self.getWordListFile())
        for i, line in contents.iteritems():
            self.addWordToList(i, line.strip())

    def addWordToIndex(self, key, value):
        self.word_index[key] = value

    def getWordFromIndex(self, key):
        if key in self.word_index.keys():
            return self.word_index[key]
        else:
            return False

    def getWordAssociation(self, key):
        return self.word_index[key]["assoc"]

    def getWordWeight(self, key):
        for i in self.word_index.keys():
            return self.word_index[key]["weight"]

    def addWordToList(self, key, word):
        self.word_list[key] = word

    def getWordFromList(self, key):
        return self.word_list[key]

    def suggest(self, query):
        if self.spellCheckObj.inList(query.lower()) or query == "":
            print "found %s" % query
            return {self.spellCheckObj.get(query.lower()): 1}
        else:
            print "Not found %s" % query
            candidates = self.spellCheckObj.search(query)
            if len(candidates) > 0:
                return candidates
            else:
                candidates = self.ktuple_candidate_search(query)
                c_list = sorted(candidates.items(), key=lambda x: x[1],
                                reverse=True)
                return self.filter_results(query, c_list)

    def openFile(self, filename, delimiter=None):
        match_dict = {}
        with open(filename, "rU") as open_file:
            for i, line in enumerate(open_file):
                if delimiter is None:
                    match_dict[i] = line.strip("\n")
                else:
                    match_dict[i] = line.strip("\n").split(delimiter)
        return match_dict
