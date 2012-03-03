#!/usr/bin/python
import random
import entity

class Logic(object):
    def __init__(self):
        pass

    def nextTurn(self, gameobj, userinputobj):
        if (userinputobj.up_pressed == True):
            gameobj.p2.paddleobj.up(5)
        if (userinputobj.down_pressed == True):
            gameobj.p2.paddleobj.down(5)
        if (userinputobj.w_pressed == True):
            gameobj.p1.paddleobj.up(5)
        if (userinputobj.s_pressed == True):
            gameobj.p1.paddleobj.down(5)
        if (userinputobj.n_pressed == True):
            gameobj.clearPoints()

        # calc ball position
        gameobj.ballobj.position_ball_x += gameobj.ballobj.velocity_ball_x
        gameobj.ballobj.position_ball_y += gameobj.ballobj.velocity_ball_y

        if (gameobj.ballobj.position_ball_y <= 0):
            gameobj.ballobj.velocity_ball_y = 2

        if (gameobj.ballobj.position_ball_y >= 350):
            gameobj.ballobj.velocity_ball_y = -2

        if (gameobj.ballobj.position_ball_x < 10):
            gameobj.addPointP2()
            gameobj.ballobj = entity.Ball()
        elif (gameobj.ballobj.position_ball_x >= 20 and gameobj.ballobj.position_ball_x < 30):
            if (gameobj.ballobj.position_ball_y >= gameobj.p1.paddleobj.position and gameobj.ballobj.position_ball_y < gameobj.p1.paddleobj.position + 55):
                gameobj.ballobj.velocity_ball_x = -gameobj.ballobj.velocity_ball_x
            
        if (gameobj.ballobj.position_ball_x > 580):
            gameobj.addPointP1()
            gameobj.ballobj = entity.Ball()
        elif (gameobj.ballobj.position_ball_x >= 565 and gameobj.ballobj.position_ball_x < 575):
            if (gameobj.ballobj.position_ball_y >= gameobj.p2.paddleobj.position and gameobj.ballobj.position_ball_y < gameobj.p2.paddleobj.position + 55):
                gameobj.ballobj.velocity_ball_x = -gameobj.ballobj.velocity_ball_x

        temp = random.random() * 100
        if (temp >= 98):
            gameobj.ballobj.velocity_ball_x = gameobj.ballobj.velocity_ball_x * 1.1
        temp = random.random() * 100
        if (temp >= 98):
            gameobj.ballobj.velocity_ball_y = gameobj.ballobj.velocity_ball_y * 1.1










