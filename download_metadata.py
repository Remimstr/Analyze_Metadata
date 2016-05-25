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
email = "thisisanemail@email.com"
base_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&id="
database = "sra"

# retrieve_accession_numbers: Str -> (listof Str)
# This function retrieves accession numbers from the database of interest (SRA)
# It takes in a search term and returns a list of accesion numbers


def retrieve_accession_numbers(query):
    Entrez.email = email
    handle = Entrez.esearch(db=database, term=query, retmax=99999)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

# generate_metadata: Str Str Str -> Str
# This function takes a name, start, and end query and input
# and queries a database of interest (default=SRA) for metadata
# Returns a string consisting of the directory name


def main(name, start, end, delay):
    directory = "%s_%s_%s" % (name, start, end)
    if not os.path.exists(directory):
        os.mkdir(directory)
    os.chdir(directory)
    start_date = start.replace("-", "/")
    end_date = end.replace("-", "/")
    # Build the query term
    query = "(%s[Organism]) AND (\"%s\"[Publication Date] : \"%s\"[Publication \
              Date])" % (name, start_date, end_date)
    # Obtain list of IDs from query
    id_list = retrieve_accession_numbers(query)
    for acc_number in id_list:
        address = base_url + acc_number
        data = urlopen(address)
        tree = ET.parse(data)
        filename = acc_number + ".xml"
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, "w") as outFile:
            print ("\nWriting %s" % filename)
            tree.write(outFile)
        time.sleep(delay)
    os.chdir("..")
    return directory