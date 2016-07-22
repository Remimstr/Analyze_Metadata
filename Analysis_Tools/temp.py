#!/usr/bin/env python

# The one you want to look at for testing is Salmonella_2011-03-12_2011-03-18.csv

import importlib

class SpecialDict():
    def __init__(self, modules):
        self.cols = []
        self.mods = []
        for mod in modules:
            for c in importlib.import_module(mod).column_strs:
                self.cols.append(c)
                self.mods.append(mod)
        if len(self.cols) != len(self.mods):
            raise Exception("Something bad happened")
        self.headers = [[] for _ in xrange(len(self.cols))]
        self.nums = [[] for _ in xrange(len(self.cols))]
    def find_positions(self, headers):
        for c in range(0, len(self.cols)):
            for h in headers:
                if self.cols[c] in h:
                    self.headers[c].append(h)
                    self.nums[c].append(parse_number(h))
    def parse_number(self):
        self.parsed_list = list(self.headers)
        for line in self.parsed_list:
            for i in line:
                i = [int(s) for s in i.split("_") if s.isdigit()]
    def fill_headers(self):
        # Extend the columns which are not the full length
        longest = max([len(i) for i in self.headers])
        for h in self.headers:
                for i in range(len(h), longest):
                    h.append(None)


    def selection_sort(self):
        while 1:
    """
#        self.longest_pos = self.pos.index(max([len(i) for i in self.pos]))
    def set_grid(self):
        self.grid = [[None for _ in xrange(self.longest)]
                     for _ in xrange(len(self.cols))]

columns = {}
for mod in modules:
    mod_cols = importlib.import_module(mod).column_strs
    for c in mod_cols:
        columns[c] = [mod]

"""
{'ORGANIZATION_name': ['organization_name'],
'collection_date': ['collection_date'],
'country': ['geographic_location'],
'geographic_location_(country_and/or_sea,region)': ['geographic_location'],
'isolation_source': ['isolation_source'],
'geographic_location': ['geographic_location'],
'serovar': ['serovar'],
'geo_loc_name': ['geographic_location']}
"""


for key in columns.keys():
    for h in headers:
        if key in h:
                columns[key].append(headers.index(h))


"""
{'ORGANIZATION_name': ['organization_name', 8],
'collection_date': ['collection_date', 34, 53, 72, 92, 111, 130, 149, 168, 187, 206, 225, 244, 276],
'country': ['geographic_location', 35, 54, 73, 93, 112, 131, 150, 169, 188, 207, 226, 245, 277],
'geographic_location_(country_and/or_sea,region)': ['geographic_location'],
'isolation_source': ['isolation_source', 38, 57, 76, 96, 115, 134, 153, 172, 191, 210, 229, 248, 278],
'geographic_location': ['geographic_location'],
'serovar': ['serovar', 40, 59, 79, 98, 117, 136, 155, 174, 193, 212, 231, 250, 280],
'geo_loc_name': ['geographic_location']}
"""

longest = max([len(columns[i]) for i in columns.keys()])
