#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import random

class Stone(object):

    def __init__(self):
        # init available stones
        # TODO: outsource to constant or something
        self.stones = {}
        # [row, cloumn]
        self.stones["J"] = [[0,0],[1,0],[1,1],[1,2]]
        self.stones["L"] = [[1,0],[1,1],[1,2],[0,2]]
        self.stones["I"] = [[0,0],[0,1],[0,2],[0,3]]
        self.stones["O"] = [[0,0],[1,0],[1,1],[0,1]]
        self.stones["S"] = [[1,0],[1,1],[0,1],[0,2]]
        self.stones["T"] = [[1,0],[1,1],[0,1],[1,2]]
        self.stones["Z"] = [[0,0],[0,1],[1,1],[1,2]]
#        self.stones["J"] = [[' ',' ',' '],[' ','x',' '],[' ','x',' '],['x','x',' ']]
#        self.stones["L"] = [[' ',' ',' '],['x',' ',' '],['x',' ',' '],['x','x',' ']]
#        self.stones["I"] = [[' ','x',' '],[' ','x',' '],[' ','x',' '],[' ','x',' ']]
#        self.stones["O"] = [[' ',' ',' '],['x','x',' '],['x','x',' '],[' ',' ',' ']]
#        self.stones["S"] = [[' ',' ',' '],[' ','x','x'],['x','x',' '],[' ',' ',' ']]
#        self.stones["T"] = [[' ',' ',' '],[' ','x',' '],['x','x','x'],[' ',' ',' ']]
#        self.stones["Z"] = [[' ',' ',' '],['x','x',' '],[' ','x','x'],[' ',' ',' ']]

        self.value = self.stones[random.choice(list(self.stones.keys()))]

        self.row = None
        self.column = None

    def printStones(self):
        print "printStones()"
        for stone in self.stones:
            print stone + ":"
            temp = [[' ',' ',' ',' '],[' ',' ',' ',' '],[' ',' ',' ',' '],[' ',' ',' ',' ']]
            for row in self.stones[stone]:
                x = None
                y = None
                for field in row:
                    if x == None:
                        x = field
                    else:
                        y = field
                temp[x][y] = 'x'
            for row in temp:
                for field in row:
                    print field,
                print

    def printValue(self):
        for row in self.value:
            for field in row:
                print field,
            print





















