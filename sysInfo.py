#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import time
import json

class SYS_INFO():
	def get_ram(self):
		try:
			s = subprocess.check_output(["free","-m"])
			lines = s.split('\n')
			data =[int(lines[1].split()[2]), int(lines[1].split()[3]), int(lines[3].split()[1]), int(lines[3].split()[2])]
			return data
		except:
			return None

	def get_process_count(self):
		try:
			s = subprocess.check_output(["ps","-e"])
			return len(s.split('\n'))        
		except:
			return None
	
	def get_cpu_load(self):
		try:
			last_idle = last_total = 0
			with open('/proc/stat') as f:
				fields = [float(column) for column in f.readline().strip().split()[1:]]
			idle, total = fields[3], sum(fields)
			idle_delta, total_delta = idle - last_idle, total - last_total
			last_idle, last_total = idle, total
			utilisation = 100.0 * (1.0 - idle_delta / total_delta)
			return "%.2f" % utilisation
		except:
			return None

	def get_up_stats(self):
		try:
			data = [None, None]
			s = subprocess.check_output(["uptime"])
			load_split = s.split('load average: ')
			load_five = float(load_split[1].split(',')[1])
			up = load_split[0]
			up_pos = up.rfind(',',0,len(up)-4)
			up = up[:up_pos].split('up ')[1]
			data[0] = up
			data[1] = load_five
			return data
		except:
			return None
		
	def get_temperature(self):
		try:
			s = subprocess.check_output(["/opt/vc/bin/vcgencmd","measure_temp"])
			return float(s.split('=')[1][:-3])
		except:
			return None
		
	def get_disk_info(self):
		try:
			s = subprocess.check_output(['df', '-h', '-T'])
			lines = s.split('\n')
			par_home = filter(lambda x: 'ext4' in x, lines)
			par_boot = filter(lambda x: 'vfat' in x, lines)
			return [str(par_home), str(par_boot)]
		except:
			return None
	def get_partion_table(self):
		try:
			s = subprocess.check_output(['df', '-h', '-T'])
			lines = s.split('\n')
			return lines
		except:
			return None

	#returns current speed in kB/s format: rx, tx, ip
	def get_network_stats(self, interface):
		try:
			rx_bytes0 = int(subprocess.check_output(["cat", "/sys/class/net/"+interface+"/statistics/rx_bytes"]))
			tx_bytes0 = int(subprocess.check_output(["cat", "/sys/class/net/"+interface+"/statistics/tx_bytes"]))
			time.sleep(1)
			rx_bytes1 = int(subprocess.check_output(["cat", "/sys/class/net/"+interface+"/statistics/rx_bytes"]))
			tx_bytes1 = int(subprocess.check_output(["cat", "/sys/class/net/"+interface+"/statistics/tx_bytes"]))

			rx_bytesPS = rx_bytes1 - rx_bytes0
			rx_kbytesPS = rx_bytesPS / 1024

			tx_bytesPS = tx_bytes1 - tx_bytes0
			tx_kbytesPS = tx_bytesPS / 1024
			ip = str(subprocess.check_output(["hostname", "-I"]))
			ip = ip.split('\n')
			sysInfo = [rx_kbytesPS, tx_kbytesPS, ip[0]]
			return sysInfo
		except:
			return None

	def generate_basicInfo_json(self, network_interface):
		try:
			cpuTemp = self.get_temperature()
			ramStats = self.get_ram()
			upStats = self.get_up_stats()
			diskStats = str(self.get_disk_info())
			cpuLoad = self.get_cpu_load()
			net_info = self.get_network_stats(network_interface)
			data_json = {'cpuLoad': cpuLoad,
						'cpuTemp': cpuTemp,
						'freeRam': ramStats[1],
						'usedRam':ramStats[0],
						'totalRam': ramStats[0]+ramStats[1],
						'totalSwap': ramStats[2],
						'usedSwap': ramStats[3],
						'upTime': upStats[0],
						'load5': upStats[1],
						'homeFree': diskStats.split()[4],
						'homeUsed': diskStats.split()[3],
						'homeTotal': diskStats.split()[2],
						'rx_bytesPS': net_info[0],
						'tx_bytesPS': net_info[1],
						'ip': net_info[2]
						}

			with open("systemInfo.json", "w") as outfile:
				data = json.dumps(data_json, indent=4, skipkeys=True, sort_keys=True)
				outfile.write(data)
				outfile.close()
		except:
			return None
	def generate_partionTable_json(self):
		try:
			table = self.get_partion_table()
			self.filesystem = [None]*(len(table)-1)
			self.type = [None]*(len(table)-1)
			self.size = [None]*(len(table)-1)
			self.used = [None]*(len(table)-1)
			self.avail = [None]*(len(table)-1)
			self.usedP = [None]*(len(table)-1)
			self.location = [None]*(len(table)-1)
			for i in range(len(table)-1):
				self.filesystem[i] = table[i].split()[0]
				self.type[i] = table[i].split()[1]
				self.size[i] = table[i].split()[2]
				self.used[i] = table[i].split()[3]
				self.avail[i] = table[i].split()[4]
				self.usedP[i] = table[i].split()[5]
				self.location[i] = table[i].split()[6]
			data_json = {'filesystem': self.filesystem,
						 'type': self.type,
						 'size': self.size,
						 'used': self.used,
						 'avail': self.avail,
						 'usedP': self.usedP,
						 'location': self.location
						}

			with open("partionTable.json", "w") as outfile:
				data = json.dumps(data_json, indent=4, skipkeys=True, sort_keys=True)
				outfile.write(data)
				outfile.close()
		except:
			return None
