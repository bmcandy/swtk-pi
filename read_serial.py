#!/usr/bin/env python

import time
import serial
import MySQLdb #apt-get install python-mysqldb
colcolour = "00c2cb"

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
	global colcolour
	# Establish the class for the car
	cur.execute('''SELECT * FROM Entries WHERE Car=%s;''' % ("'"+carno+"'"))
	if cur.rowcount:
		entry=cur.fetchone()
		vclass=entry[5]
		cur.execute('''SELECT Car,Best FROM (SELECT Car,Least(COALESCE(Timed1,Timed2),COALESCE(Timed2,Timed1),COALESCE(Timed3,Timed1),COALESCE(Timed4,Timed1)) AS Best from ClassResults where Class = %s order by Best) As Dave WHERE Best > 0 ORDER BY Best;''' % ("'"+str(vclass)+"'"))
		if cur.rowcount:
			classfastest = cur.fetchone()
		else:
			classfastest = ["Nobody", 999.999]
	else:
		print "unknown class"
		vclass = "Unknown"
		classfastest = ["Nobody", 999.999]
	
	# Get results so far
	cur.execute('''SELECT * FROM ClassResults WHERE Car=%s;''' % ("'"+carno+"'"))
	if cur.rowcount:
		results=cur.fetchone()
		if rs=="FAIL":	# set a FAIL to 999 seconds for easy querying
			ftime=999.999
		RunColumns=["","Practice1","Practice2","Timed1","Timed2","Timed3","Timed4"]
		fastest = 999.999
		for x in range(1,6):
			if results[x] is None:
				skip = 1
			else:
				if fastest > float(results[x]):
					fastest = float(results[x])
			if results[x] is None:
				print " Recording run "+str(x)+" ... Car: "+str(results[0])+"    Time: "+str(ftime)
				# Update the first empty column in the row for that car
				cur.execute('''UPDATE ClassResults SET {} = %s WHERE Car = %s;'''.format(RunColumns[x]),(ftime,carno))
				print repr(ftime)
				ftime = ftime.replace("\x00","")
				print "Values#This:"+str(ftime)+"#Best:"+str(fastest)+"#ClassBest:"+str(classfastest[1])+"#"
				#print "Types#This:"+str(type(ftime))+"#Best:"+str(type(fastest))+"#ClassBest:"+str(type(classfastest[1]))+"#"
				if ftime.replace('.','',1).isdigit():
					ftime = float(ftime)
				else:
					colcolour = "00c2cb"
					break
				#print str(type(ftime))
				if float(classfastest[1]) > float(ftime) and (classfastest[1]) < 999.99:

					print "\n\n*** Fastest ***\n\n"
					colcolour = "9e73f3"
				else:
					if float(ftime) < float(fastest):
						print "*** Improvement ***"
						colcolour = "7ed957"
					else:
						colcolour = "00c2cb"
				break

	else:
		print "First run ... Car: "+carno+"    Time: "+ftime
		cur.execute('''INSERT INTO ClassResults(Car,Practice1,Class) VALUES(%s,%s,%s);''',(carno,ftime,vclass))
		print "No results yet"

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
	#x=ser.readline()
	x=result.split("\r")[1]
	print "Result#"+x+"#"
	# Find s=64 foot and split times from second line of text
	sixtyfour=x.split("   ")[1].split(" ")[0]
	splittime=x.split("  ")[2].split("\r")[0]
	if len(sixtyfour) == 0:
		sixtyfour="0.00"
	# Deal with failed runs
	if finishtime == "NTR": # change this for what is expected to be a RERUN
		print "No time recorded: re-run expected"
		finishtime="999.999"
		runstate="RERUN"
	elif finishtime == "FAIL": # Change this for what is expected to be a FAIL
		print "No time recorded: Failed run"
		runstate="FAIL"
		UpdateResults(carnumber,finishtime,runstate) # update the results table with a FAIL
	elif finishtime == "Red Flag": # Change this for what is expected to be a RERUN
		print "No time recorded: re-run Expected"
		runstate="RERUN"
	else:
		runstate="Normal"
		UpdateResults(carnumber,finishtime,runstate) # Update the results table with time
	print "DBupdate#CarNo:"+carnumber+"#64:"+sixtyfour+"#split:"+splittime+"#Finish:"+finishtime+"#Colour:"+colcolour+"#\n"
	
	# Record raw results in the SQL table
	cur.execute('''INSERT INTO RawResults(Car,SixtyFour,Split,Finish,RunState,Colour) VALUES(%s,%s,%s,%s,%s,%s);''',(carnumber,sixtyfour,splittime,finishtime,runstate,colcolour))
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
