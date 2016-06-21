#!/usr/bin/env/python

from Parent import Parent

class Child(Parent):
    def __init__(self):
        Parent.__init__(self)
        print self.num_combinations

son = Child()
print son.num_combinations
