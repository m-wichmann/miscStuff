#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

#####
#ttst
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

import json

class Match(object):
    def __init__(self, playerid1, playerid2, points1, points2, serveplayer1, southplayer1, time):
        self.playerid1 = playerid1
        self.playerid2 = playerid2
        self.points1 = points1
        self.points2 = points2
        self.serveplayer1 = serveplayer1
        self.southplayer1 = southplayer1
        self.time = time


class Player(object):
    def __init__(self, name, pid):
        self.name = name
        self.pid = pid
    def __str__(self):
        return str(self.pid) + " " + str(self.name)


class TTST(object):
    def __init__(self):
        self.data = self.loadData("./data.json")


    def cli(self):
        self.exit = False
        while (self.exit == False):

            for x in range(0,10):
                print ""

            print "===== TTST ====="
            print "1. Add player   "
            print "2. Add match    "
            print "8. List players "
            print "9. List matches "
            print "================"
            print "0. Exit         "
            print "================"

            userInput = raw_input("Input:")

            if (userInput == "0"):
                self.exit = True
            elif (userInput == "1"):
                print "Add new player"
                nameInput = raw_input("Playername:")
                self.addPlayer(nameInput)
            elif (userInput == "2"):
                print "Add new match"
                player1 = raw_input("Player ID 1:")
                player2 = raw_input("Player ID 2:")
                points1 = raw_input("Points 1:")
                points2 = raw_input("Points 2:")
                serveplayer1 = raw_input("Serveplayer1:")
                southplayer1 = raw_input("Southplayer1:")
                time = raw_input("Time:")
                ret = self.addMatch(player1, player2, points1, points2, serveplayer1, southplayer1, time)
                if ret == -1:
                    print "Could not add match"
            elif (userInput == "8"):
                for entry in self.data["player"]:
                    print str(entry)
            elif (userInput == "9"):
                for entry in self.data["matches"]:
                    print str(entry.playerid1) + " " + str(entry.points1) + ":" + str(entry.points2) + " " + str(entry.playerid2)

        self.saveData(self.data, "./data.json")


    def addPlayer(self, name):
        pid = 0
        pids = []        
        for p in self.data["player"]:
            pids.append(p.pid)

        pids.sort()
        try:
            pid = pids[len(pids) - 1] + 1
        except IndexError:
            pass

        player = Player(name, pid)

        self.data["player"].append(player)
        return player


    def addMatch(self, player1, player2, points1, points2, serveplayer1, southplayer1, time):
        pids = []        
        for p in self.data["player"]:
            pids.append(p.pid)

        if pids.count(int(player1)) == 1 and pids.count(int(player2)) == 1:
            match = Match(player1, player2, points1, points2, serveplayer1, southplayer1, time)
            self.data["matches"].append(match)
    

    def dataToJSON(self, data):
        JSONdata = {"player": [], "matches": []}
        for entry in data["player"]:
            JSONdata["player"].append(entry.__dict__)
        for entry in data["matches"]:
            JSONdata["matches"].append(entry.__dict__)
        return JSONdata


    def JSONToData(self, data):
        ret = {"player": [], "matches": []}

        for player in data["player"]:
            ret["player"].append(Player(player["name"], player["pid"]))
        for match in data["matches"]:
            newmatch = Match(match["playerid1"], match["playerid2"], match["points1"], match["points2"], match["serveplayer1"], match["southplayer1"], match["time"])
            ret["matches"].append(newmatch)

        return ret


    def saveData(self, data, filename):
        fh = open(filename, "wb")
        temp = self.dataToJSON(data)
        json.dump(temp, fh, indent=4)
        fh.close()


    def loadData(self, filename):
        try:
            fh = open(filename, "rb")        
            data = json.load(fh)
            ret = self.JSONToData(data)
            return ret
        except:
            return {"player": [], "matches": []}


def application(environ, start_response):

    # HTML output var
    output = []

    # create main obj and load data
    obj = TTST()

#    output.append("<pre>")
#    for e in environ:
#        output.append(str(e) + "=" + str(environ[e]) + "\n")
#    output.append("</pre>")


#############################################
    # evaluate POST data
    # TODO: make this into wsgi called methods
    # TODO: this should be threadsafe...
    if environ['REQUEST_METHOD'] == 'POST':
        # read raw data
        rawpostdata = environ['wsgi.input'].read(int(environ["CONTENT_LENGTH"]))

        # split by variable
        rawpostdata = rawpostdata.split("&")
        postdata = {}
        # split vars by = and store in dict
        for field in rawpostdata:
            postdata[field.split("=")[0]] = field.split("=")[1]

        # TODO: fix this really bad stuff
        if len(postdata) == 1:
            obj.addPlayer(postdata["newplayername"])

        if len(postdata) == 9:
            # TODO: calc date and find player ids
            # TODO: parse the arguments like they should be
            date = postdata["day"] + "-" + postdata["month"] + "-" + postdata["year"]
            obj.addMatch(postdata["player1"], postdata["player2"], postdata["points1"], postdata["points2"], postdata["serve"], postdata["south"], date)

        # save changed data
        obj.saveData(obj.data, "./data.json")
#############################################


    # generate output using the template and data
    fh = open('template.html','r')
    player = {}
    # go through template and find magic comments
    for line in fh:
        if line.find("#####INSERT_PLAYER#####") != -1:
            for p in obj.data["player"]:
                # store player in dict for later use
                player[str(p.pid)] = p.name
                output.append("<tr>")
                output.append("<td>" + str(p.pid) + "</td>")
                output.append("<td>" + str(p.name) + "</td>")
                output.append("</tr>")
        elif line.find("#####INSERT_MATCHES#####") != -1:
            for m in obj.data["matches"]:
                output.append("<tr>")
                output.append("<td>" + str(player[str(m.playerid1)]) + "</td>")
                output.append("<td>" + str(m.points1) + "</td>")
                output.append("<td>" + str(m.points2) + "</td>")
                output.append("<td>" + str(player[str(m.playerid2)]) + "</td>")
                output.append("<td>" + str(m.serveplayer1) + "</td>")
                output.append("<td>" + str(m.southplayer1) + "</td>")
                output.append("<td>" + str(m.time) + "</td>")
                output.append("</tr>")
        else:
            output.append(line)


    # generate response
    output_len = sum(len(line) for line in output)
    start_response('200 OK', [('Content-type', 'text/html'),
                              ('Content-Length', str(output_len))])

    return output


if __name__ == '__main__':
    # wsgi interface using the python simple http server
    from wsgiref.simple_server import make_server
    ip = 'localhost'
    port = 8080
    func = application
    srv = make_server(ip, port, func)

    print "Serving at " + str(ip) + ":" + str(port)
    print "Press \"CTRL+c\" to exit."

    srv.serve_forever()

    # cli interface
#    obj = TTST()
#    obj.cli()
