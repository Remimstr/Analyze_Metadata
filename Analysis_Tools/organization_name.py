#!/usr/bin/env python

# Author: Remi Marchand
# Date: July 20, 2016
# Description: A wrapper to parse organization_name information

import multilevel_parse

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

keys = multilevel_parse.keys
# column_strs is a list of strings representing columns of interest
column_strs = ["organization_name"]


def parse(organization_name, org_name_info):
    return multilevel_parse.parse(organization_name, org_name_info)
