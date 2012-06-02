#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""in this script two video files are evaluated"""


import cv
import border
from optparse import OptionParser

def main():
    """main method"""
    print "Start"


    parser = OptionParser()

    parser.add_option("-l", "--left", dest="left", help="left video file")
    parser.add_option("-r", "--right", dest="right", help="right video file")
    parser.add_option("-s", "--sync", dest="sync", help="sync videos. Frames of left video are skipped arcording to given value. Negative Values are used to skip frames on right video.")

    (options, args) = parser.parse_args()

    if (not options.left) or (not options.right):
        parser.error('files not specified')

    filepathleft = options.left
    filepathright = options.right

    # open video file
#    filepathleft = "ocupleft.avi"
    dataleft = openfile(filepathleft)
#    filepathright = "ocupright.avi"
    dataright = openfile(filepathright)

    # TODO: be able to sync videos (skip some frames...)
    # TODO: remember: if frames are skipped, the for xrange loop doesn't have to go that far...

    limit = 0
    if dataleft["fcount"] > dataright["fcount"]:
        limit = dataleft["fcount"] - 1
    else:
        limit = dataright["fcount"] - 1

    for f in xrange(limit):

        # query next frame from video
        frameleft = cv.QueryFrame(dataleft["video"])
        frameright = cv.QueryFrame(dataright["video"])

        # create images to store... well... images...
        frameleftbw = cv.CreateImage((frameleft.width, frameleft.height), cv.IPL_DEPTH_8U, 1)
        frameleftbin = cv.CreateImage((frameleft.width, frameleft.height), cv.IPL_DEPTH_8U, 1)
        frameleftedges = cv.CreateImage((frameleft.width, frameleft.height), cv.IPL_DEPTH_8U, 1)
        frameleftout = cv.CreateImage((frameleft.width, frameleft.height), cv.IPL_DEPTH_8U, 1)
        frameleftoutcol = cv.CreateImage((frameleft.width, frameleft.height), cv.IPL_DEPTH_8U, 3)

        framerightbw = cv.CreateImage((frameright.width, frameright.height), cv.IPL_DEPTH_8U, 1)
        framerightbin = cv.CreateImage((frameright.width, frameright.height), cv.IPL_DEPTH_8U, 1)
        framerightedges = cv.CreateImage((frameright.width, frameright.height), cv.IPL_DEPTH_8U, 1)
        framerightout = cv.CreateImage((frameright.width, frameright.height), cv.IPL_DEPTH_8U, 1)
        framerightoutcol = cv.CreateImage((frameright.width, frameright.height), cv.IPL_DEPTH_8U, 3)

        # rgb to grayscale
        cv.CvtColor(frameleft,frameleftbw,cv.CV_BGR2GRAY)
        cv.CvtColor(frameright,framerightbw,cv.CV_BGR2GRAY)

        # grayscale to binary
        cv.Threshold(frameleftbw, frameleftbin, 150, 255, cv.CV_THRESH_BINARY);
        cv.Threshold(framerightbw, framerightbin, 150, 255, cv.CV_THRESH_BINARY);

        cv.Copy(frameleftbin, frameleftout)
        cv.Copy(framerightbin, framerightout)

        cv.CvtColor(frameleftout, frameleftoutcol, cv.CV_GRAY2RGB)
        cv.CvtColor(framerightout, framerightoutcol, cv.CV_GRAY2RGB)

        # check the image and get result if street is straight or curved
        resultleft = checkimage(frameleftbin, frameleftoutcol)
        resultright = checkimage(framerightbin, framerightoutcol)

        cv.ShowImage("left", frameleftoutcol)
        cv.ShowImage("right", framerightoutcol)
        cv.WaitKey(50000)

    # delete used ressources
    deleteRessources(data)

    print "Done"








def checkimage(frame, frameout):
    """check image and return if street is straigth (0), left (-1) or right (1)"""
    ret = border.checkimage(frame, frameout)
    return ret


def deleteRessources(data):
    """delete used resources (namely the capture object)"""
    del(data["video"])


def openfile(filepath):
    """open video at filepath and return dict with data"""
    # capture video from file
    video = cv.CaptureFromFile(filepath)
    
    # extract some information
    width = int(cv.GetCaptureProperty(video, cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(cv.GetCaptureProperty(video, cv.CV_CAP_PROP_FRAME_HEIGHT))
    fps = int(cv.GetCaptureProperty(video, cv.CV_CAP_PROP_FPS))
    fcount = int(cv.GetCaptureProperty(video, cv.CV_CAP_PROP_FRAME_COUNT))

    # print video data
    print "======"
    print "Opened file: " + filepath
    print "Width: " + str(width)
    print "Height: " + str(height)
    print "FPS: " + str(fps)
    print "Frame count: " + str(fcount)
    print "======"

    # store data in dict
    # TODO: check if necesarry
    data = {}
    data["video"] = video
    data["height"] = height
    data["width"] = width
    data["fps"] = fps
    data["fcount"] = fcount

    return data


if __name__ == '__main__':
    main()
