#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys
from optparse import OptionParser

def wcc(path):
    """opens every file in path and sums up the word count results"""

    # normalize path, so we know what to deal with
    path = os.path.normpath(path)

    # get all files in path
    listing = os.listdir(path)

    # iterate through files and sum up file results
    completesum = 0
    for infile in listing:
        # try if file really exists (should not happen)
        try:
            # open file
            fd = open(path + "/" + infile,'r')
            summe = 0
            # iterate through file and sum up lines
            for line in fd:
                temp = line.split()
                summe = summe + int(temp[1])
            fd.close()
            completesum = completesum + summe
            print "sum in file: " + infile + ": " + str(summe)
        except IOError:
            print "[ERROR] Could not open file"
            print "[ERROR] This should not have happend -.-"
            sys.exit(-1)
            
    # output result
    print "====="
    print "sum of all files: " + str(completesum)


if __name__ == '__main__':
    # create option parser with specific options
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="dir", help="directory of wordcount result files")

    # get result from option parser
    (options, args) = parser.parse_args()

    # if a dir is specified, call wcc, otherwise...
    if options.dir != None:
        wcc(options.dir)
    else:
        print "Please specify a result directory"
