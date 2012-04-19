#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import random

class Stone(object):

    def __init__(self):
        # init available stones
        # TODO: outsource to constant or something
        self.stones = {}
        self.stones["J"] = [[' ',' ',' '],[' ','x',' '],[' ','x',' '],['x','x',' ']]
        self.stones["L"] = [[' ',' ',' '],['x',' ',' '],['x',' ',' '],['x','x',' ']]
        self.stones["I"] = [[' ','x',' '],[' ','x',' '],[' ','x',' '],[' ','x',' ']]
        self.stones["O"] = [[' ',' ',' '],['x','x',' '],['x','x',' '],[' ',' ',' ']]
        self.stones["S"] = [[' ',' ',' '],[' ','x','x'],['x','x',' '],[' ',' ',' ']]
        self.stones["T"] = [[' ',' ',' '],[' ','x',' '],['x','x','x'],[' ',' ',' ']]
        self.stones["Z"] = [[' ',' ',' '],['x','x',' '],[' ','x','x'],[' ',' ',' ']]

        self.value = self.stones[random.choice(list(self.stones.keys()))]

        self.row = None
        self.column = None

    def printStones(self):
        print "printStones()"
        for stone in self.stones:
            print stone + ":"
            for row in self.stones[stone]:
                for field in row:
                    print field,
                print

    def printValue(self):
        for row in self.value:
            for field in row:
                print field,
            print





















