#!/usr/bin/python
# -*- coding: utf8 -*-

import festival

class Synthesizer:
    '''
    Speech Synthesizer for notifications (when no screen available) and user interface
    switched from espeak to festival
    '''
    def __init__(self):
      return

    def say(self,text):
      festival.say_text(text)

    def close(self):
      return
   
