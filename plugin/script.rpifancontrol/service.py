#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import xbmc
import xbmcaddon
import commands
import os
import subprocess
import shlex
from subprocess import Popen,PIPE,STDOUT,call

addon       	= xbmcaddon.Addon()
addonname 		= addon.getAddonInfo('name')
ADDONPATH       = addon.getAddonInfo('path')
TEMP            = "sudo cat /sys/class/thermal/thermal_zone0/temp | awk 'NR == 1 { print $1 / 1000}' | cut -c -4"
FANSTATUS       = commands.getoutput("sudo cat /sys/class/gpio/gpio23/value")
pinnumber       = addon.getSetting('pinnumber')
temp_run_fan    = addon.getSetting('temp_run_fan')
debugis         = addon.getSetting('debug')
ICON = os.path.join(ADDONPATH, 'icon.png')

#OPCJE URUCHAMIAJĄCE WENTYLATOR AUTOMATYCZNIE.

def zaladuj():
	os.popen('sudo chmod 777 /sys/class/gpio/export /sys/class/gpio/unexport')
	os.popen('sudo echo 23 > /sys/class/gpio/export')
	os.popen('sudo chmod 777 /sys/class/gpio/gpio23/direction')
	os.popen('sudo chmod 777 /sys/class/gpio/gpio23/value')
	os.popen('sudo echo "out" > /sys/class/gpio/gpio23/direction')
	os.popen('sudo chmod 777 /sys/class/gpio/gpio23/value')

def log(string):
    return xbmc.log('BMW RPI FAN: %s' % string, xbmc.LOGNOTICE)	

def note(heading, message = None, time = 5000):
    import xbmcgui
    xbmcgui.Dialog().notification(heading='%s' % heading, message='%s' % message if message else '', icon=ICON, time=time)
    log('BMW RPI FAN NOTIFICATION: "%s%s"' % (heading, ' - %s' % message if message else ''))

def info():
	xbmc.log("Ustawienia Załadowane Wentylatora: %s" % debugis, level=xbmc.LOGNOTICE)
	if debugis == 'true':
		note('Uruchamiam Kontrole Wentylatora')

def main():
	monitor = xbmc.Monitor()
	
	while not monitor.abortRequested():
		# Sleep/wait for abort for 10 seconds
		if monitor.waitForAbort(5):
			# Abort was requested while waiting. We should exit
			xbmc.executebuiltin('Notification(Ohh,Nie działa,5000,/script.hellow.world.png)')
			break
		GETFAN_STATUS   = commands.getoutput(TEMP)
		if debugis == 'true':
			xbmc.log("Temperatura Procesora: %s" % GETFAN_STATUS, level=xbmc.LOGNOTICE)
		os.popen('sudo chmod 777 /sys/class/gpio/gpio23/value')
		
		if GETFAN_STATUS <= '39.99':
			os.popen('sudo echo "0" > /sys/class/gpio/gpio%s/value' % pinnumber)
			
		if GETFAN_STATUS <= '49':
			os.popen('sudo echo "0" > /sys/class/gpio/gpio%s/value' % pinnumber)

		if GETFAN_STATUS >= '50':
			os.popen('sudo echo "1" > /sys/class/gpio/gpio%s/value' % pinnumber)

if __name__ == '__main__':
	zaladuj()
	info()
	main()
