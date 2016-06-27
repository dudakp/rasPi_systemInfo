#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, time
sys.path.append('/home/pi/Development/Python/Sensors/lib_htu21d')
#from db_logger import SQLITE_DB_LOGGER
#from lib_htu21d import HTU21D
from sysInfo import *

#htu = HTU21D()
info = SYS_INFO()

print info.get_network_stats("wlan0")
