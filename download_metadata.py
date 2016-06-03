#!/usr/bin/env python

# Author: Remi Marchand
# Date: May 13, 2016
# Description: This script downloads metadata from the SRA database
# based on organism name, and publication date limits. It outputs the
# results in an xml file.

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
# It splits the retrieved metadata into individual files and places
# them in a directory based on query. It provides this directory as
# the return value.


def download_metadata(query, delay):
    # Obtain list of IDs from query
    id_list = retrieve_accession_numbers(query)
    handle = Entrez.efetch(db=database, id=id_list)
    xml_list = []
    # Fetch the root (eps) and the sub_elements (xml_list)
    for event, element in ET.iterparse(handle):
        if element.tag == "EXPERIMENT_PACKAGE_SET":
            eps = element
        elif element.tag == "EXPERIMENT_PACKAGE":
            xml_list.append(element)
    for element, i in zip(xml_list, id_list):
        # Purge the root (eps) of all of its children
        for child in list(eps):
            eps.remove(child)
        # Insert the current element as a subelement of the empty root (eps)
        eps.insert(0, element)
        tree = ET.tostring(eps)
        filename = i + ".xml"
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, "w") as outFile:
            outFile.write(tree)
    handle.close()
    os.chdir("..")
    time.sleep(delay)
