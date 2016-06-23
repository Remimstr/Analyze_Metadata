#!/usr/bin/env python

# Original Method: James Robertson as BuildSearchIndex.php
# Python Version: Remi Marchand - June 16, 2016
# Description: A short script to build a search index (default: sys.argv[2]
#              from a newline-delimited text file (default: sys.argv[4]).
#              The index is built out of k-mer chunks (default: sys.argv[1])
#              from the text file. Furthermore, each line from the text file
#              is re-formatted to a new text file (default: sys.argv[3])

from KmerTdf_Idf import KmerTdf_Idf

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

word_size = sys.argv[1]
filename = sys.argv[2]
out_name = sys.argv[3]
out_index_file = sys.argv[4]

lst = {}
out_file = open(out_name, "w")
with open(filename, "rU") as in_file:
    for i, line in enumerate(in_file):
        row = line.strip().split("|")
        count = len(row)
        if count == 0:
            row = line.strip().split("\t")
        for element in row:
            if element not in lst and element != "":
                out_file.write("%s\n" % element)
                lst[element] = ""
out_file.close()
k = KmerTdf_Idf()
k.init(out_name)
size = k.num_combinations
with open(out_index_file, "w") as out_index:
    for i in range(size):
        out_index.write("%s\t%s\t%s\t%s\t%s\n" % (i, k.getWord(i),
                        k.getFreq(i), k.getWeight(i), k.getAssoc(i)))
