#!/usr/bin/python

#####
# cp_wrapper, cp wrapper that adds a progress bar to the cp command
#
# Copyright 2012, erebos42 (https://github.com/erebos42/miscScripts)
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of
# the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this software; if not, write to the Free
# Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA, or see the FSF site: http://www.fsf.org.
#####

# TODO:
# - parse flags dynamically

import os
import sys
import subprocess
import string
import time
import collections
from datetime import datetime
from datetime import timedelta

def main():
    flags = ""
    src = ""
    dest = ""

    # parse sys.argv[]
    if (len(sys.argv) == 3):
        src = sys.argv[1]
        dest = sys.argv[2]
    elif (len(sys.argv) == 4):
        flags = sys.argv[1]
        src = sys.argv[2]
        dest = sys.argv[3]
    else:
        print "usage:"
        print "python cp_wrapper -FLAGS src dest"
        print "Flags must be all without spaces between them..."

    # start cp command in background and pass arguments on
    command = "cp " + flags + " " + src + " " + dest + " &"
    os.system(command)

    # get size if source file
    srcsize = os.stat(src)

    # get pid of cp process so it can be tracked later
    proc1 = subprocess.Popen(["ps -Af | grep -m1 \"" + command + "\" | awk '{print $2}'"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc1.communicate()
    # TODO: THIS IS NOT GOOD! WHY IS THE PID ALWAYS OFF BY ONE???
    pid = int(out) - 1

    # try/except to catch ^C Keyboard Interrupt
    try:
        keepgoing = True
        # TODO: destsize should be initialized with an os.stat object with 0 bytes size. Quick Hack: use /dev/zero instead
        destsize = os.stat("/dev/zero")

        # initialize the size and time ring buffer to calculate speed and ETA
        cptime = datetime.now()
        sizehistory = collections.deque(maxlen=8)
        for i in range(0, sizehistory.maxlen):
            sizehistory.append(0L)
        timehistory = collections.deque(maxlen=8)
        for i in range(0, timehistory.maxlen):
            timehistory.append(cptime)

        # while loop until cp process is done
        while (keepgoing):

            # check if cp process is still there. This could probably be improved
            cmd = "ps -p " + string.strip(str(pid),"\n") + " | wc -l"
            proc2 = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
            (temp, err) = proc2.communicate()
            temp = int(temp)
            if (temp != 2):
                keepgoing = False

            # calc current size of destination an current time
            destsize = os.stat(dest)
            cptime = datetime.now()
            # store size and time in circular buffer for current speed and ETA 
            sizehistory.append(destsize.st_size)
            timehistory.append(cptime)

            # calculate current speed
            temp3 = 0
            for i in range(0, sizehistory.maxlen - 1):
                temp1 = (sizehistory[i+1] - sizehistory[i]) / 1000000 
                temp2 = timehistory[i+1] - timehistory[i]
                if (temp2.total_seconds() == 0):
                    temp3 = 0
                else:
                    temp3 = temp3 + (temp1/temp2.total_seconds())
            temp3 = temp3 / (sizehistory.maxlen - 1)

            # TODO: calc est. time         

            # calculate current percentage
            percent = (destsize.st_size * 100) / srcsize.st_size

            # build the output string
            out = "["
            for x in range(0, (percent / 2)):
                out += "#"
            for x in range((percent / 2), 50):
                out += "-"

            out += "] "
            out += str(percent).rjust(3) + " %  " + str(int(temp3)).rjust(4) + " Mb/s"
            # Print the output string. It should always be printed on one line, but for some reason it's to slow -.-
            print out
#            print '{0}\r'.format(out),

            # sleep until next check
            # TODO: check if sleep() is to inaccurate, since there are these weird stutters
            time.sleep(0.25)
    # catch ^C Exception and make sure the cp process is also killed. Otherwise it would be ghosting around in the background
    except KeyboardInterrupt:
        os.system("kill " + str(pid))
        sys.exit(0)

main()
