#!/usr/bin/env python

# Author: Remi Marchand
# Date: May 18, 2016
# Description: This script parses metadata from an xml file into a
# dictionary which it returns to the user.

import os
from lxml import etree

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/Xml_Validation/"
sys.path.append(path)
from validate_xml import validate_xml

# Set fields to ignore while searching for "primary_IDs" and "grandparents"
exclude_list = ["EXPERIMENT_REF", "MEMBER", "Member", "DEFAULT_MEMBER"]

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


# accession_numbers: ElementTree SimpleDict -> None
# This function retrieves and parses all of the accession numbers
# (SRR, ERR, SRX, etc) from my_tree and adds them to metadata.


def accession_numbers(my_tree, metadata):
    # Find all of the PRIMARY_IDs and use their grandparent tags as keys
    ID_LIST = [x for x in my_tree.getiterator("PRIMARY_ID")]
    for ID in ID_LIST:
        parents = [x for x in ID.iterancestors()]
        grandparent = parents[1]
        if grandparent.tag not in exclude_list:
            metadata.add(parents[1].tag, ID.text)

# sample_attributes: Element SimpleDict Str -> None
# This function retrieves and parses all of the information under the
# sample_attributes (sa) node, accounting for the tree's unique structure.
# It adds all information found to metadata, using the string provided in
# the field "sample" to classify the information by sample name.


def sample_attributes(sa, metadata, sample):
    for child in sa:
        if len(child) == 2:
            if (child[0].tag == "TAG") and (child[1].tag == "VALUE"):
                if child[0].text is not None:
                    metadata.add(sample + child[0].text, child[1].text)
        else:
            metadata.add(sample + child.tag, child.text)

# parse_sa_st_data: Element SimpleDict Str -> None
# This function parses information found in the SAMPLE and STUDY nodes.
# It starts at the root node (SAMPLE/STUDY) and adds information found to
# metadata, usin the string provided in the field "sample" to classify the
# information by sample name.


def sample_study_nodes(root, metadata, sample):
    for child in root:
        if child.tag != "SAMPLE_ATTRIBUTES":
            for j in child.getiterator():
                # The attribute "namespace" is the key in certain situations
                if j.tag == "SUBMITTER_ID" or j.tag == "EXTERNAL_ID":
                    metadata.add(sample + j.attrib["namespace"], j.text)
                elif j.tag != "PRIMARY_ID":
                    metadata.add(sample + j.tag, j.text)
        else:
            sample_attributes(child, metadata, sample)

# sample_study_data: ElementTree SimpleDict -> None
# This function parses sample and study data from my_tree into
# metadata according to specific rules, using previously
# retrieved accession values as keys.


def sample_study_data(my_tree, metadata):
    # For each of the keys currently in metadata, retrieve corresponding data
    for acc in metadata.my_dict.keys():
        tag = acc.rstrip("1234567890_")
        accession = metadata.my_dict[acc][0]
        for i in my_tree.getiterator():
            sample = acc + "_"
            # Retrieve all of the fields that fit the criteria
            if (i.tag == tag == "SAMPLE" or i.tag == tag == "STUDY") \
                    and i.attrib["accession"] == accession:
                sample_study_nodes(i, metadata, sample)
            # Add the center_name information to metadata
            # if i.tag == "SAMPLE":
            #     print i.tag, acc, tag
            if i.tag == acc == "SAMPLE" and "center_name" in i.attrib:
                metadata.add(sample + "center_name", i.attrib["center_name"])

# add_other_metadata: ElementTree SimpleDict -> None
# This function adds metadata from my_tree with specific rules.
# Specifically, it deals with LIBRARY_LAYOUT, LIBRARY_DESCRIPTOR,
# and PLATFORM tags.


def add_other_metadata(my_tree, metadata):
    for i in my_tree.getiterator():
        if i.tag == "LIBRARY_LAYOUT" or i.tag == "PLATFORM":
            metadata.add(i.tag, i[0].tag)
        if i.tag == "LIBRARY_DESCRIPTOR" or i.tag == "PLATFORM":
            for field in i.getiterator():
                metadata.add(field.tag, field.text)

# parse_metadata: Xml -> Dict
# This function calls other functions that parse xml_file and adds the
# relevant information within to the dictionary that is returned to
# the caller.


def parse_metadata(xml_file):
    # Initialize a dictionary of header:value pairs
    metadata = SimpleDict()
    tree = etree.parse(xml_file)
    # Validate that the xml file is a valid XML, otherwise throw an error
    if not validate_xml(tree):
        raise ValueError("%s is an invalid XML file" % xml_file)
    # Add the accession numbers to metadata
    accession_numbers(tree, metadata)
    # Retrieve all metadata related to the sample accession numbers
    sample_study_data(tree, metadata)
    # Add library description metadata and platform metadata
    add_other_metadata(tree, metadata)
    for key in sorted(metadata.my_dict.iterkeys()):
        # Remove duplicates and join elements into one string
        metadata.my_dict[key] = ", ".join(list(set(metadata.my_dict[key])))
    return metadata.my_dict

# xml_file = sys.argv[1]
# parse_metadata(xml_file)
