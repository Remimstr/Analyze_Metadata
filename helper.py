#!/usr/bin/env python

# Author: Remi Marchand
# Date: May 19, 2016
# Description: A collection of scripts to help analyze ElementTrees

from lxml import etree
import os
from optparse import OptionParser

def print_path(item, xml_file):
    tree = etree.parse(xml_file)
    root = tree.getroot()
    for child in root.iter():
        tags = []
        if (child.text is not None) and (item in child.text):
            tags.append(child.text)
            while (1):
                try:
                    tags.append(child.tag)
                    child = child.getparent()
                except:
                    break
            tags.reverse()
            print " > ".join(tags)

if __name__ == "__main__":
    os.chdir(os.getcwd())
    # Process the command line input using optparse
    usage = "usage: %prog options"
    parser = OptionParser(usage=usage)
    parser.add_option("-t", "--tool", help="tool to use", dest="tool")
    parser.add_option("--xml", help=".xml file to use",
                      dest="xml_file")
    parser.add_option("-e", "--element", help="element to use as input",
                      dest="element")
    (options, args) = parser.parse_args()

    # Raise optparse errors as necessary
    if (options.tool == "print_path") or (options.tool == "pp"):
        print_path(options.element, options.xml_file)
