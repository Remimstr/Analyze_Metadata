#!/usr/bin/env python

# Written by: Remi Marchand - June 23, 2016
# Description: Collection of classes to evaluate the performance of
#              different metadata tools.

import re
import copy
from random import *

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Class to make the kinds of data entry mistakes humans would make to compare
# them to the suggestions that the spell check would make.
class Eval_Spellcheck():
    def __init__(self, inFile, outFile):
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890.()[],+:-_ '
        self.choice_list = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 3]
        self.index_file = "../Resources/Standard_Serovars_Index.txt"
        self.standard_file = "../Resources/Standard_Serovars.txt"
        self.function_ref = {0: self.insert_square_brackets,
                             1: self.remove_square_brackets,
                             2: self.delete, 3: self.insert,
                             4: self.swap, 5: self.sub}
        seed(5)
        self.input_words = self.openFile(inFile)
        self.mutated_words = self.openFile(inFile)
        self.process_contents()
        self.writeWords(outFile)

    def process_contents(self):
        # For each line, randomly assign some changes to be made
        for pos in range(len(self.mutated_words)):
            print self.mutated_words[0]
            print pos
            # Choose the number of changes to be made
            c = choice(self.choice_list)
            ref = copy.copy(self.function_ref).keys()
            for change in range(c):
                # Choose a function to perform the change on
                if ref != []:
                    f = choice(ref)
                else:
                    break
                ref.remove(f)
                self.function_ref[f](pos)

    def insert_square_brackets(self, pos):
        word = self.getWord(pos)
        # Find all ints in the word
        positions = []
        for p in range(len(word)):
            try:
                int(word[p])
                positions.append(p)
            except ValueError:
                continue
        if positions == []:
            return None
        # Insert a random number of sets of square brackets around the ints
        changes = []
        for i in range(choice(self.choice_list)):
            # Choose a random position
            if positions == []:
                break
            else:
                p = choice(positions)
            positions.remove(p)
            # If one or more changes have already been performed, move indexes
            for c in changes:
                if p > c:
                    p += 2
            word = word[:p] + "[" + word[p] + "]" + word[p + 1:]
            changes.append(p)
        self.setWord(pos, word)

    def remove_square_brackets(self, pos):
        word = self.getWord(pos)
        # Finds all of the square bracket pairs in the word
        brackets = []
        for m in re.finditer(r"\[|\]", word):
            if m.group() == "[":
                brackets.append([m.start()])
            elif m.group() == "]" and [m.start() - 2] in [l for l in brackets]:
                for l in brackets:
                    if l == [(m.start() - 2)]:
                        l.append(m.start())
        brackets = filter(lambda x: len(x) == 2, brackets)
        # Remove a random number of square brackets
        changes = []
        for i in range(len(brackets)):
            # Choose a random set
            p = choice(brackets)
            avg = (p[0] + p[1]) / 2
            # If one or more changes have already been performed, move indexes
            for c in changes:
                # print "C: %s, avg: %s" % (c, avg)
                if avg > c:
                    for j in range(len(p)):
                        p[j] -= 2
                    avg -= 2
            word = word[:p[0]] + word[avg] + word[p[1] + 1:]
            changes.append(avg)
            brackets.remove(p)
        self.setWord(pos, word)

    def delete(self, pos):
        # Make a random number of deletions
        for deletion in range(choice(self.choice_list)):
            # Choose a random character to delete
            word = self.getWord(pos)
            char = choice(range(len(word)))
            word = word[:char] + word[char + 1:]
            self.setWord(pos, word)

    def insert(self, pos):
        # Make a random number of insertions
        for insertion in range(choice(self.choice_list)):
            # Choose a random character to add
            word = self.getWord(pos)
            character = self.alphabet[choice(range(len(self.alphabet)))]
            p = choice(range(len(word)))
            word = word[:p] + character + word[p:]
            self.setWord(pos, word)

    def sub(self, pos):
        # Make a random number of subs
        for sub in range(choice(self.choice_list)):
            # Choose a random character to sub in
            word = self.getWord(pos)
            character = self.alphabet[choice(range(len(self.alphabet)))]
            p = choice(range(len(word)))
            word = word[:p] + character + word[p + 1:]
            self.setWord(pos, word)

    def swap(self, pos):
        # Make a random number of swaps
        for swap in range(choice(self.choice_list)):
            # Choose two random characters to swap
            s = self.getWord(pos)
            char1, char2 = choice(range(len(s))), choice(range(len(s)))
            c1, c2 = min(char1, char2), max(char1, char2)
            if c1 == c2:
                break
            else:
                word = "".join((s[:c1], s[c2], s[c1 + 1:c2],
                                s[c1], s[c2 + 1:]))
            self.setWord(pos, word)

    def getWord(self, index):
        return self.mutated_words[index]

    def setWord(self, index, word):
        self.mutated_words[index] = word

    def writeWords(self, outFile):
        with open(outFile, "w") as open_file:
            for i, m in zip(self.input_words, self.mutated_words):
                open_file.write(str(i) + "\t" + str(m) + "\n")

    def openFile(self, inFile):
        lst = []
        with open(inFile, "rU") as open_file:
            for line in open_file:
                    lst.append(line.strip("\n"))
        return lst

inFile = sys.argv[1]
outFile = sys.argv[2]
x = Eval_Spellcheck(inFile, outFile)

# Retrieve all of the standard seronames from filename

"""
x = Eval_Spellcheck()
x.remove_square_brackets("4,[5],1[2]:d:-")
"""
