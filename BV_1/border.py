#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""this file implements the border searching algorithms"""




def checkimage(frame):
    """check image and return if street is straigth (0), left (-1) or right (1)"""

    right = checkborderright(frame)
    left = checkborderleft(frame)
    
    print "right: " + str(right)
    print "left:  " + str(left)

    return 0






# TODO: this is copy paste... adjust for left border
def checkborderleft(frame):
    """check left border"""
    border = []

    # start at frame height / 2 and go up
    for y in xrange(int(frame.height/2),39,-20):
        # start at frame width / 2 and go to the right
        for x in xrange(int(frame.width/2),frame.width,-3):
            # check if value is white
            if frame[y,x] == 255:
#                print "line at: x: " + str(x) + " y: " + str(y)
                # check if line is not just 1 pixel in width
                # TODO: make sure this isn't outside of the image
                if frame[y,x-2] == 255:
                    border.append((x,y))
                    # break so every edge is just detected once
                    break

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







def checkborderright(frame):
    """check right border"""
    border = []

    # start at frame height / 2 and go up
    for y in xrange(int(frame.height/2),39,-20):
        # start at frame width / 2 and go to the right
        for x in xrange(int(frame.width/2),frame.width,3):
            # check if value is white
            if frame[y,x] == 255:
#                print "line at: x: " + str(x) + " y: " + str(y)
                # check if line is not just 1 pixel in width
                # TODO: make sure this isn't outside of the image
                if frame[y,x+2] == 255:
                    border.append((x,y))
                    # break so every edge is just detected once
                    break

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
