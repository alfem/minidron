#!/usr/bin/python
# -*- coding: utf8 -*-

import festival

class Synthesizer:
    '''
    Speech Synthesizer for notifications (when no screen available) and user interface
    switched from espeak to festival
    '''
    def __init__(self):
      festival.setStretchFactor(1) # voice speed, 0 (fast) to 5 (slow), 
      return

    def say(self,text):
      festival.sayText(text)

    def close(self):
      return
   
