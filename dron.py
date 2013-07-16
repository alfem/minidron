#!/usr/bin/python
# -*- coding: utf8 -*-

# dron

# Author: Alfonso E.M.
# License: Free (GPL) 
# Version: 1.0 - 29/Jun/2010

import pygame
from pygame.locals import *
import random
import time
import sys

from face.face import *
from voice.voice import *
from arduino.servo import *
from sensors.wifi import *
from sensors.battery import *

import curses


arduino=Arduino("/dev/ttyUSB0")
wifi="wlan0"
battery="BAT0"

# Typical netbook resolution
resolution=1024,600

pygame.display.init()
pygame.mouse.set_visible(0)
screen=pygame.display.set_mode(resolution)

face=Face(resolution)



def sayandmove(text2say):
        say(text2say)
        for n in range(0,len(text2say)):
          if text2say[n] in 'aeiou':
            face.mouth.draw(screen,text2say[n])
            time.sleep(.20)
        face.mouth.draw(screen,"base")


def prompttext():
        textscreen.addstr(16,0," SAY [RETURN]:",curses.A_REVERSE)
        textscreen.nodelay(0)
        text2say=textscreen.getstr(16,14)
        textscreen.nodelay(1)
        textscreen.addstr(16,0," SAY [RETURN]:")
        textscreen.addstr(17,20,text2say)
        textscreen.refresh()
        sayandmove(text2say)
        return text2say

        
# BUCLE PRINCIPAL

textscreen = curses.initscr()
textscreen.addstr(" BATTERY:                        WIFI:")
textscreen.addstr( 2,0," MOVE:      <-ARROWS->           STOP:  SPACEBAR")

textscreen.addstr( 4,0,"             \   /                /   \     _   _")     
textscreen.addstr( 5,0," FACES       O   O      O   O     O   O     O   O")
textscreen.addstr( 6,0,"             _____        o        ___      _____")
textscreen.addstr( 7,0,"              [a]        [s]       [d]       [f]")

textscreen.addstr( 9,0," BLINK      O   -      -   -     -   O")
textscreen.addstr(10,0,"            _____      _____     _____")
textscreen.addstr(11,0,"             [q]        [e]       [r] ")

textscreen.addstr(13,0," LOOK      <O   O      O   O     O   O>")
textscreen.addstr(14,0,"             [z]        [x]       [c] ")

textscreen.addstr(16,0," SAY [RETURN]:")
textscreen.addstr(17,0," REPEAT [BACKSPACE]:")

last_text=""
last_blink=time.clock()
last_sensors=time.clock()
battery_capacity=get_battery_capacity(battery)

while 1:

#Refresh wifi and battery indicators
  if time.clock()-last_sensors > 5:

     x=get_battery_level()
     x=x*100/battery_capacity 

     if x > 0:
       x=int(x/10)
       indicator="||||||||||"[0:x]+".........."[0:10-x]   
     else:
       indicator="OFF"
     textscreen.addstr(0,9,indicator)

     x=get_wifi_level()
     if x > 0:
       x=int(x/10)
       indicator="||||||||||"[0:x]+".........."[0:10-x]   
     else:
       indicator="OFF"
     textscreen.addstr(0,38,indicator)

     last_sensors=time.clock()

#Blink randomly
  if time.clock()-last_blink > 2:
    if random.randint(0,100000) == 1:
      face.blink_both()
      last_blink=time.clock()

  
# Control por teclas
  textscreen.nodelay(1)
  textscreen.keypad(1)
#  curses.noecho()
#  curses.cbreak()
  textscreen.move(19,0)
  key = textscreen.getch()

  if key != -1:
    if key == K_ESCAPE:
        curses.endwin()
        pygame.quit()	
        sys.exit(0)
    if key == ord(" "):
        textscreen.addstr("Brakes !!")
        arduino.stopall()    
    if key == curses.KEY_UP:
        textscreen.addstr("Forward >>")
        arduino.forward()
    if key == curses.KEY_DOWN:
        textscreen.addstr("Backward <<")
        arduino.backward()
    if key == curses.KEY_LEFT:
        textscreen.addstr("Left")
        arduino.left()
    if key == curses.KEY_RIGHT:
        textscreen.addstr("Right")
        arduino.right()
    if (key == 10):
        last_text=prompttext()
    if (key == curses.KEY_BACKSPACE and last_text != ""):
        textscreen.addstr(17,20,last_text)
        textscreen.refresh()
        sayandmove(last_text)
        
    if (key == K_z):
        face.look_left()
    if (key == K_c):
        face.look_right()
    if (key == K_q):
        face.blink_left()
    if (key == K_e):
        face.blink_right()
    if (key == K_w):
        face.blink_both()

    if (key == K_f):
       face.mouth.draw(screen,"base")
    if (key == K_s):
       face.surprise()
    if (key == K_d):
       face.sad()
    if (key == K_a):
       face.angry()
    if (key == K_g):
       face.mouth.draw(screen,"smile")

     
