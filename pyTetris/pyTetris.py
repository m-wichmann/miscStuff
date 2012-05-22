#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

#####
#pyTetris
#
#Copyright 2012, erebos42 (https://github.com/erebos42/miscScripts)
#
#This is free software; you can redistribute it and/or modify it
#under the terms of the GNU Lesser General Public License as
#published by the Free Software Foundation; either version 2.1 of
#the License, or (at your option) any later version.
#
#This software is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this software; if not, write to the Free
#Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
#02110-1301 USA, or see the FSF site: http://www.fsf.org.
#####

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
