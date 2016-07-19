#!/usr/bin/env python

# Author: Remi Marchand
# Date: July 15, 2016
# Description: Attempt to make a collection_date relational database

import os
import sqlite3

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

column_strs = ["collection_date"]

class SQL_Manager():
    """SQL_Manager manages an sql_databse
       It works just with dates for now"""
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def new_table(self):
        format_str = """
        CREATE TABLE "{database}" (
        INTEGER PRIMARY KEY,
        RUN VARCHAR(15),
        Collection_Date DATE,
        Error INTEGER,
        Original VARCHAR(15),
        Ambiguous BOOLEAN
        );"""

        sql_command = format_str.format(database=self.db_name)
        self.cursor.execute(sql_command)
        self.connection.commit()

    def add_date(self, date_info):
        format_str = """
        INSERT INTO {database} (RUN, Collection_Date, Error, Original, Ambiguous)
        VALUES ("{run}", "{col_date}", "{error}", "{orig}", "{amb}");"""

        sql_command = format_str.format(database=self.db_name,
                                        run=date_info[0],
                                        col_date=date_info[1],
                                        error=date_info[2],
                                        orig=date_info[3],
                                        amb=date_info[4])
        self.cursor.execute(sql_command)
        self.connection.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM %s" % self.db_name)
        result = self.cursor.fetchall()
        for r in result:
            print r
