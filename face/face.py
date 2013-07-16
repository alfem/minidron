#!/usr/bin/python
# -*- coding: utf8 -*-

# face

# Face of a dron
# Author: Alfonso E.M.
# License: Free (GPL) 
# Version: 1.0 - 29/Jun/2010

import pygame
from pygame.locals import *
import time

from eye import Eye
from mouth import Mouth


class Face:
  def __init__(self,resolution,color=(0, 0, 0)):

    self.screen=pygame.display.set_mode(resolution)

    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill(color)

    center_x=self.background.get_width()/2

    self.left_eye=Eye(center_x-250,250)
    self.right_eye=Eye(center_x+250,250)
    self.mouth=Mouth(center_x,500)

    self.draw()

  def draw(self):
    self.screen.blit(self.background,(0,0))
    self.left_eye.draw(self.screen)
    self.right_eye.draw(self.screen)
    self.mouth.draw(self.screen)
    pygame.display.flip()

  
  def surprise(self):
    self.left_eye.draw(self.screen,"up")
    self.right_eye.draw(self.screen,"up")
  def sad(self):
    self.left_eye.draw(self.screen,"brownleft")
    self.right_eye.draw(self.screen,"brownright")
  def angry(self):
    self.left_eye.draw(self.screen,"brownright")
    self.right_eye.draw(self.screen,"brownleft")
  def look_left(self):
    self.left_eye.draw(self.screen,"left")
    self.right_eye.draw(self.screen,"left")
  def look_right(self):
    self.left_eye.draw(self.screen,"right")
    self.right_eye.draw(self.screen,"right")
  def blink_left(self):
    self.left_eye.blink(self.screen)
  def blink_right(self):
    self.right_eye.blink(self.screen)
  def close_both(self):
    self.left_eye.draw(self.screen,"close")
    self.right_eye.draw(self.screen,"close")
  def open_both(self):
    self.left_eye.status="open"
    self.right_eye.status="open"
    self.left_eye.draw(self.screen)
    self.right_eye.draw(self.screen)
  def blink_both(self):
    self.close_both()
    time.sleep(0.10)
    self.open_both()
