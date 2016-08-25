#!/usr/bin/env python

column_strs = ["RUN/PRIMARY_ID", "SAMPLE/PRIMARY_ID", "EXPERIMENT_REF/PRIMARY_ID",
               "STUDY/PRIMARY_ID", "size", "total_bases", "SPOT_LENGTH", "total_spots",
               "organism", "PLATFORM", "INSTRUMENT_MODEL", "sub_species", "Subspecies"]

keys = [""]


def parse(id_info):
    return [id_info]
