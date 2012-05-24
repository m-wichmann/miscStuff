#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""this file implements the border searching algorithms"""

import cv


def checkimage(frame, frameout):
    """check image and return if street is straigth (0), left (-1) or right (1)"""

    right = checkborderright(frame, frameout)
    left = checkborderleft(frame, frameout)
    stop = checkstop(frame, frameout)

#    print "right: " + str(right)
#    print "left:  " + str(left)

    # TODO: evaluate vars right, left, stop

    return right






def checkstop(frame, frameout):
    """check in front for a stop line"""
    # array with potential stop line positions
    stop = []

    # check always in the middle of the frame
    x = frame.width/2

    # check from almost bottom of the frame to somewhere up the frame
    for y in xrange(frame.height-50,(frame.height/4),-5):
        # if pixel is white check left and right
        if frame[y,x] == 255:
            # don't rely on a single point, so test some more points at the left and right
            if frame[y,x - 40] == 255 and frame[y,x - 20] == 255 and frame[y,x + 20] == 255 and frame[y,x + 40] == 255:
                cv.Line(frameout, (x - 40,y), (x + 40,y), cv.CV_RGB(255, 0, 0), thickness=4)
                stop.append((x,y))

    # TODO: analyse the stop data


    # TODO: return info about the position of the stop line
    return 0





def checkborderleft(frame, frameout):
    """check left border"""
    border = []

    # start at frame height / 2 and go up
    for y in xrange(int(frame.height/2),39,-20):
        # start at frame (width / 2) - 20 and go to the left
        for x in xrange(int(frame.width/2) - 20,0,-3):
            # check if value is white
            if frame[y,x] == 255:
                # make sure we don't read outside the frame
                if x < 2:
                    x = 2
                # check if line is not just 1 pixel in width
                if frame[y,x-2] == 255:
                    border.append((x,y))
                    # break so every edge is just detected once
                    break


    if len(border) > 0:
        p1 = border[0]
        p2 = border[len(border)-1]
        cv.Line(frameout, p1, p2, cv.CV_RGB(0, 0, 255), thickness=4)



    # TODO: check if left border values are left turn or what?!
    result = 0

    if result > 1:
        result = 1
    if result < -1:
        result = -1

    return result







def checkborderright(frame, frameout):
    """check right border"""
    border = []

    # start at frame height / 2 and go up
    for y in xrange(int(frame.height/2),39,-20):
        # start at frame (width / 2) + 20 and go to the right
        for x in xrange(int(frame.width/2) + 20,frame.width,3):
            # check if value is white
            if frame[y,x] == 255:
                # make sure we don't read outside the frame
                if (x > (frame.width - 3)):
                    x = frame.width - 3
                # check if line is not just 1 pixel in width
                if frame[y,x+2] == 255:
                    border.append((x,y))
                    # break so every edge is just detected once
                    break


    if len(border) > 0:
        p1 = border[0]
        p2 = border[len(border)-1]
        cv.Line(frameout, p1, p2, cv.CV_RGB(0, 0, 255), thickness=4)


    # TODO: check if right border values are left turn or what?!
    result = 0


    if result > 1:
        result = 1
    if result < -1:
        result = -1

    return result
