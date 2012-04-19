#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


import pygtk
pygtk.require("2.0")
import gtk

class GUI(object):
    def startGTK(self):
        gtk.main()


    def destroy(self, *args):
        gtk.main_quit()


    def addSong(self, *args):
        for x in range(0,20):
            self.treestore.append(None, ["asd"])
        pass


    def __init__(self, r):
        self.builder = gtk.Builder()
        self.builder.add_from_file("repo.glade")
        self.window = self.builder.get_object("repoWindow")
        self.window.connect('destroy', self.destroy)
        button = self.builder.get_object("buttonAddSong")
        button.connect('clicked', self.addSong)

        self.createTreeStore()

        self.repoToTree(r)

        self.window.show()


    def repoToTree(self, r):
        for s in r.repo:
            self.treestore.append(None, [r.repo[s].artist + " - " + r.repo[s].title])


    def createTreeStore(self):
        # create a treestore
        self.treestore = gtk.TreeStore(str)

        # get treeview from builder and set model
        self.treeview = self.builder.get_object("repotree")
        self.treeview.set_model(self.treestore)

        self.cell = gtk.CellRendererText()

        self.namecolumn = self.treeview.insert_column_with_attributes(-1, 'Name', self.cell, text=0)

#        self.namecolumn.pack_start(self.cell, True)
        self.namecolumn.add_attribute(self.cell, 'text', 0)
        self.namecolumn.set_sort_column_id(0)

        self.treeview.set_search_column(0)





