#!/usr/bin/env python

import time
import serial
import MySQLdb #apt-get install python-mysqldb

# BUGS
# Doesn't do Timed4

# Initialise serial interface
ser = serial.Serial (
	port='/dev/ttyS0',
	baudrate=1200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

# Connect to MySQL
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

# Update results table
def UpdateResults(carno="",ftime="",rs=""):
	# Establish the class for the car
	cur.execute('''SELECT * FROM Entries WHERE Car=%s;''' % ("'"+carno+"'"))
	entry=cur.fetchone()
	vclass=entry[5]
	
	# Get results so far
	cur.execute('''SELECT * FROM ClassResults WHERE Car=%s;''' % ("'"+carno+"'"))
	if cur.rowcount:
		results=cur.fetchone()
		if rs=="FAIL":	# set a FAIL to 999 seconds for easy querying
			ftime="999.999"
		RunColumns=["","Practice1","Practice2","Timed1","Timed2","Timed3","Timed4"]
		for x in range(1,7):
			if results[x] is None:
				print " Recording run "+str(x)+" ... Car: "+str(results[0])+"    Time: "+str(ftime)
				# Update the first empty column in the row for that car
				cur.execute('''UPDATE ClassResults SET %s = %s WHERE Car = '%s';''' % (RunColumns[x],ftime,carno))
				break
	else:
		print "First run ... Car: "+carno+"    Time: "+ftime
		cur.execute('''INSERT INTO ClassResults(Car,Practice1,Class) VALUES(%s,%s,%s);''',(carno,ftime,vclass))
		print "no results yet"

# Record the raw result
def RecordFinish(result):
	# Initialise variables
	carnumber=""
	sixtyfour=""
	splittime=""
	finishtime=""
	runstate=""
	
	# Find car number and finish time from first line of text
	carnumber=result.split("Car: ")[1].split(" ")[0]
	finishtime=result.split("Time: ")[1].split("\r")[0]
	
	# Read secxond line of text
	x=ser.readline()
	# Find s=64 foot and split times from second line of text
	sixtyfour=x.split("  ")[1].split(" ")[0]
	splittime=x.split("  ")[2].split("\r")[0]
	# Deal with failed runs
	if finishtime == "NTR": # change this for what is expected to be a RERUN
		print "No time recorded: re-run expected"
		finishtime="999.999"
		runstate="RERUN"
	elif finishtime == "Red Flag": # Change this for what is expected to be a FAIL
		print "No time recorded: failed run"
		finishtime="999.999"
		runstate="FAIL"
		UpdateResults(carnumber,finishtime,runstate) # update the results table with a FAIL
	else:
		runstate="Normal"
		UpdateResults(carnumber,finishtime,runstate) # Update the results table with time
	print "#"+carnumber+"#"+sixtyfour+"#"+splittime+"#"+finishtime+"#"
	
	# Record raw results in the SQL table
	cur.execute('''INSERT INTO RawResults(Car,SixtyFour,Split,Finish,RunState) VALUES(%s,%s,%s,%s,%s);''',(carnumber,sixtyfour,splittime,finishtime,runstate))
	conn.commit()

# Just keep looping...
while 1:
	# Read a line of text from the serial interface
	x=ser.readline()
	
	# If this line has the car number, record the results
	if "Car:" in x:
		RecordFinish(x)
#	if "End of Batch" in x:
#		UpdateResults()