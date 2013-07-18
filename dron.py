#!/usr/bin/python
# -*- coding: utf8 -*-

# Minidron Web Control 

# Author: Alfonso E.M.
# License: Free (GPL) 
# Version: 2.0 - 16/Jun/2013

import pygame
from pygame.locals import *
import random
import time
import sys
import signal
import threading
from Queue import Queue

import BaseHTTPServer
import SocketServer
from urlparse import urlparse

from face.face import *
from voice.voice import *
from arduino.servo import *
from sensors.wifi import *
from sensors.battery import *

PORT=80
arduino=Arduino("/dev/ttyUSB0")
wifi="wlan0"
battery="BAT0"


# Typical netbook resolution
resolution=1024,600

pygame.display.init()
pygame.mouse.set_visible(0)
screen=pygame.display.set_mode(resolution)

face=Face(resolution)

q=Queue(100)

class dronHTTPServer():
  def __init__(self, ip, port):
        self.server = HTTPServer((ip,port), HTTPHandler)

  def start(self):
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()

class HTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
  """
HTTP MultiThread Server
"""
  pass


class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  """
HTTP Request Handler
"""
  def load_index(self,filename):
     f=open(filename)
     content=f.read()
     f.close()
     return content

  def do_GET(self):
    print self.path
    if self.path == "/":
      if not hasattr(self,"index"):
         self.index=self.load_index("remote.html") 
      response = self.index
    else:
      q.put(self.path)
      response="OK"
 
    self.send_response(200)
    self.send_header("Content-Length", str(len(response)))
    self.send_header("Cache-Control", "no-store")
    self.end_headers()
    self.wfile.write(response) 


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


def quit(signum, frame):
    print "Bye!"
    sys.exit(0)
        
# BUCLE PRINCIPAL

if __name__ == '__main__':

    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    print "Starting web server at port", PORT, "...",
    http_server = dronHTTPServer("",PORT)
    http_server.start()

    print "OK."

    last_text=""
    last_blink=time.clock()
    last_sensors=time.clock()
    battery_capacity=get_battery_capacity(battery)

    while True:

    #Refresh wifi and battery indicators
      if time.clock()-last_sensors > 5:

         x=get_battery_level()
         x=x*100/battery_capacity 

         if x > 0:
           x=int(x/10)
           indicator="||||||||||"[0:x]+".........."[0:10-x]   
         else:
           indicator="OFF"
    #     textscreen.addstr(0,9,indicator)

         x=get_wifi_level()
         if x > 0:
           x=int(x/10)
           indicator="||||||||||"[0:x]+".........."[0:10-x]   
         else:
           indicator="OFF"
    #     textscreen.addstr(0,38,indicator)

         last_sensors=time.clock()

    #Blink randomly
      if time.clock()-last_blink > 2:
        if random.randint(0,100000) == 1:
          face.blink_both()
          last_blink=time.clock()

      while not q.empty():
        items=urlparse(q.get())
        action=items.path[1:]
        params=items.query
      
# Actions received from web interface

        if params == "quit":
            pygame.quit()	
            sys.exit(0)
# Movement    
        elif action == "stop":
            arduino.stopall()    
        elif action == "forward":
            arduino.forward()
        elif action == "backward":
            arduino.backward()
        elif action == "left":
            arduino.left()
        elif action == "right":
            arduino.right()
        elif (action == "say"):
            sayandmove(params)
# Face Expressions            
        if (action == K_z):
            face.look_left()
        if (action == K_c):
            face.look_right()
        if (action == K_q):
            face.blink_left()
        if (action == K_e):
            face.blink_right()
        if (action == K_w):
            face.blink_both()

        if (action == K_f):
           face.mouth.draw(screen,"base")
        if (action == K_s):
           face.surprise()
        if (action == "sad"):
           face.sad()
        if (action == "angry"):
           face.angry()
        if (action == "smile"):
           face.mouth.draw(screen,"smile")

         
