#!/usr/bin/env python

import time
import serial
import MySQLdb #apt-get install python-mysqldb
import csv

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

#for x in range(1,200):
#	cur.execute('''INSERT INTO Entries(Car,Driver,MakeModel,Capacity,Category,Class) VALUES(%s,%s,%s,%s,%s,%s);''',(str(x)+"A","Driver A"+str(x),"Ford Focus",str(x*10),"Libre",str(round(x/10,0))))
#	conn.commit()

with open('20210731-WiscombeEntries.csv') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar="|")
	for row in reader:
		print row
		cur.execute('''INSERT INTO Entries(Car,Driver,MakeModel,Capacity,Category,Class) VALUES(%s,%s,%s,%s,%s,%s);''',(str(row[1]),str(row[2]),str(row[5]),str(row[6]),"TBC",str(row[0])))
		conn.commit()
		
		
