#!/usr/bin/env python

# Original Method: James Robertson as kmer_similarity.php
# Python Version: Remi Marchand - June 16, 2016
# Description: Class to manipulate k-mer data relating to the alphabet
#              provided. Instead of storing the kmers, it allows the user to
#              access their data using their position.

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Kmer_Similarity:
    def __init__(self):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz1234567890.()[],+:-_' "
        self.size = 3
        self.counts = {}
        self.num_combinations = 0
        self.calcArraySize()
        self.initCounts()

    # Retrieves and returns the word found at position pos
    def getWord(self, pos):
        length = len(self.getAlphabet())
        alphabet = self.getAlphabet()
        size = self.size
        word = ""
        for i in range(size):
            r = pos % length
            word += (alphabet[r])
            pos = int(pos / length)
        return word[::-1]

    # Retrieves and returns the position of word
    def calc_position(self, word):
        length = len(word)
        pos = {}
        alphabet = self.getAlphabet()
        alphaSize = len(alphabet)
        size = self.size - 1
        pos = []
        for i in range(length):
            char = word[i]
            pos.append(alphabet.find(char))
        value = pos[0] * (alphaSize ** size)
        count = len(pos)
        for i in range(1, count):
            size = size - 1
            value = value + (pos[i] * (alphaSize ** size))
        return value

    # Calculates the size of the array to be created, taking into account
    # the size of the alphabet and the size of the individual kmers
    def calcArraySize(self):
        self.num_combinations = len(self.getAlphabet()) ** self.getSize()

    # Initialize the values of the entire array to 0
    def initCounts(self):
        for i in range(self.num_combinations):
            self.counts[i] = 0

    def setAlphabet(self, alpha):
        self.alphabet = alpha

    def getAlphabet(self):
        return self.alphabet

    def getSize(self):
        return self.size

    def setSize(self, s):
        self.size = s
