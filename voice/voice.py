#!/usr/bin/python
# -*- coding: utf8 -*-

from subprocess import *

# Start a Festival TTS in pipe mode and let it running

festival = Popen(["festival","--pipe"], shell=True, stdin=PIPE).stdin

def say(text):

 text=unicode(text,'utf-8')
# text=text.encode("latin-1")
 festival_cmd='(SayText "%s")\n' % text
 print festival_cmd
 festival.write(festival_cmd)
