#!/usr/bin/env/python

class Parent(object):
    def __init__(self):
        self.num_combinations = 4

class Child(Parent):
    def return_combinations(self):
        print self.num_combinations

#dad = Parent()
son = Child()

#print dad.num_combinations
print son.return_combinations()
