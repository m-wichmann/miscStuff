#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import src.entities as entities

class Game(object):
    def __init__(self):
        self.point = 0
        self.level = 1

        self.width = 10
        self.height = 20
        self.field = []
        for i in range(self.height):
            self.field.append([])
            for j in range(self.width):
                self.field[i].append(' ')

        # init active stones
        self.activeStone = None
        self.nextStone = None
        self.nextRound()


    def printField(self):

        # clear field, char _ as placeholder
        tempfield = []
        for i in range(self.height):
            tempfield.append([])
            for j in range(self.width):
                tempfield[i].append('_')

        # place active stone
        for field in self.activeStone.value:
            x = None
            y = None
            for val in field:
                if x == None:
                    x = val
                else:
                    y = val
            tempfield[self.activeStone.row + x][self.activeStone.column + y] = 'o'



        # TODO: place rested stones


        # print field
        for row in tempfield:
            for field in row:
                print field,
            print
        

    def nextRound(self):
        if self.activeStone == None:
            if self.nextStone == None:
                self.activeStone = entities.Stone()
                self.nextStone = entities.Stone()
            else:
                self.activeStone = self.nextStone
                self.nextStone = entities.Stone()
            self.__placeActiveStone()
        self.__lowerActiveStone()


    def __placeActiveStone(self):
        print "placeActiveStone()"

        self.activeStone.row = -2
        self.activeStone.column = 3

        self.__checkCollision()


    def __lowerActiveStone(self):
        print "lowerActiveStone()"

        self.activeStone.row = self.activeStone.row + 1

        self.__checkCollision()


    def __checkCollision(self):
        print "checkCollision()"
















