#!/usr/bin/python

# Servo control in python

import serial

class Arduino:
  """
  Arduino serial (USB) class
  """
  def __init__(self,port="/dev/ttyUSB0"):

    try:
        self.conn = serial.Serial(port,9600,timeout=1,parity='N',stopbits=1,xonxoff=0,rtscts=0)  # open first serial port
    except: 
        print "ERROR: No Arduino detected!"    
        
# Servo pins in Arduino
    self.servo={}
    self.servo["left"]=Servo(1,"a","z")
    self.servo["right"]=Servo(7,"s","x")
    self.stop=" "
      
  def forward(self,servo=""):
    if servo == "left":
       self.conn.write(self.servo[servo].forward)
    elif servo == "right":
       self.conn.write(self.servo[servo].forward)
    else:
       self.forward("left")
       self.forward("right")
    
  def backward(self,servo=""):
    if servo == "left":
       self.conn.write(self.servo[servo].backward)
    elif servo == "right":
       self.conn.write(self.servo[servo].backward)
    else:
       self.backward("left")
       self.backward("right")
 
  def left(self):
    self.backward("right")
    self.forward("left")
    
  def right(self):
    self.backward("left")
    self.forward("right")

  def stopall(self):
      self.conn.write(self.stop)


class Servo:
  """ 
  Servo dummy class 
  """
  def __init__(self,pin,forward,backward):
    self.pin=pin
    self.forward=forward
    self.backward=backward
    