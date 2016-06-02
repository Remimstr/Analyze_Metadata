#!/usr/bin/env python

# Author: Remi Marchand
# Date: May 13, 2016
# Description: This script downloads metadata from the SRA database
# based on organism name, and publication date limits. It outputs the
# results in an xml file.

import re
import os
import time
from Bio import Entrez
import xml.etree.ElementTree as ET

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# global variables
email = "thisisamail@email.com"
base_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&id="
database = "sra"

# retrieve_accession_numbers: Str -> (listof Str)
# This function retrieves accession numbers from the database of interest,
# (default=SRA). It takes in a search term and returns a list of
# accesion numbers


def retrieve_accession_numbers(query):
    Entrez.email = email
    handle = Entrez.esearch(db=database, term=query, retmax=99999)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

# download_metadata: Str Str Str -> Str
# This function takes a name, start, and end query and input
# and queries a database of interest (default=SRA) for metadata
# Returns a string consisting of the directory name


def download_metadata(query, delay):
    split_word = "<EXPERIMENT_PACKAGE>"
    # Obtain list of IDs from query
    id_list = retrieve_accession_numbers(query)
    data = Entrez.efetch(db=database, id=id_list)
    tree = ET.parse(data)
    root = tree.getroot()
    xml_string = ET.tostring(root)
    print "\nWriting XML Files"
    for x, i in zip(xml_string.split(split_word)[1:], id_list):
        x = re.sub(r"</*EXPERIMENT_PACKAGE(_SET)*>.*", "", x, flags=re.DOTALL)
        x = split_word + x + "</EXPERIMENT_PACKAGE>"
        filename = i + ".xml"
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, "w") as outFile:
            outFile.write(x)
    # Include a delay between queries so as not to aggravate the database
    time.sleep(delay)
    os.chdir("..")
