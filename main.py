#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, time
sys.path.append('/home/pi/Development/Python/Sensors/lib_htu21d')
from db_logger import DB_LOGGER
#from lib_htu21d import HTU21D
from sysInfo import *

#htu = HTU21D()
info = SYS_INFO()

#print htu.readTemperatureData()
CPU_load = info.get_cpu_load()
used_RAM = str(info.get_ram()[0])
uptime = info.get_up_stats()[0]
rx_speed = str(info.get_network_stats("wlan2")[0])

print "CPU load: "+ CPU_load
print "Used RAM: "+ used_RAM
print "Uptime: "+ uptime
print "Current download speed in kB/s: "+ rx_speed

