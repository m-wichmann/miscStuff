#!/usr/bin/python
import pygame
import entity
import userinput


class UI(object):
    def __init__(self, width, height):
        self.bgcolor = (0, 0, 0)
        self.fgcolor = (255, 255, 255)
        self.width = width
        self.height = height

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.bgcolor)

        self.frame_left = 25
        self.frame_right = 615
        self.frame_top = 100
        self.frame_bottom = 455

    def update(self, gameobj, userinputobj):

        self.screen.fill(self.bgcolor)

        pygame.draw.rect(self.screen, self.fgcolor, (25, 100, self.frame_right - self.frame_left, self.frame_bottom - self.frame_top),1)

        score_string = "Player 1: " + str(gameobj.p1.score) + "  Player 2: " + str(gameobj.p2.score)
        font = pygame.font.SysFont("Monospace", 38, True)
        ren = font.render(score_string, False, self.fgcolor)
        self.screen.blit(ren, (25, 25))

        # draw rect:
        # screen, color, (left, top, widht, height)

        # draw p1 paddle
        pygame.draw.rect(self.screen, self.fgcolor, (self.frame_left + 25, self.frame_top + gameobj.p1.paddleobj.position, gameobj.p1.paddleobj.width, gameobj.p1.paddleobj.height))
        # draw p2 paddle
        pygame.draw.rect(self.screen, self.fgcolor, (self.frame_right - 25, self.frame_top + gameobj.p2.paddleobj.position, gameobj.p2.paddleobj.width, gameobj.p2.paddleobj.height))
        # draw ball
        pygame.draw.rect(self.screen, self.fgcolor, (self.frame_left + gameobj.ballobj.position_ball_x, self.frame_top + gameobj.ballobj.position_ball_y, gameobj.ballobj.width, gameobj.ballobj.height))

        pygame.display.flip()







