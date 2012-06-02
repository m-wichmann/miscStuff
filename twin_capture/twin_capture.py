#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""this script captures the frames of two webcams into avi files"""

#####
#twin_capture
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

import cv
from optparse import OptionParser

def capture():
    """main function"""
    # parse cmd line options
    parser = OptionParser()

    parser.add_option("-0", "--file0", dest="file0", help="path of target file0")
    parser.add_option("-1", "--file1", dest="file1", help="path of target file1")

    (options, args) = parser.parse_args()
    
    file0 = "out0.avi"
    file1 = "out1.avi"

    if options.file0:
        file0 = options.file0
    if options.file1:
        file1 = options.file1

    print "[INFO ] output file0: " + str(file0)
    print "[INFO ] output file1: " + str(file1)

    # init cams
    cam0 = cv.CaptureFromCAM(0);
    cam1 = cv.CaptureFromCAM(1);

    # check if cams are init correctly
    if not cam0:
        print "[ERROR] Could not init cam0"
        return
    if not cam1:
        print "[ERROR] Could not init cam1"
        return

    # skip first frames since they are normally garbage...
    print "[INFO ] Skipping first 10 frames..."
    for i in xrange(10):
        frame0 = cv.QueryFrame(cam0)
        frame1 = cv.QueryFrame(cam1)

    # init some vars
    # TODO: calc fps and image size correctly and output on console
    writer0 = cv.CreateVideoWriter(file0, cv.CV_FOURCC('M', 'J', 'P', 'G'), 30, (320,240))
    writer1 = cv.CreateVideoWriter(file1, cv.CV_FOURCC('M', 'J', 'P', 'G'), 30, (320,240))

    # create some windows to output frames
    cv.NamedWindow("cam0", cv.CV_WINDOW_AUTOSIZE)
    cv.NamedWindow("cam1", cv.CV_WINDOW_AUTOSIZE)

    print "[INFO ] Starting recording..."
    print "[INFO ] To quit press q or esc..."
    while True:
        # save the frames we want...
        frame0 = cv.QueryFrame(cam0)
        frame1 = cv.QueryFrame(cam1)

        # check if frames are valid
        if not frame0:
            print "[ERROR] could not query frame from cam0"
            continue
        if not frame1:
            print "[ERROR] could not query frame from cam1"
            continue

        # write frames to video files
        cv.WriteFrame(writer0, frame0)
        cv.WriteFrame(writer1, frame1)

        # output frames...
        cv.ShowImage("cam0", frame0)
        cv.ShowImage("cam1", frame1)
        key = cv.WaitKey(100)
        if key == 113 or key == 27: # esc or q key
            break

    # destroy stuff...
    print "[INFO ] destroying opencv objects..."
    cv.DestroyWindow("cam0");
    cv.DestroyWindow("cam1");
    del(writer0)
    del(writer1)
    del(cam0)
    del(cam1)

    print "[INFO ] everything done... bye..."


if __name__ == '__main__':
    capture()
