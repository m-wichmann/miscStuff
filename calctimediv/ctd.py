#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

#####
#wordcountcount
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

import datetime
from optparse import OptionParser

def ctd(time):
    # expected input format "2012-05-23 12:49:52     2012-05-23 12:55:21"
    temp = time.split()

    date1string = temp[0]
    time1string = temp[1]
    date2string = temp[2]
    time2string = temp[3]

    date1token = date1string.split("-")
    time1token = time1string.split(":")
    date2token = date2string.split("-")
    time2token = time2string.split(":")

    time1 = datetime.datetime(year=int(date1token[0]),month=int(date1token[1]),day=int(date1token[1]),hour=int(time1token[0]),minute=int(time1token[1]),second=int(time1token[2]))

    time2 = datetime.datetime(year=int(date2token[0]),month=int(date2token[1]),day=int(date2token[1]),hour=int(time2token[0]),minute=int(time2token[1]),second=int(time2token[2]))

    timedelta = time2-time1

    print "time1: " + str(time1)
    print "time2: " + str(time2)
    print "=================="
    print "timediv: " + str(timedelta)
    


if __name__ == '__main__':
    # create option parser with specific options
    parser = OptionParser()
    parser.add_option("-t", "--time", dest="time", help="string with the two times")

    # get result from option parser
    (options, args) = parser.parse_args()

    # if a dir is specified, call wcc, otherwise...
    if options.time != None:
        ctd(options.time)
    else:
        print "Please specify a time string"
