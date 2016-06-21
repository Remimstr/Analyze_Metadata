#!/usr/bin/env python

# Created by: Remi Marchand
# Date: June 14, 2016
# Description: I don't know what this does yet

import re
import math

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class KWord_Search:
    def __init__(self, word_array):
        self.word_lookup = {}
        self.word_array = {}
        self.numberoflines = 0
        self.word_search_array = {}
        self.set_word_list(word_array)
        self.word_search_array["WordFrequency"] = {}
        self.word_search_array["WordInstitutions"] = {}
        self.word_search_array["WordWeight"] = {}
        self.init_search_list()
        self.calc_word_weights()

    def inList(self, inst):
        if inst in self.word_lookup.keys():
            return True
        else:
            return False

    def set_word_list(self, array):
        self.word_array = array
        self.numberoflines = len(self.word_array)
        for inst in self.word_array:
            self.word_lookup[inst.strip()] = ""

    def get_word_by_line_number(self, num):
        if num in self.word_array.keys():
            return self.word_array[num]
        else:
            return False

    def get_line_count(self):
        return self.numberoflines

    def get_word_freq(self, word):
        if word in self.word_search_array["Word_Frequency"].keys():
            return self.word_search_array["Word_Frequency"][word]
        else:
            return 0

    def set_word_freq(self, word, count):
        self.word_search_array["Word_Frequency"][word] = count

    def get_word_association(self, word):
        if word in self.word_search_array["WordInstitutions"].keys():
            return self.word_search_array["WordInstitutions"][word]
        else:
            return ""

    def set_word_association(self, word, lst):
        self.word_search_array["WordInstitutions"][word] = lst

    def init_search_list(self):
        element_count = self.get_line_count()
        for i in range(len(element_count)):
            inst = re.sub(r"/\,|\n|\n\r/", "", self.get_word_by_line_number(i))
            if len(inst) == 0:
                continue
            tok = inst.split(" ")
            for t in tok:
                if len(t) == 0:
                    continue
                t = t.lower()
                frequency = self.get_word_freq(t)
                frequency += 1
                self.set_word_freq(t, frequency)
                lst = i + "," + self.get_word_association(t)
                self.set_word_association(t, lst)

    def calc_word_weights(self):
        numDocs = self.get_line_count()
        for word, insts in self.word_search_array["WordInstitutions"]:
            numInstWithWord = len(insts.split(","))
            idf = math.log((numDocs / numInstWithWord), 10)
            self.word_search_array["WordWeight"][word] = idf

    def search(self, institution):
        institution = re.sub(r"/\,|\n|\nr/", institution)
        tok = institution.split(" ")
        inst_list = {}
        for t in tok:
            if len(t) == 0:
                continue
            t = t.lower()
            lst = self.get_word_association(t).split(",")
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
            if len(self.get_word_by_line_number(inst)) < 3:
                continue
            i += 1
            top_matches[self.get_word_by_line_number(inst)] = score
            if i == num_match_to_return:
                break
        return top_matches
