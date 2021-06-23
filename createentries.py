#!/usr/bin/env python

import time
import serial
import MySQLdb #apt-get install python-mysqldb

try:
	conn = MySQLdb.connect(
		user="Results",
		passwd="Results",
		host="localhost",
		port=3306,
		db="SpeedOnScreen"
	)
except MySQLdb.Error as e:
	print e
cur = conn.cursor()

for x in range(1,200):
	cur.execute('''INSERT INTO Entries(Car,Driver,MakeModel,Capacity,Category,Class) VALUES(%s,%s,%s,%s,%s,%s);''',(str(x)+"A","Driver A"+str(x),"Ford Focus",str(x*10),"Libre",str(round(x/10,0))))
	conn.commit()
