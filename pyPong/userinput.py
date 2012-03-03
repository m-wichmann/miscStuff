#!/usr/bin/python
import pygame
import sys

class UserInput(object):

    def __init__(self):
        # 0 no menu/running game
        # 1 main menu
        # 2 options
        # 3 new game menu
        # 4 pause menu 
        self.state = 0

        # highlighted field in menu
        self.field = 0

        self.up_pressed = False
        self.down_pressed = False
        self.w_pressed = False
        self.s_pressed = False
        self.m_pressed = False
        self.n_pressed = False
        

    def checkEvents(self, event):
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_UP:
                self.up_pressed = True
            if event.key == pygame.K_DOWN:
                self.down_pressed = True
            if event.key == pygame.K_w:
                self.w_pressed = True
            if event.key == pygame.K_s:
                self.s_pressed = True
            if event.key == pygame.K_n:
                self.n_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.up_pressed = False
            if event.key == pygame.K_DOWN:
                self.down_pressed = False
            if event.key == pygame.K_w:
                self.w_pressed = False
            if event.key == pygame.K_s:
                self.s_pressed = False
            if event.key == pygame.K_n:
                self.n_pressed = False















