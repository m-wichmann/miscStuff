#!/usr/bin/python
# -*- coding: utf-8 -*-
"""script for shuting down a server"""

#####
#server_down
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

import sys
import os
import commands
import string

pfad = sys.argv[1:]

if pfad == []:
	sys.exit(1)

fd = open(pfad[0], "r")

fdlog = open("/var/log/server_down.log", "r")
linecount = 0
for lines in fdlog:
	linecount += 1
fdlog.close()

fdlog = open("/var/log/server_down.log", "a")

if linecount >= 1000:
	print "delete lines from log"

fdlog.write("===============" + "\n")
fdlog.write("Date: " + commands.getoutput("date") + "\n")
fdlog.write("===============" + "\n")

liste = []

check = 0

for line in fd:
	temp = string.split(line)
	if temp and temp[0].count('.') == 3:
		liste.append(temp[0])

fd.close()

for el in liste:

	fdlog.write("Ziel IP: " + el + "\n")

	if el != "127.0.0.1" and el != "192.168.10.17" and el != "192.168.10.2":
		command = 'ping -c 1 ' + el + ' | grep "Destination Host Unreachable"'
		returnval = os.system(command)

		fdlog.write("returnval: " + str(returnval/256) + "\n")

		check = check + returnval

		fdlog.write("-----" + "\n")


if check == 0:
	fdlog.write("No IPs online. Shutting Down!" + "\n")
	fdlog.write("===============" + "\n")
	fdlog.close()
	os.system('/sbin/shutdown -h 1')
if check != 0:
	fdlog.write(str(returnval/256) + " IPs online. Exiting script!" + "\n")
	fdlog.write("===============" + "\n")
	fdlog.close()
print "DONE!"
