#!/usr/bin/env python

# Author: Remi Marchand
# Date: May 18, 2016
# Major Revision: July 25-29, 2016
# Description: This script parses metadata from an xml file into a
# dictionary which it returns to the user.

from lxml import etree

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from Xml_Validation import validate_xml

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


def parse_generic(term, metadata, prefixes):
    parse_string = ""
    # Parse generic with prefixes
    for p in prefixes:
        parse_string += p + "/"
    metadata.add(parse_string + term.tag, term.text)

# *************************************************************************** #


def experiment(experiment, metadata):
    key = ""
    for child in experiment:
        # Parse EXPERIMENT -> IDENTIFIERS ->
        if child.tag == "IDENTIFIERS":
            for grandchild in child:
                if grandchild.tag == "PRIMARY_ID":
                    key = grandchild.text
                    parse_generic(grandchild, metadata, [key, "EXPERIMENT_REF"])
        # Parse EXPERIMENT -> STUDY_REF -> IDENTIFIERS ->
        if child.tag == "STUDY_REF":
            for grandchild in child:
                if grandchild.tag == "IDENTIFIERS":
                    for greatgrandchild in grandchild:
                        parse_generic(greatgrandchild, metadata, [key, "STUDY"])
        # Parse EXPERIMENT -> DESIGN -> LIBRARY_DESCRIPTOR ->
        if child.tag == "DESIGN":
            for grandchild in child:
                if grandchild.tag == "LIBRARY_DESCRIPTOR":
                    library_descriptor(grandchild, metadata, key)
        # Parse EXPERIMENT -> PLATFORM
        if child.tag == "PLATFORM":
            platform(child, metadata, key)
    return key


def library_descriptor(library_descriptor, metadata, key):
    # Parse LIBRARY_NAME, LIBRARY_STRATEGY, LIBRARY_SOURCE,
    #       LIBRARY_SELECTION, LIBRARY_CONSTRUCTION_PROTOCOL
    for child in library_descriptor:
        if child.tag == "LIBRARY_LAYOUT":
            metadata.add(key + "/" + child.tag, child[0].tag)
        else:
            parse_generic(child, metadata, [key])


def platform(platform, metadata, key):
    # Parse PLATFORM, -> -> INSTRUMENT_MODEL
    metadata.add(key + "/" + platform.tag, platform[0].tag)
    for field in platform.getiterator():
        if field.tag == "INSTRUMENT_MODEL":
            parse_generic(field, metadata, [key])


# *************************************************************************** #


def submission(submission, metadata):
    key = ""
    for child in submission:
        # Parse SUBMISSION -> IDENTIFIERS
        if child.tag == "IDENTIFIERS":
            for grandchild in child:
                if grandchild.tag == "PRIMARY_ID":
                    key = grandchild.text
                    parse_generic(grandchild, metadata, [key, "SUBMISSION"])
    return key


# *************************************************************************** #

def organization(organization, metadata, key):
    for child in organization:
        # Parse Organization -> Name
        if child.tag == "Name":
            parse_generic(child, metadata, [key, "Organization_Name"])

# *************************************************************************** #


def study(study, metadata):
    key = ""
    for child in study:
        # Parse STUDY -> IDENTIFIERS
        if child.tag == "IDENTIFIERS":
            for grandchild in child:
                if grandchild.tag == "PRIMARY_ID":
                    key = grandchild.text
                    parse_generic(grandchild, metadata, [key, "PROJECT"])
        # Parse STUDY -> DESCRIPTOR -> STUDY_TITLE
        if child.tag == "DESCRIPTOR":
            for grandchild in child:
                if grandchild.tag == "STUDY_TITLE":
                    parse_generic(grandchild, metadata, [key, "STUDY"])
    return key


# *************************************************************************** #


