#!/usr/bin/python
# -*- coding: utf8 -*-

import speechd

class Synthesizer:
    '''
    Speech Synthesizer for notifications (when no screen available) and user interface
    '''
    def __init__(self):

      self.client=speechd.SSIPClient('minidron')

      print self.client.list_output_modules()
      print self.client.list_synthesis_voices()

      self.client.set_output_module("espeak")
      self.client.set_language("es")
      self.client.set_synthesis_voice("spanish")
      self.client.set_pitch(5)
      self.client.set_rate(5)
      self.client.set_punctuation(speechd.PunctuationMode.SOME)


    def say(self,text):
      self.client.speak(text)

    def close(self):
      self.client.close()
   
