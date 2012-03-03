#!/usr/bin/python

import random

class Ball(object):
    def __init__(self):
        self.height = 5
        self.width = 5
        self.position_ball_x = 320 # 0 to 585
        self.position_ball_y = 180 # 0 to 350

        temp = (random.random() * 2) + 2
        self.velocity_ball_x = temp
        temp = (random.random() * 2) + 2
        self.velocity_ball_y = temp

        temp = random.randint(0, 1)
        if (temp == 1):
            self.velocity_ball_x = -self.velocity_ball_x

        temp = random.randint(0, 1)
        if (temp == 1):
            self.velocity_ball_y = -self.velocity_ball_y



class Paddle(object):
    def __init__(self):
        self.height = 55
        self.width = 5
        self.position = 150 # 0 to 300 (actually frame height - paddle height)

    def down(self, amount):
        self.position = self.position + amount
        if (self.position <= 0):
            self.position = 0
        elif (self.position >= 300):
            self.position = 300

    def up(self, amount):
        self.position = self.position - amount
        if (self.position <= 0):
            self.position = 0
        elif (self.position >= 300):
            self.position = 300




class Player(object):
    def __init__(self):
        self.score = 0
        self.paddleobj = Paddle()


class Game(object):

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.ballobj = Ball()

    def clearPoints(self):
        self.p1.score = 0
        self.p2.score = 0
        self.ballobj = Ball()

    def addPointP1(self):
        self.p1.score += 1

    def addPointP2(self):
        self.p2.score += 1
