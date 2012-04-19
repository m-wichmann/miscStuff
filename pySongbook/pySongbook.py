#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import src.song as song
import src.repo as repo
import src.repoio as repoio
import src.gui as gui

class PySongbook(object):

    rio = None

    def __init__(self):
        self.rio = repoio.RepoIO()

    def main(self):
        r = self.rio.loadRepoFromDisk("/home/erebos/temp/pySongbook/")

        g = gui.GUI(r)
        g.startGTK()


#        while (1):
#            print "===================="
#            print "= 1. List Repo"
#            print "===================="
#            print "= 2. Add Song"
#            print "= 3. Modify Song"
#            print "= 4. Remove Song"
#            print "===================="
#            print "= 0. Exit"
#            print "===================="
#            # TODO: user input
#            choice = raw_input()
#
#            # TODO: check input and do something ;-)
#            if choice == "1":
#                print r
#            elif choice == "2":
#                s = song.Song("Cake", "Phone")
#                s.year = 2004
#                r.addSong(s)
#            elif choice == "3":
#                pass
#            elif choice == "4":
#                pass
#            elif choice == "0":
#                break
#            else:
#                pass

        self.rio.saveRepoToDisk(r, "/home/erebos/temp/pySongbook/")





if __name__ == '__main__':
    obj = PySongbook()
    obj.main()
