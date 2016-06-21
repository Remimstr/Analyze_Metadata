#!/usr/bin/env/python

# Created by: Remi Marchand
# Date: June 20, 2016
# Description: I don't know what this does yet

from __future__ import division
import Levenshtein

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SpellCheck:
    def __init__(self):
        self.dictionary = {}
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890.()[],+:- '
        self.delimeter = "\t"

    def setAlphabet(self, alpha):
        self.alphabet = alpha

    def getAlphabet(self):
        return self.alphabet

    def getDelimeter(self):
        return self.delimeter

    def setDelimiter(self, d):
        self.delimeter = d

    def build(self, f):
        d = self.getDelimeter()
        contents = self.openFile(f)
        for line in contents.values():
            for token in line.split(d):
                self.add(token)

    def add(self, word):
        self.dictionary[word.lower()] = str(word)

    def get(self, word):
        if word in self.dictionary.keys():
            return self.dictionary[word]
        else:
            return False

    def inList(self, word):
        #print "Word is %s, dict is %s" % (word, self.dictionary.keys())
        if word in self.dictionary.keys():
            return True
        else:
            return False

    def edits(self, word):
        alphabet = self.getAlphabet()
        mod_dict = {}
        pos = 0
        for i in self.deletes(word).values():
            mod_dict[pos] = i
            pos += 1
        for i in self.substitute(word).values():
            mod_dict[pos] = i
            pos += 1
        for i in self.insert(word, alphabet).values():
            mod_dict[pos] = i
            pos += 1
        for i in self.transpose(word).values():
            mod_dict[pos] = i
            pos += 1
        return mod_dict

    def deletes(self, word):
        length = len(word)
        edits = {}
        for i in range(length):
            newWord = ""
            for k in range(length):
                if i != k:
                    newWord += word[k]
            edits[i] = newWord
        return edits

    def substitute(self, word):
        alphabet = self.getAlphabet()
        word_len = len(word)
        alpha_len = len(alphabet)
        edits = {}
        counter = 0
        for i in range(word_len):
            for k in range(alpha_len):
                newWord = ""
                for j in range(word_len):
                    if i != j:
                        newWord += word[j]
                    else:
                        newWord += alphabet[k]
                edits[counter] = newWord
                counter += 1
        return edits

    def insert(self, word, alphabet):
        word_len = len(word)
        alpha_len = len(alphabet)
        edits = {}
        counter = 0
        for i in range(word_len):
            for k in range(alpha_len):
                newWord = ""
                for j in range(word_len):
                    if i == j:
                        newWord += alphabet[k]
                    newWord += word[j]
                edits[counter] = newWord
                counter += 1
        return edits

    def transpose(self, word):
        length = len(word)
        word_len = length - 1
        edits = {}
        for i in range(word_len):
            newWord = ""
            for k in range(length):
                if i == k:
                    newWord += word[k + 1] + word[k]
                elif k != (i + 1):
                    newWord += word[k]
            edits[i] = newWord
        return edits

    def search(self, word):
        original = word
        word = word.lower()
        candidates = {}
        if (self.inList(word)):
            candidates[self.get(word)] = 0
        else:
            edits = self.edits(word)
            for word in edits.values():
                if (self.inList(word) and word[0] == original[0].lower()):
                    word, original = self.get(word).lower(), original.lower()
                    candidates[self.get(word)] = Levenshtein.distance(word, original) / len(original) * 100
        return candidates

    def openFile(self, filename):
        match_dict = {}
        with open(filename, "rU") as open_file:
            for i, line in enumerate(open_file):
                match_dict[i] = line.strip("\n")
        return match_dict
