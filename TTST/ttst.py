#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

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


class TTST():
    def cli(self):
        self.data = self.loadData("./data.json")

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
    

    # TODO: make this more dynamic
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
        json.dump(temp, fh)
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

    output = []    

    # get data from file
    obj = TTST()
    data = obj.loadData("./data.json")

    # output player
    output.append("<h1>Player</h1>")

    output.append("<table>")
    output.append("<tr>")
    output.append("<th>ID</th>")
    output.append("<th>Name</th>")
    output.append("</tr>")

    player = {}
    for p in data["player"]:
        # store player in dict for later use
        player[str(p.pid)] = p.name
        output.append("<tr>")
        output.append("<td>" + str(p.pid) + "</td>")
        output.append("<td>" + str(p.name) + "</td>")
        output.append("</tr>")
    output.append("</table>")


    # output matches
    output.append("<h1>Matches</h1>")

    output.append("<table>")
    output.append("<tr>")
    output.append("<th>Player 1</th>")
    output.append("<th>Points 1</th>")
    output.append("<th>Points 2</th>")
    output.append("<th>Player 2</th>")
    output.append("<th>Aufschlag</th>")
    output.append("<th>Süd</th>")
    output.append("<th>Zeit</th>")
    output.append("</tr>")

    for m in data["matches"]:
        output.append("<tr>")
        output.append("<td>" + str(player[str(m.playerid1)]) + "</td>")
        output.append("<td>" + str(m.points1) + "</td>")
        output.append("<td>" + str(m.points2) + "</td>")
        output.append("<td>" + str(player[str(m.playerid2)]) + "</td>")
        output.append("<td>" + str(m.serveplayer1) + "</td>")
        output.append("<td>" + str(m.southplayer1) + "</td>")
        output.append("<td>" + str(m.time) + "</td>")
        output.append("</tr>")
    output.append("</table>")

    # generate response
    output_len = sum(len(line) for line in output)
    start_response('200 OK', [('Content-type', 'text/html'),
                              ('Content-Length', str(output_len))])

    return output





if __name__ == '__main__':
    # wsgi interface using the python simple http server
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

    # cli interface
#    obj = TTST()
#    obj.cli()












