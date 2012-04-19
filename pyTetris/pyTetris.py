#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import src.game as game
import src.entities as entities

class PyTetris(object):
    def __init__(self):
        pass





if __name__ == '__main__':
    print "Start!"

    obj = game.Game()
    print "====="
    obj.nextRound()
    obj.printField()
    print "====="
    obj.nextRound()
    obj.printField()
    print "====="
    obj.nextRound()
    obj.printField()
    print "====="
    obj.nextRound()
    obj.printField()

    print "Done!"


#    obj = PyTetris()
#    obj.main()
