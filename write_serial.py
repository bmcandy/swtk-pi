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
	# Select a random entry from the database
	cur = conn.cursor()
	cur.execute('''SELECT Car FROM Entries;''')
	entries=cur.fetchall()
	conn.commit()
	randomentry = random.randint(0,len(entries)-1)
	car = str(''.join(entries[randomentry]))
	# Add an "A" car that probably doesn't exist every ~20 cars
	if random.randint(1,20) == 1:
		print "Invalid car"
		car = car + "A"
	finish = str(random.randint(34,63)) + "." + str(random.randint(10,99))
	# Report car as no time recorded every ~40 cars
	if random.randint(1,40) == 1:
		print "NTR"
		finish = "NTR"
	# Report car as red flagged every ~100 cars
	if random.randint(1,100) == 1:
		print "Red Flag"
		finish = "Red Flag"
	# Generate a 64ft/split time 99% of the time
	if random.randint(1,100) > 1:
		sixfour = str(random.randint(2,4)) + "." + str(random.randint(10,99))
	else:
		print "No 64ft time"
	if random.randint(1,100) > 1:
		print "No split time"
		splittime = str(random.randint(22,28)) + "." + str(random.randint(10,99))
	print "Car: %s  Time: %s\r\n   %s  %s\r\n\nxxx\n"%(car,finish,sixfour,splittime)
	ser.write("Car: %s  Time: %s\r   %s  %s\rxxx"%(car,finish,sixfour,splittime))
	f.write("Car: %s  Time: %s\r\n   %s  %s\r\n\nxxx\n"%(car,finish,sixfour,splittime))
	# Wait until starting the next car
	interval = random.randint(2,5)	#2-5 seconds (fast testing)
#	interval = random.randint(22,30) # 22-30 seconds (realistic)
	print "waiting %d seconds"%(interval)
	time.sleep(interval)
	# Add end of batch every ~20 cars
	if random.randint(1,20) == 1:
		ser.write("End of Batch\n")
		f.write("End of Batch\n")
		endbatch=random.randint(300,600)
		print "End of batch.  Sleeping %d seconds"%(endbatch)
		#time.sleep(endbatch)
