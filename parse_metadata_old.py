# Author: Remi Marchand
# Date: May 18, 2016
# Description: This script parses metadata from an xml file into a
# dictionary which it returns to the user.

import xml.etree.ElementTree as ET

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Class to initialize the dictionary and functions


class SimpleDict:
    # Initialize my_dict
    def __init__(self):
        self.my_dict = {}

    # Add an element to my_dict
    def add(self, key, value):
        # Standardize the key by replacing spaces and dashes with underscores
        key = key.replace(" ", "_")
        key = key.replace("-", "_")
        if key not in self.my_dict:
            self.my_dict[key] = [value]
        else:
            self.my_dict[key].append(value)

# add_generic: Element Dict
# Adds a generic element (element) to the dictionary metadata


def add_generic(element, metadata, additional=""):
    if element_pass(element.text):
        metadata.add(additional + element.tag, element.text)

# element_pass: Element -> Bool
# Returns true if an element passes specified criteria


def element_pass(element):
    if element is not None and element != "Missing" and element != "missing":
        return True

# identifiers, sample_links, sample_attributes: ET Dict
# Each function parses the identifiers section of the Element Tree
# with the root starting at each respective location. It adds all information
# found to the metadata dictionary.


def identifiers(iden, metadata, additional):
    for child in iden:
        if (child.tag == "EXTERNAL_ID") and ("namespace" in child.attrib):
            metadata.add(additional + child.attrib["namespace"], child.text)
        if (child.tag == "SUBMITTER_ID") and ("namespace" in child.attrib) \
                and ("label" in child.attrib):
            metadata.add(additional + "Submitter_ID", child.attrib["namespace"])
            metadata.add(additional + child.attrib["label"], child.text)
        else:
            add_generic(child, metadata, additional)  # Use generic parsing


def sample_links(sl, metadata, additional):
    for pos in range(0, len(sl)):
        for child in sl[pos].iter():
            if child.text is not None:
                metadata.add((additional + child.tag + "_%s" % str(pos + 1)),
                             child.text)


def sample_attributes(sa, metadata, additional):
    for child in sa:
        if (child[0].tag == "TAG") and (child[1].tag == "VALUE"):
            if (element_pass(child[0].text) and element_pass(child[1].text)):
                metadata.add(additional + child[0].text, child[1].text)
        else:
            add_generic(child, metadata, additional)

# main: Str -> Dict
# takes in a path to an xml file and parses it according to certain criteria.
# It adds all infomation found to the output dictionary, metadata


def main(xml_file):
    # Initialize a dictionary of header:value pairs
    metadata = SimpleDict()
    # Set variables for each category
    tree = ET.parse(xml_file)
    root = tree.getroot()
    sample, experiment, submission, study, primary_id = [], [], [], [], []
    for child in root.iter():
        if child.tag == "SAMPLE":
            sample.append(child)
        if child.tag == "EXPERIMENT":
            experiment.append(child)
        if child.tag == "SUBMISSION":
            submission.append(child)
        if child.tag == "PRIMARY_ID":
            primary_id.append(child)
            add_generic(child, metadata)
        if child.tag == "STUDY":
            study.append(child)

    # Add all primary ids to the metadata
    for item in primary_id:
        add_generic(item, metadata)

    for item in experiment:
        for field in item.iter():
            if field.tag == "LIBRARY_LAYOUT" or field.tag == "PLATFORM":
                metadata.add(field.tag, field[0].tag)
            add_generic(field, metadata)

    for item in sample:
        for field in item:
            # Parse the identifier fields of sample
            if field.tag == "IDENTIFIERS":
                identifiers(field, metadata, "SAMPLE_")
            # Add the title of sample
            if field.tag == "TITLE":
                add_generic(field, metadata, "SAMPLE_")
            # Add the sample name fields of sample
            if field.tag == "SAMPLE_NAME":
                for child in field.iter():
                    if child.text is not None:
                        add_generic(child, metadata)
            # Add the sample links of sample
            if field.tag == "SAMPLE_LINKS":
                sample_links(field, metadata, "SAMPLE_")
            # Add the sample attributes of sample
            if field.tag == "SAMPLE_ATTRIBUTES":
                sample_attributes(field, metadata, "SAMPLE_")

    for item in study:
        for field in item:
            # Parse the identifier fields of study
            if field.tag == "IDENTIFIERS":
                identifiers(field, metadata, "STUDY_")
            # Add the study descriptor fields
            if field.tag == "DESCRIPTOR":
                for child in field.iter():
                    if child.text is not None:
                        add_generic(child, metadata)
            # Add the attributes of study
            if field.tag == "SAMPLE_ATTRIBUTES":
                sample_attributes(field, metadata, "STUDY_")

    # Sort the metadata dictionary
    for key in sorted(metadata.my_dict.iterkeys()):
        # Remove duplicates and join elements into one string
        metadata.my_dict[key] = ", ".join(list(set(metadata.my_dict[key])))
    return metadata.my_dict
