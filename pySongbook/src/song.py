#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import time
import hashlib

class Song(object):

    song_hash = ""
    artist = ""
    title = ""
    year = 0
    label = ""
    note = ""
    lyric = ""
    time_created = 0

    def __init__(self, artist, title):
        self.artist = artist
        self.title = title
        self.time_created = int(time.time())
        self.song_hash = self.calcHash()

    def __str__(self):
        return "[" + self.song_hash + "] " + self.artist + ", " + self.title + " (" + str(self.year) + ")"

    def calcHash(self):
        song_string = self.artist + self.title + str(self.time_created)
        h = hashlib.md5(song_string)
        return h.hexdigest()
