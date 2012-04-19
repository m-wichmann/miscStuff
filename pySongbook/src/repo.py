#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import song

class Repo(object):

    repo = {}

    def __init__(self):
        pass

    def addSong(self, s):
        self.repo[s.song_hash] = s

# TODO: testing...
    def delSong(self, s):
        if type(s).__name__=='Song':
            del self.repo[s.song_hash]

    def getSongByName(self, artist, title):
        for s in self.repo:
            if self.repo[s].artist == artist and self.repo[s].title == title:
                return self.repo[s]

    def __str__(self):
        ret = ""
        for hash_value in self.repo:
            ret += str(self.repo[hash_value]) + "\n"
        return ret

#    def __getstate__(self):
#        return self.repo

#    def __setstate__(self, dict):
#        self.repo = dict

#    def default(self, o):
#        return o.repo
