#!/usr/bin/env python

# Author: Remi Marchand
# Date: July 13, 2016
# Description: This script validates an SRA xml file to tell
# the caller whether the file will parse without error.

import os
from lxml import etree

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Get the relative path for the xsd files
path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/Xml_Validation/"

paths = {"EXPERIMENT": path + "SRA.experiment.xsd",
         "SUBMISSION": path + "SRA.submission.xsd",
         "STUDY": path + "SRA.study.xsd",
         "SAMPLE": path + "SRA.sample.xsd"}

# build_schema: Str -> XmlSchema
# This function builds an xml schema used to validate whole xml files
# of parts of an xml file. It uses filename as the basis for this
# schema.


def build_schema(filename):
    xmlschema_doc = etree.parse(filename)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    return xmlschema

# validate_xml: Str -> Bool
# This function validates as many parts of the input SRA xml as it can
# using the SRA xml formatting guidelines specified by the files in path
# (of the format "SRA.*.xsd"). Returns true if the xml file is found to
# be valid, and false otherwise.


def validate_xml(xml_file):
    valid = True
    root = xml_file.getroot()
    for child in root[0]:
        if child.tag in paths.keys():
            schema = build_schema(paths[child.tag])
            valid = schema.validate(child) and valid
            schema.assertValid(child)
    return valid
