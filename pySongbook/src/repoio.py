#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

#import cPickle as pickle
import string
import pickle
import glob
import os
import tarfile
import repo
import song

class RepoIO(object):

    def __init__(self):
        pass

    def saveRepoToDisk(self, r, path):
        # delete all existing songs
        for infile in glob.glob( os.path.join(path, '*.song') ):
            os.remove(infile)

        # dump all songs
        for song_hash in r.repo:
            fd = open(path + song_hash + ".song", "wb")
            pickle.dump(r.repo[song_hash], fd)
            fd.close()

    def loadRepoFromDisk(self, path):
        try:
#            tar = tarfile.open(path + "repo.tar.bz2", "r:bz2")
#            tar.extractall(path=path)
#            tar.close        

            r = repo.Repo()

            for infile in glob.glob( os.path.join(path, '*.song') ):
                fd = open(infile, "rb")
                r.addSong(pickle.load(fd))
                fd.close()
            return r
        except (tarfile.ReadError, IOError):
            return repo.Repo()

    def packRepo(self, path):
        pass
        # pack repo in tar

        filelist = ""
        for infile in glob.glob( os.path.join(path, '*.song') ):
            filelist = filelist + " ./" + infile[string.rfind(infile, "/") + 1:]
#            filelist = filelist + " " + infile

        print filelist

        os.system("tar cjf repo.tar.bz2 " + filelist)

#        tar = tarfile.open(path + "repo.tar.bz2", "w:bz2")
#        for infile in glob.glob( os.path.join(path, '*.song') ):
            # TODO: check if file are correctly added to tar file
#            tar.addfile(tarfile.TarInfo(infile[string.rfind(infile, "/") + 1:]), file(infile))
#            tar.add(infile, recursive=False)
#        tar.close()

        # delete all songs
        for infile in glob.glob( os.path.join(path, '*.song') ):
            os.remove(infile)



















