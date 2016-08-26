#!/usr/bin/env python

# Original Method: James Robertson as BuildSearchIndex.php
# Python Version: Remi Marchand - June 16, 2016
# Description: A short script to build a search index (-i, --index)
#              from a newline-delimited text file (-f, --file).
#              The index is built out of k-mer chunks (-s, --ksize).
#              from the text file. Furthermore, each line from the text file
#              is re-formatted to a new text file (-o, --outfile)

from KmerTdf_Idf import KmerTdf_Idf
from optparse import OptionParser

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def build_search_index(word_size, filename, out_name, out_index_file):
    lst = {}
    out_file = open(out_name, "w")
    with open(filename, "rU") as in_file:
        for i, line in enumerate(in_file):
            # Separate by "|" delimiter
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

if __name__ == "__main__":
    usage = "usage %prog options"
    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--ksize", help="size to split words when building the index file",
                      dest="ksize")
    parser.add_option("-f", "--file", help="path to the newline-delimited input text file",
                      dest="file")
    parser.add_option("-o", "--outfile", help="touched-up copy of the input text file (output)",
                      dest="outfile")
    parser.add_option("-i", "--index", help="index file built from the input text file",
                      dest="index")
    (options, args) = parser.parse_args()

    if options.ksize is None:
        parser.error("Please provide a kmer word size")
    if options.file is None:
        parser.error("Please provide an input text file from which to build the index")
    if options.outfile is None:
        parser.error("Please provide an outfile name")
    if options.index is None:
        parser.error("Please provide a name for the index file you want to build")
    build_search_index(options.ksize, options.file, options.outfile, options.index)