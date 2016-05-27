from lxml import etree

# from pprint import pprint
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

exclude_list = ["EXPERIMENT_REF", "MEMBER", "Member", "DEFAULT_MEMBER"]

class SimpleDict:
    # Initialize my_dict
    def __init__(self):
        self.my_dict = {}

    # Add an element to my_dict
    def add(self, key, value):
        # Standardize the key by replacing spaces and dashes with underscores
        key = key.replace(" ", "_")
        key = key.replace("-", "_")
        # Some complicated junk for naming conventions
        if key not in self.my_dict:
            self.my_dict[key] = [value]
        else:
            iteration = 2
            next_key = key + "_" + str(iteration)
            while (next_key in self.my_dict):
                next_key = key + "_" + str(iteration)
                iteration += 1
            self.my_dict[next_key] = [value]


def add_generic(element, metadata, additional=""):
    if element_pass(element.text):
        metadata.add(additional + element.tag, element.text)


def element_pass(element):
    if element is not None and element != "Missing" and element != "missing":
        return True


def accession_numbers(my_tree, metadata):
    # Find all of the PRIMARY_ID's and use their grandparent tags as keys
    ID_LIST = [x for x in my_tree.getiterator("PRIMARY_ID")]
    for ID in ID_LIST:
        parents = [x for x in ID.iterancestors()]
        grandparent = parents[1]
        if grandparent.tag not in exclude_list:
            metadata.add(parents[1].tag, ID.text)


def sample_attributes(sa, metadata, additional):
    for child in sa:
        if (child[0].tag == "TAG") and (child[1].tag == "VALUE"):
            if (element_pass(child[0].text) and element_pass(child[1].text)):
                metadata.add(additional + child[0].text, child[1].text)
        else:
            add_generic(child, metadata, additional)


def parse_data(root, title, metadata):
    for i in root:
        if i.tag != "SAMPLE_ATTRIBUTES":
            for j in i.getiterator():
                # Use namespace if SUBMITTER_ID tag
                if j.tag == "SUBMITTER_ID" or j.tag == "EXTERNAL_ID":
                    metadata.add(title + j.attrib["namespace"], j.text)
                elif j.tag != "PRIMARY_ID":
                    add_generic(j, metadata, title)
        else:
            root = i
            sample_attributes(root, metadata, title)


def sample_study_data(my_tree, metadata):
    for acc in metadata.my_dict.keys():
        tag = acc.rstrip("1234567890_")
        accession = metadata.my_dict[acc][0]
        for i in my_tree.getiterator():
            if (i.tag == tag == "SAMPLE" or i.tag == tag == "STUDY") \
                    and i.attrib["accession"] == accession:
                root = i
                acc += "_"
                parse_data(root, acc, metadata)
            if i.tag == tag == "SAMPLE" and "center_name" in i.attrib:
                metadata.add("center_name", i.attrib["center_name"])


def add_other_metadata(my_tree, metadata):
    for i in my_tree.getiterator():
        if i.tag == "LIBRARY_LAYOUT" or i.tag == "PLATFORM":
            metadata.add(i.tag, i[0].tag)
        if i.tag == "LIBRARY_DESCRIPTOR" or i.tag == "PLATFORM":
            for field in i.getiterator():
                add_generic(field, metadata)


def main(xml_file):
    # Initialize a dictionary of header:value pairs
    metadata = SimpleDict()
    tree = etree.parse(xml_file)
    # Add the accession numbers to metadata
    accession_numbers(tree, metadata)
    # Retrieve all metadata related to the sample accession numbers
    sample_study_data(tree, metadata)
    # Add library description metadata and platform metadata
    add_other_metadata(tree, metadata)

    # Clean up and print the dict
    for key in sorted(metadata.my_dict.iterkeys()):
        # Remove duplicates and join elements into one string
        metadata.my_dict[key] = ", ".join(list(set(metadata.my_dict[key])))
    # print(metadata.my_dict)
    return metadata.my_dict

# xml_file = sys.argv[1]
# main(xml_file)
