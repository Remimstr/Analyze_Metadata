#!/usr/bin/env python

# Author: Remi Marchand
# Date: July 27, 2016
# Description: This script parses the experiment section of an xml

import os
import lxml import etree

# Set default string process to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from parse_metadata import *


def identifiers(identifiers, metadata, prefix):
    for child in identifiers:
        metadata.add(prefix + "_" + child.tag, child.text)


# experiment: Xml element -> None
def experiment(experiment, metadata):
    # Parse EXPERIMENT -> IDENTIFIERS -> PRIMARY_ID as EXPERIMENT_ID
    for child in experiment:
        if child.tag == "IDENTIFIERS":
            identifiers(child, metadata, "EXPERIMENT")
