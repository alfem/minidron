#!/usr/bin/python


def get_battery_capacity(bat="BAT0"):

  try:
    f = open('/proc/acpi/battery/'+bat+'/info')
    lines = f.readlines()
    f.close()
  except IOError:
    return -1

  val=-2

  for l in lines:
    item = l.split(":")
    if item[0] == "last full capacity":
      val,unit = item[1].split()
      val = int(val)
  return val

def get_battery_level(bat="BAT0"):

  try:
    f = open('/proc/acpi/battery/'+bat+'/state')
    lines = f.readlines()
    f.close()
  except IOError:
    return -1

  val=-2

  for l in lines:
    item = l.split(":")
    if item[0] == "remaining capacity":
      val,unit = item[1].split()
      val = int(val)
  return val


