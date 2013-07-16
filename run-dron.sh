#!/bin/sh

#set speaker level

amixer sset Master Playback Volume  100%

mjpg_streamer -i "input_uvc.so -d /dev/video0 -y -r 320x240 -f 10" -o "output_http.so -w /home/brain/minidron/www -p 8080" --background

#run the dron
export DISPLAY=0:0; 
sudo ./dron.py

#reset screen
reset

killall mjpg_streamer
