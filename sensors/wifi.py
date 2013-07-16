#!/usr/bin/python


def get_wifi_level(iface="wlan0"):

  try:
    f = open('/proc/net/wireless')
    lines = f.readlines()  
    f.close()
  except IOError:
    return -1

  val=-2
  
  for l in lines[2:]:
    item = l.split()
    if item[0].rstrip(':') == iface:
      val = item[2]
      val = val.rstrip('. :')
      val = int(val)
  return val
