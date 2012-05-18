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
    def main(self):
        self.data = self.loadData("./data.json")

#        self.addPlayer("Markus")
#        self.addPlayer("Martin")
#        self.addPlayer("Christian")
#        self.addMatch("Markus", "Martin", 11, 3, 1, 1, 0)

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


if __name__ == '__main__':
    obj = TTST()
    obj.main()
