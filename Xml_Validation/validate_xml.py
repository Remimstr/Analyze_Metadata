#!/usr/bin/env python

# Author: Remi Marchand
# Date: July 13, 2016
# Description: This script validates an SRA xml file
# to tell the caller whether the file will parse without error.

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


def build_schema(filename):
    xmlschema_doc = etree.parse(filename)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    return xmlschema

# Try and validate as much of the xml file as possible


def validate_xml(xml_file):
    valid_list = []
    valid = True
    root = xml_file.getroot()
    for child in root[0]:
        if child.tag in paths.keys():
            schema = build_schema(paths[child.tag])
            valid = schema.validate(child) and valid
            valid_list.append([child.tag, build_schema(paths[child.tag]).validate(child)])
            schema.assertValid(child)
    return valid
