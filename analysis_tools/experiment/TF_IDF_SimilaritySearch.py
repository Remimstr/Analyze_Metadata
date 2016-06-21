#!/usr/bin/env python

# Original Method: James Robertson as BuildSearchIndex.php
# Python Version: Remi Marchand - June 16, 2016
# Descriptions: I don't know what this does yet

import re
import math
import Levenshtein

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class TF_IDF_SimilaritySearch:
    def __init__(self, filename):
        self.entity_lookup = {}
        self.entity_array = {}
        self.numberOfInst = 0
        self.word_search_array = {}
        self.set_entity_list(filename)
        self.word_search_array["WordFrequency"] = {}
        self.word_search_array["WordInstitutions"] = {}
        self.word_search_array["WordWeight"] = {}
        self.init_search_list()
        self.calc_word_weights()

    def inList(self, inst):
        if inst in self.entity_lookup.keys():
            return True
        else:
            return False

    def set_entity_list(self, filename):
        self.entity_array = self.openFile(filename).split
        self.numberOfInst = len(self.entity_array)
        for inst in self.entity_array:
            self.entity_lookup[inst.strip()] = ""

    def get_entity_by_line_number(self, num):
        if num in self.entity_array:
            return self.entity_array[num]
        else:
            return False

    def get_inst_count(self):
        return self.numberOfInst

    def get_word_freq(self, word):
        if word in self.word_search_array["WordFrequency"]:
            return self.word_search_array["WordFrequency"][word]
        else:
            return 0

    def set_word_freq(self, word, count):
        self.word_search_array["WordFrequency"][word] = count

    def get_word_entity_association(self, word):
        if word in self.word_search_array["WordInstitutions"]:
            return self.word_search_array["WordInstitutions"][word]
        else:
            return ""

    def set_word_entity_association(self, word, lst):
        self.word_search_array["WordInstitutions"][word] = lst

    def init_search_list(self):
        element_count = self.get_inst_count()
        for i in range(len(element_count)):
            inst = re.sub(r"/\,|\n|\n\r/", "", self.get_entity_by_line_number(i))
            if len(inst) == 0:
                continue
            tok = inst.lower().split(" ")
            for t in tok:
                if len(t) == 0:
                    continue
                t = t.lower()
                frequency = self.get_word_freq(t)
                frequency = frequency + 1
                self.set_word_freq(t, frequency)
                lst = i + "," + self.get_word_entity_association(t)
                self.set_word_entity_association(t, lst)

    def cal_word_weights(self):
        numDocs = self.get_inst_count()
        for word, insts in self.word_search_array["WordInstitutions"].iteritems():
            numInstWithWord = len(insts.split())
            idf = math.log10((numDocs / numInstWithWord))
            self.word_search_array["WordWeight"][word] = idf

    def get_word_weight(self, word):
        if word in self.word_search_array["WordWeight"].keys():
            return self.word_search_array["WordWeight"][word]
        else:
            return 0

    def search(self, entity):
        entity = re.sub(r"/\,|\n|\n\r", "", entity)
        tok = entity.split(" ")
        inst_list = {}
        for t in tok:
            if len(t) == 0:
                continue
            t = t.lower()
            lst = self.get_word_entity_association(t).split(",")
            for i in lst:
                if i in inst_list.keys():
                    inst_list[i] = inst_list[i] + self.get_word_weight(t)
                else:
                    inst_list[i] = self.get_word_weight(t)
        return inst_list

    def getBestMatches(self, inst_list, num_match_to_return):
        i = 0
        top_matches = {}
        for inst in sorted(inst_list.keys(), reverse=True):
            score = inst_list[inst]
            if len(self.get_entity_by_line_number(inst)) < 3:
                continue
                i += 1
                top_matches[self.get_entity_by_line_number(inst)] = score
                if (i == num_match_to_return):
                    break
        return top_matches

    def normalize_matches(self, query_string, match_array):
        for match, score in match_array.iteritems():
            distance = Levenshtein.distance(query_string, match)
            score = score / (1 + distance)
            match_array[match] = score
        match_array = sorted(match_array.keys(), reverse=True)
        return match_array

    def openFile(self, filename):
        match_dict = {}
        with open(filename, "rU") as open_file:
            for i, line in enumerate(open_file):
                match_dict[i] = line.strip("\n")
        return match_dict
