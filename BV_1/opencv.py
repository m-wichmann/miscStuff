#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""this script does an analysis of the video and outputs the direction of the street"""

# Notes:
#        cv.ShowImage( "My Video Window", frame)
#        cv.WaitKey(50)
#
# pixel access:
#   frame[row,column]
#
# cv.SaveImage("bilder/bild" + str(f).zfill(4) + ".png", frame)
#
#
#
#
# bin image:
# 255 -> Weiß
# 0   -> Schwarz


import cv
import border


def main():
    """main method"""
    print "Start"

    # open video file
    filepath = "ocup.avi"
    data = openfile(filepath)


    # DEBUG: just to skip some frames
#    for f in xrange(860):
#        frame = cv.QueryFrame(data["video"])


    # TODO: last image is empty?
    for f in xrange(data["fcount"] - 1):
#    for f in xrange(1):
        # query next frame from video
        frame = cv.QueryFrame(data["video"])

        # create images to store... well... images...
        framebw = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, 1)
        framebin = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, 1)
        frameedges = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, 1)
        frameout = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, 1)

        # rgb to grayscale
        cv.CvtColor(frame,framebw,cv.CV_BGR2GRAY)
        # grayscale to binary
        cv.Threshold(framebw, framebin, 150, 255, cv.CV_THRESH_BINARY);
        # detect edges with canny...
        cv.Canny(framebin,frameedges,150,300,3)
#        cv.Canny(framebin,frameedges,150,100,3)

        cv.Copy(framebin, frameout)

        # check the image and get result if street is straight or curved
        result = checkimage(framebin, frameout)

        # TODO: implement state machine or something
        if result == 0:
            print "straight"
        if result == -1:
            print "left"
        if result == 1:
            print "right"

        

        cv.ShowImage("window", frameout)
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
    print "Opened file: " + filepath
    print "Width: " + str(width)
    print "Height: " + str(height)
    print "FPS: " + str(fps)
    print "Frame count: " + str(fcount)

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
