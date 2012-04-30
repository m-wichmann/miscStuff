#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import json


class Match(object):
    def __init__(self):
        self.time = None
        self.player1 = None # player 1 object
        self.player2 = None # player 2 object
        self.points1 = 0 # points player 1
        self.points2 = 0 # points player 2
        self.serve = None # wer hatte aufschlag
        self.south = None # wer spielt im süden

class Player(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

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
                player1 = raw_input("Player 1:")
                player2 = raw_input("Player 2:")
                points1 = raw_input("Points 1:")
                points2 = raw_input("Points 2:")
                serve = raw_input("Serve:")
                south = raw_input("South:")
                time = raw_input("Time:")
                ret = self.addMatch(player1, player2, points1, points2, serve, south, time)
                if ret == -1:
                    print "Could not add match"
            elif (userInput == "8"):
                for entry in self.data["player"]:
                    print entry.name
            elif (userInput == "9"):
                for entry in self.data["matches"]:
                    print str(entry.player1) + " " + str(entry.points1) + ":" + str(entry.points2) + " " + str(entry.player2)

        self.saveData(self.data, "./data.json")



    def addPlayer(self, name):
        player = Player(name)
        self.data["player"].append(player)
        return player

    def addMatch(self, player1, player2, points1, points2, serve, south, time):
        match = Match()

        match.player1 = None
        match.player2 = None

        for entry in self.data["player"]:
            if entry.name == player1:
                match.player1 = entry
            if entry.name == player2:
                match.player2 = entry

        match.points1 = points1
        match.points2 = points2
        match.serve = serve
        match.south = south
        match.time = time

        if (match.player1 == None or match.player1 == None):
            return -1
        else:
            self.data["matches"].append(match)
            return match
    
    # TODO: make this more dynamic
    def dataToJSON(self, data):
        JSONdata = {"player": [], "matches": []}
        for entry in data["player"]:
            JSONdata["player"].append(str(entry))
        for entry in data["matches"]:
            temp = entry.__dict__
            temp["player1"] = str(temp["player1"])
            temp["player2"] = str(temp["player2"])
            JSONdata["matches"].append(temp)
        return JSONdata

    # TODO: get this to work!
    def JSONToData(self, data):
        ret = {"player": [], "matches": []}
        for player in data["player"]:
            ret["player"].append(self.addPlayer(player))
        for match in data["matches"]:
            ret["matches"].append(self.addMatch(entry["player1"],entry["player2"],entry["points1"],entry["points2"],entry["serve"],entry["south"],entry["time"],))
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
            print ret
            return ret
        except:
            return {"player": [], "matches": []}




if __name__ == '__main__':
    obj = TTST()
    obj.main()
