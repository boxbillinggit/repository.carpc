#!/usr/bin/env python
# -*- coding: utf-8 -*-

#24.07.2017 - Jarosław 
#Tylko z 2N2222 TOS91

import xbmcaddon
import xbmcvfs
import xbmcgui
import xbmc
import os
import sys
import time
import socket
import commands
from datetime import datetime
from time import sleep
from subprocess import Popen,PIPE,STDOUT,call
		
#-------------------------Variablen & Spezialvariablen----------------------#
author 			= 'Jarek'
addon       	= xbmcaddon.Addon()
ADDON_ID 		= addon.getAddonInfo('id')
addonname 		= addon.getAddonInfo('name')

ADDON_PATH 		= addon.getAddonInfo('path')
ADDON_USERPATH 	= os.path.join(xbmc.translatePath('special://userdata'), 'addon_data', ADDON_ID)
JahrMonat		= datetime.now()

time = 5000 #ms fuer die dialogboxen

#Icons beim Start, Notifikation
iconServiceGelb	= os.path.join(ADDON_PATH,'resources', 'skins', 'Default','media','gelb.png')
iconServiceRot	= os.path.join(ADDON_PATH,'resources', 'skins', 'Default','media','rot.png')

ACTION_PREVIOUS_MENU = 92 # Backspace
ACTION_NAV_BACK = 10 # ESC
ACTION_SELECT_ITEM = 7
ACTION_LEFT  = 1
ACTION_RIGHT = 2
ACTION_UP    = 3
ACTION_DOWN  = 4

#----------------------MAIN---------------------#

def main(): 
	if not xbmcvfs.exists(ADDON_USERPATH):
		xbmcvfs.mkdir(ADDON_USERPATH)
	
class FensterXML(xbmcgui.WindowXML):
	#bttn codes
	HOCH_TASTE 		= 3
	RUNTER_TASTE 	= 4
	TEMP            = "sudo cat /sys/class/thermal/thermal_zone0/temp | awk 'NR == 1 { print $1 / 1000}' | cut -c -4"
	FANSTATUS       = "sudo cat /sys/class/gpio/gpio23/value"
	GETFAN_STATUS   = commands.getoutput(FANSTATUS)
	pinnumber       = "23"
	
	def GetTemp(self):
		res = Popen(self.TEMP, stdout=PIPE, stderr=PIPE, shell=True)
		out, error = res.communicate()

		if error:
			self.getControl( 101 ).setLabel(error+'Nie ma odczytu')
			self.msg('NIE mam jak sprawdzić')
		else:
			self.getControl( 101 ).setLabel(str(out)+' Stopni')
			self.msg('Sprawdziłem i wiem')
			
	def GetStatusFan(self):
		#out_fan = commands.getoutput(self.FANSTATUS)
		outtemp = self.GETFAN_STATUS

		if outtemp == '0':
			self.getControl( 103 ).setLabel('Wyłączony')
			self.getControl( 5005 ).setLabel("Włącz Wentylator")
		else:
			self.getControl( 103 ).setLabel('Włączony')
			self.getControl( 5005 ).setLabel("Wyłącz Wentylator")
	
	def setFanOnOff(self):
		os.popen('sudo chmod 777 /sys/class/gpio/gpio%s/value' % self.pinnumber)
		outtemp = self.GETFAN_STATUS
		if outtemp == '1':
			os.popen('sudo echo "0" > /sys/class/gpio/gpio%s/value' % self.pinnumber)
			xbmc.log("Status Wentylatora: %s" %self.GETFAN_STATUS, level=xbmc.LOGNOTICE)
			self.msg('Wyłączam Wentylator')
		else:
			os.popen('sudo echo "1" > /sys/class/gpio/gpio%s/value' % self.pinnumber)
			xbmc.log("Status Wentylatora: %s" %self.GETFAN_STATUS, level=xbmc.LOGNOTICE)
			self.msg('Włączam Wentylator')
	
	def onInit(self):
		#Deklarierung der großen Symbole links im Bild und in den Notifikationen
		self.getControl( 99 ).setLabel("BMW Fan Control")
		self.getControl( 100 ).setLabel("Aktualna Temperatura Procesora:")
		self.getControl( 102 ).setLabel("Wentylator Pracuje?:")

		self.GetTemp()
		self.GetStatusFan()
		
		self.BtnTMP = self.getControl(5005)
		self.setFocus(self.BtnTMP)
		#self.addControl(self.BtnTMP)
		
	def customAction(self):
		self.setFanOnOff()
		sleep(3)
		self.GetStatusFan()
		
	def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
		if action == ACTION_DOWN:
			self.setFocus(self.BtnTMP)

	def onClick(self, controlID):
		if controlID == 5005:
			self.customAction()
		if controlID == 105:
			xbmc.executebuiltin('Notification(Kliknięto,Ok wentylator włączam,5000,/script.hellow.world.png)')
			
	def onFocus(self, controlID):
		if (controlID == 5005):
			self.BtnTMP.setVisible(True)
		else:
			self.BtnTMP.setVisible(False)

	def onControl(self, control):
		self.message("Window.onControl(control=[%s])"%control)
			
	#focus schmeisst Exception raus, keine Ahnung was er hat, schein wohl ein problem mit der onFocus funktion selber zu sein, funktioniert dennoch
	#def onFocus(self, controlID):
	#OPCJE DODATKOWE
	def message(self, message):
		dialog = xbmcgui.Dialog()
		dialog.ok("Informacja", message)
		
	def msg(self, message):
		xbmc.executebuiltin('Notification(Temperatura,%s,2000,/script.hellow.world.png)'%message)
			
	#def onAction(self, action): #hat keinen nutzen fuer mich			

if __name__ == '__main__':
	main() #ok
	w = FensterXML("skin.xml", ADDON_PATH, 'Default', '720p') #ok
	w.doModal() #ok
	del w #ok