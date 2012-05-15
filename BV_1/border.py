#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""this file implements the border searching algorithms"""

import cv


def checkimage(frame, frameout):
    """check image and return if street is straigth (0), left (-1) or right (1)"""

    right = checkborderright(frame, frameout)
    left = checkborderleft(frame, frameout)
   
    print "right: " + str(right)
    print "left:  " + str(left)

    return 0






# TODO: this is copy paste... adjust for left border
def checkborderleft(frame, frameout):
    """check left border"""
    border = []

    # start at frame height / 2 and go up
    for y in xrange(int(frame.height/2),39,-20):
        # start at frame width / 2 and go to the left
        for x in xrange(int(frame.width/2),0,-3):
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
        cv.Line(frameout, p1, p2, cv.CV_RGB(100, 100, 100), thickness=4)



    # check if right border values are left turn or what?!
    # TODO: reimplement this! This doesn't make any sense -.-
    result = 0
    for i in xrange(0,len(border)-1):
        if border[i][0] > border[i+1][0]:
            result = result + 1
        if border[i][0] < border[i+1][0]:
            result = result - 1


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
        # start at frame width / 2 and go to the right
        for x in xrange(int(frame.width/2),frame.width,3):
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
        cv.Line(frameout, p1, p2, cv.CV_RGB(100, 100, 100), thickness=4)


    # check if right border values are left turn or what?!
    # TODO: reimplement this! This doesn't make any sense -.-
    result = 0
    for i in xrange(0,len(border)-1):
        if border[i][0] > border[i+1][0]:
            result = result + 1
        if border[i][0] < border[i+1][0]:
            result = result - 1


    if result > 1:
        result = 1
    if result < -1:
        result = -1

    return result
