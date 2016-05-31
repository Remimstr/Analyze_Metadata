#!/usr/bin/env python

# Author: Remi Marchand
# Date: May 13, 2016
# Description: This script downloads metadata from the SRA database
# based on organism name, and publication date limits. It outputs the
# results in an xml file.

from urllib import urlopen
from Bio import Entrez
import time
import os
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
    # Obtain list of IDs from query
    id_list = retrieve_accession_numbers(query)
    for acc_number in id_list:
        # For each query, construct a url and download data from it
        address = base_url + acc_number
        data = urlopen(address)
        # Open the data in xml format and write it to the outfile
        tree = ET.parse(data)
        filename = acc_number + ".xml"
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, "w") as outFile:
            print ("\nWriting %s" % filename)
            tree.write(outFile)
        # Include a delay between queries so as not to aggravate the database
        time.sleep(delay)
    os.chdir("..")
