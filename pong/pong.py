#!/usr/bin/python
import pygame
import sys
import ui
import userinput
import logic
import entity

class Pong(object):
    def __init__(self, width, height):
        # init vars
        self.uiobj = ui.UI(width, height)
        self.userinputobj = userinput.UserInput()
        self.gameobj = entity.Game(entity.Player(), entity.Player())
        self.logicobj = logic.Logic()

        # update ui at start
        self.uiobj.update(self.gameobj, userinput)
  
    def event_loop(self):
        while True:
            # check events
            for event in pygame.event.get():
                self.userinputobj.checkEvents(event)

            # check if "special" events eccoured, such as a new game or something

            # check logic what happens next
            self.logicobj.nextTurn(self.gameobj, self.userinputobj)

            # update ui
            self.uiobj.update(self.gameobj, self.userinputobj)

            pygame.time.wait(25)


if __name__ == '__main__':
    p = Pong(640, 480)
    p.event_loop()
