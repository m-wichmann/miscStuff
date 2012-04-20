#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import src.game as game
import src.entities as entities

class PyTetris(object):
    def __init__(self):
        pass





if __name__ == '__main__':
    print "Start!"

#    obj = entities.Stone()
#    obj.printStones()

    obj = game.Game()
    for x in range(0,20):
        obj.printField()
        obj.nextRound()
    

    print "Done!"


#    obj = PyTetris()
#    obj.main()