def sample(sample, metadata):
    key = ""
    for child in sample:
        # Parse SAMPLE -> IDENTIFIERS and SAMPLE -> SAMPLE_NAME
        if child.tag == "IDENTIFIERS" or "SAMPLE_NAME":
            for grandchild in child:
                if grandchild.tag == "PRIMARY_ID":
                    key = grandchild.text
                    parse_generic(grandchild, metadata, [key, "SAMPLE"])
        # Parse SAMPLE -> SAMPLE_ATTRIBUTES
        if child.tag == "SAMPLE_ATTRIBUTES":
            sample_attributes(child, metadata, key)
    return key


def sample_attributes(sample_attributes, metadata, key):
    for child in sample_attributes:
        # Parse SAMPLE_ATTRIBUTES -> TAG/VALUE pairs
        if (len(child) == 2) and (child[0].tag == "TAG") and \
                (child[1].tag == "VALUE"):
            metadata.add(key + "/" + child[0].text, child[1].text)


# *************************************************************************** #


def run(run, metadata):
    key = ""
    for child in run:
        # Parse RUN -> IDENTIFIERS
        if child.tag == "IDENTIFIERS":
            for grandchild in child:
                if grandchild.tag == "PRIMARY_ID":
                    key = grandchild.text
                    parse_generic(grandchild, metadata, [key, "RUN"])
        for i in child.getiterator():
            if i.tag == "EXPERIMENT_REF" or i.tag == "Member":
                for grandchild in i:
                    for greatgrandchild in grandchild:
                        if greatgrandchild.tag == "PRIMARY_ID":
                            tag = "SAMPLE" if i.tag == "Member" else i.tag
                            parse_generic(greatgrandchild, metadata,
                                          [key, tag])
    return key

# *************************************************************************** #


def throw_errors(expt_key, sub_key, sample_keys, run_keys, xml_file):
    if expt_key == "":
        raise Exception("No experiments were found in this xml: %s" % xml_file)
    if sub_key == "":
        raise Exception("No submissions were found in this xml: %s" % xml_file)
    if sample_keys == []:
        raise Exception("No samples were found in this xml: %s" % xml_file)
    if run_keys == []:
        print "No runs were found in this xml: %s" % xml_file


# parse_metadata: Xml -> Dict
# This function calls other functions that parse an xml_file and adds the
# relevant information within to the dictionary that is returned to
# the caller.


def parse_metadata(xml_file):
    # Initialize a dictionary of header:value pairs
    metadata = SimpleDict()
    tree = etree.parse(xml_file)
    # Validate that the xml file is a valid XML, otherwise throw an error
    if not validate_xml.validate_xml(tree):
        raise ValueError("%s is an invalid XML file" % xml_file)
    try:
        root = tree.find("EXPERIMENT_PACKAGE")
    except:
        raise Exception("Could not find Experiment Package of %s" % xml_file)
    experiment_key = ""
    submission_key = ""
    study_key = ""
    sample_keys = []
    run_keys = []
    for child in root:
        # Parse EXPERIMENT ->
        if child.tag == "EXPERIMENT":
            experiment_key = experiment(child, metadata)
        # Parse SUBMISSION ->
        if child.tag == "SUBMISSION":
            submission_key = submission(child, metadata)
        # Parse Organization ->
        if child.tag == "Organization":
            organization(child, metadata, experiment_key)
        # Parse STUDY ->
        if child.tag == "STUDY":
            study_key = study(child, metadata)
        # Parse SAMPLE ->
        if child.tag == "SAMPLE":
            sample_keys.append(sample(child, metadata))
        # Parse RUN_SET ->
        if child.tag == "RUN_SET":
            for grandchild in child:
                run_keys.append(run(grandchild, metadata))
    throw_errors(experiment_key, submission_key,
                 sample_keys, run_keys, xml_file)
    # expt_package = tree.getroot()
    for key in sorted(metadata.my_dict.iterkeys()):
        # Remove duplicates and join elements into one string
        metadata.my_dict[key] = ", ".join(list(set(metadata.my_dict[key])))
    ret_vals = {"expt_key": experiment_key, "sub_key": submission_key,
                "sample_keys": sample_keys, "run_keys": run_keys,
                "study_key": study_key, "metadata": metadata.my_dict}
    return ret_vals

# xml_file = sys.argv[1]
# parse_metadata(xml_file)
