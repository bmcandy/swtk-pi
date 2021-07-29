#!/usr/bin/env python

import time
import serial
import random
import MySQLdb #apt-get install python-mysqldb

ser = serial.Serial (
	port='/dev/ttyS0',
	baudrate=1200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

f = open("serialoutput.txt", "w")

try:
	conn = MySQLdb.connect(
		user="Results",
		passwd="Results",
		host="localhost",
		port=3306,
		db="SpeedOnScreen"
	)
except MySQLdb.Error as e:
	print(e)

while 1:
	cur = conn.cursor()
	cur.execute('''SELECT Car FROM Entries;''')
	entries=cur.fetchall()
	conn.commit()
	randomentry = random.randint(0,len(entries)-1)
	car = str(''.join(entries[randomentry]))
#	if random.randint(1,20) == 1:
#		car = car + "A"
	finish = str(random.randint(34,63)) + "." + str(random.randint(10,99))
	if random.randint(1,40) == 1:
		finish = "NTR"
	if random.randint(1,100) == 1:
		finish = "Red Flag"
	if random.randint(1,100) > 1:
		sixfour = str(random.randint(2,4)) + "." + str(random.randint(10,99))
		splittime = str(random.randint(22,28)) + "." + str(random.randint(10,99))
		print "Car: %s  Time: %s\r\n  %s  %s\r\n\nxxx\n"%(car,finish,sixfour,splittime)
		ser.write("Car: %s  Time: %s\r\n  %s  %s\r\n\nxxx\n"%(car,finish,sixfour,splittime))
		f.write("Car: %s  Time: %s\r\n  %s  %s\r\n\nxxx\n"%(car,finish,sixfour,splittime))
	else:
		print "no split time"
	interval = random.randint(2,5)
#	interval = random.randint(22,30)
	print "waiting %d seconds"%(interval)
	time.sleep(interval)
	if random.randint(1,20) == 1:
		ser.write("End of Batch\n")
		f.write("End of Batch\n")
		endbatch=random.randint(300,600)
		print "End of batch.  Sleeping %d seconds"%(endbatch)
		#time.sleep(endbatch)
