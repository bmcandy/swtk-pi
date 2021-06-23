#!/usr/bin/env python

import time
import serial
import mysql.connector #pip install mysql-connector-python
#import mariadb #pip install mariadb

ser = serial.Serial (
	port='/dev/ttyS0',
	baudrate=1200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

#try:
#	conn = mariadb.connect(
#		user="Results",
#		password="Results",
#		host="localhost",
#		port=3306,
#		database="SpeedOnScreen"
#	)
#except mariadb.Error as e:
#	print e
#cur = conn.cursor()

while 1:
	x=ser.readline()
	if "Car:" in x:
		carnumber=x.split("Car: ")[1].split(" ")[0]
		finishtime=x.split("Time: ")[1].split("\r")[0]
		x=ser.readline()
		sixtyfour=x.split("  ")[1].split(" ")[0]
		splittime=x.split("  ")[2].split("\r")[0]
		if finishtime == "NTR":
			print("No time recorded: re-run expected")
		if finishtime == "Red Flag":
			print("No time recorded: failed run")
		print("#"+carnumber+"#"+sixtyfour+"#"+splittime+"#"+finishtime+"#")
		
