#!/usr/bin/env python

# Author: Remi Marchand
# Date: May 18, 2016
# Updated: July 25, 2016
# Description: This script parses metadata from an xml file into a
# dictionary which it returns to the user.

import os
from lxml import etree

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

path = os.path.abspath(os.path.dirname(sys.argv[0])) + "../Xml_Validation/"
sys.path.append(path)
from validate_xml import validate_xml

from experiment import experiment

# Class used to initialize and add dictionary items
class SimpleDict:
    # Initialize my_dict
    def __init__(self):
        self.my_dict = {}

    # Add an element to my_dict
    def add(self, key, value):
        if (value is None or value == "Missing" or value == "missing"):
            return None
        # Standardize the key by replacing spaces and dashes with underscores
        key = key.replace(" ", "_")
        key = key.replace("-", "_")
        # Set up naming conventions for each key
        if key not in self.my_dict:
            self.my_dict[key] = [value]
        else:
            iteration = 2
            next_key = key + "_" + str(iteration)
            while (next_key in self.my_dict):
                next_key = key + "_" + str(iteration)
                iteration += 1
            self.my_dict[next_key] = [value]


# parse_metadata: Xml -> Dict
# This function calls other functions that parse an xml_file and adds the
# relevant information within to the dictionary that is returned to
# the caller.


def parse_metadata(xml_file):
    # Initialize a dictionary of header:value pairs
    metadata = SimpleDict()
    tree = etree.parse(xml_file)
    # Validate that the xml file is a valid XML, otherwise throw an error
    if not validate_xml(tree):
        raise ValueError("%s is an invalid XML file" % xml_file)
    root = tree.getroot()
    for child in root:
        if child.tag == "EXPERIMENT":
            experiment(child, metadata)
    # expt_package = tree.getroot()
    for key in sorted(metadata.my_dict.iterkeys()):
        # Remove duplicates and join elements into one string
        metadata.my_dict[key] = ", ".join(list(set(metadata.my_dict[key])))
    return metadata.my_dict

# xml_file = sys.argv[1]
# parse_metadata(xml_file)
