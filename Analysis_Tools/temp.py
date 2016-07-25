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

    def run(self, headers):
        self.headers = [[] for _ in xrange(len(self.cols))]
        self.find_positions(headers)
        self.deep_selection_sort()
        self.fill_list()
        self.print_headers()

    def find_positions(self, headers):
        for c in range(0, len(self.cols)):
            for h in headers:
                if self.cols[c] in h:
                    self.headers[c].append({h: self.parse_number(h)})

    def parse_number(self, number):
        num = [int(s) for s in number.split("_") if s.isdigit()]
        if len(num) > 1:
            raise Exception("Multiple Header Numbers Were Found")
        elif len(num) == 0:
            return num
        else:
            return num[0]

    def fill_list(self):
        # Extend the columns which are not the full length
        longest = max([len(i) for i in self.headers])
        for h in self.headers:
                for i in range(len(h), longest):
                    h.append(None)

    def deep_selection_sort(self):
        f_list = self.headers[0]
        for p1 in range(0, len(f_list)):
            for sublist in self.headers[1:]:
                for p2 in range(0, len(sublist)):
                    if f_list[p1].values() == sublist[p2].values():
                        temp = sublist[p2]
                        sublist[p2] = sublist[p1]
                        sublist[p1] = temp

    def print_headers(self):
        ret_vals = []
        for i in range(0, len(self.headers[0])):
            line_set = []
            for l in self.headers:
                if l[i] is None:
                    line_set.append(None)
                else:
                    line_set.append(l[i].keys()[0])
            ret_vals.append(line_set)
        return ret_vals

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
