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
import urllib

from face.face import *
from voice.voice import *
from arduino.servo import *
from sensors.wifi import *
from sensors.battery import *


# --- Some configurable parameters

PORT=80
arduino=Arduino("/dev/ttyUSB0")
wifi="wlan0"
battery="BAT0"
resolution=1024,600 # Typical netbook resolution

# --- End of configurable stuff

pygame.display.init()
pygame.mouse.set_visible(0)
screen=pygame.display.set_mode(resolution)

face=Face(resolution)

battery_level=0
wifi_level=0
q=Queue(100) # simple communication method between http server and main program


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
      response="OK;%i;%i;" % (battery_level, wifi_level)
 
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


def quit(signum, frame):
    print "Bye!"
    sys.exit(0)
        

# MAIN 

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


# MAIN LOOP
    while True:

# Refresh wifi and battery indicators every ten seconds (TODO)
      if time.clock()-last_sensors > 10:

         x=get_battery_level()
         x=x*100/battery_capacity 

         if x > 0:
           battery_level=int(x/10)
         else:
           battery_level=-1

         x=get_wifi_level()
         if x > 0:
           wifi_level=int(x/10)
         else:
           wifi_level=-1

         last_sensors=time.clock()

# Blink randomly
      if time.clock()-last_blink > 2:
        if random.randint(0,100000) == 1:
          face.blink_both()
          last_blink=time.clock()

 
# Actions received from web interface
      while not q.empty():
        items=urlparse(urllib.unquote(q.get()))
        action=items.path[1:]
        params=items.query

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
        elif (action == "sad"):
           face.sad()
        elif (action == "angry"):
           face.angry()
        elif (action == "smile"):
           face.mouth.draw(screen,"smile")

        elif (action == "photo"):
           face.photo.draw(screen, params)
           time.sleep(2)
           face.draw()


# TODO:
#            face.look_left()
#            face.look_right()
#            face.blink_left()
#            face.blink_right()
#            face.blink_both()
#            face.mouth.draw(screen,"base")
#            face.surprise()
         
