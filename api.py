#!/usr/bin/env python

# Provides the following APIs:
# 1. /RecentFinishers - Finishers in the last x seconds
# 2. /LastFinishers - The last x finishers
# 3. /ClassResults - The current results by class
# 4. /EntryList - The entry list including car number, name, vehicle and class


import datetime
import MySQLdb #apt-get install python-mysqldb
from flask import Flask, render_template, jsonify # pip install flask

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
	print(e)

app = Flask(__name__)
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/RecentFinishers/<seconds>')
def recentfinishers(seconds):
	cur = conn.cursor()
	cur.execute('''SELECT Car,SixtyFour,Split,Finish FROM RawResults WHERE (TimeOfDay > (NOW() - INTERVAL %s SECOND)) ORDER BY TimeOfDay Desc;''' % (str(seconds)))
	recentfew=cur.fetchall()
	conn.commit()
	return jsonify(recentfew)
		
@app.route('/LastFinishers')
def lastfinishers():
	# Return last x cars
	numberoffinishers=2
	cur = conn.cursor()
	cur.execute('''SELECT Car,SixtyFour,Split,Finish FROM RawResults order by TimeOfDay Desc limit %s;''' % (str(numberoffinishers)))
	lastfew=cur.fetchall()
	conn.commit()
	return jsonify(lastfew)
	
	#Set variables to display first item returned (messy and doesn't scale)
#	carno1=lastfew[0][0]
#	sixtyfour1=lastfew[0][1]
#	split1=lastfew[0][2]
#	finish1=lastfew[0][3]
#

#	return render_template('lastfinishers.html',carno1=carno1,driver1=driver1,car1=car1,sixtyfour1=sixtyfour1,split1=split1,finish1=finish1,numberoffinishers=numberoffinishers)

@app.route('/AllClassResults')
def allclassresults():
	cur = conn.cursor()
	cur.execute('''SELECT * FROM ClassResults;''')
	currentresults=cur.fetchall()
	conn.commit()
	return jsonify(currentresults)

@app.route('/AllClassResults/<thisclass>')
def thisallclassresults(thisclass):
	cur = conn.cursor()
	cur.execute('''SELECT * FROM (SELECT Car,Least(COALESCE(Timed1,Timed2),COALESCE(Timed2,Timed1),COALESCE(Timed3,Timed1),COALESCE(Timed4,Timed1)) AS Best from ClassResults where Class = %s order by Best) As Dave WHERE Best > 0;''' % ("'"+str(thisclass)+"'"))
	thisclassresults=cur.fetchall()
	conn.commit()
	position = 1
	driver = "tbc"  # TBC - establish driver and car
	car = "tbc"  # TBC - establish driver and car
	stilltorun = []
	tabularresults=[]
	for thisresult in thisclassresults:
		# Find driver/car
		cur.execute('''SELECT Driver,MakeModel,Class FROM Entries WHERE Car=%s;''' % ("'"+str(thisresult[0])+"'"))
		entry=cur.fetchone()
		driver=entry[0]  #Breaks if no car in entry list
		car=entry[1]
	
		# Add row to table
		if thisresult[1]:
			thislist = [position,driver,car,str(thisresult[1])]
			tabularresults.append(list(thislist))
			position = position + 1
		else:
			thislist = ["",driver,car,str(thisresult[1])]
			stilltorun.append(list(thislist))
	conn.commit()
	tabularresults += stilltorun
	return render_template('classresults.html',rows=tabularresults,thisclass=thisclass)

@app.route('/EntryList')
def entrylist():
	cur = conn.cursor()
	cur.execute('''SELECT * FROM Entries;''')
	entries=cur.fetchall()
	conn.commit()
	return jsonify(entries)

@app.route('/ClassResults/<myclass>')
def classresults(myclass):
	rightnow = datetime.datetime.now()
	thistime='00:00:00'
	timestampstring = str(rightnow.year) + '-0' + str(rightnow.month) + '-' + str(rightnow.day) + ' ' + thistime
	cur = conn.cursor()
	print timestampstring
	cur.execute('''select Entries.Driver, class, RawResults.Car, min(Finish) AS Best From RawResults INNER JOIN Entries on Entries.Car = RawResults.Car WHERE timeofday > '%s' and class = '%s' GROUP BY RawResults.Car Order by Best limit 12;''') ,(timestampstring,myclass[0]+myclass[1])
	print ('''select Entries.Driver, class, RawResults.Car, min(Finish) AS Best From RawResults INNER JOIN Entries on Entries.Car = RawResults.Car WHERE timeofday > '%s' and class = '%s' GROUP BY RawResults.Car Order by Best limit 12;''') ,(timestampstring,myclass[0]+myclass[1])
	results = cur.fetchall()
	conn.commit()
	return jsonify(results)

@app.route('/RunOff')
def RunOff():
	cur = conn.cursor()
	cur.execute('''select Entries.Driver, class, RawResults.Car, min(Finish) AS Best From RawResults INNER JOIN Entries on Entries.Car = RawResults.Car WHERE timeofday > '2021-08-01 16:07:00' and finish >0 GROUP BY RawResults.Car Order by Best limit 12;''') 
	results = cur.fetchall()
	conn.commit()
	return jsonify(results)

@app.route('/T1Results')
def T1results():
	cur = conn.cursor()
	cur.execute('''select Entries.Driver, class, RawResults.Car, min(Finish) AS Best From RawResults INNER JOIN Entries on Entries.Car = RawResults.Car WHERE timeofday > '2021 07 31 10:00:00' and class = 'T1' GROUP BY RawResults.Car Order by Best limit 12;''') 
	results = cur.fetchall()
	conn.commit()
	return jsonify(results)

@app.route('/T2Results')
def T2results():
	cur = conn.cursor()
	cur.execute('''select Entries.Driver, class, RawResults.Car, min(Finish) AS Best From RawResults INNER JOIN Entries on Entries.Car = RawResults.Car WHERE timeofday > '2021 07 31 10:00:00' and class = 'T2' GROUP BY RawResults.Car Order by Best limit 12;''') 
	results = cur.fetchall()
	conn.commit()
	return jsonify(results)

@app.route('/T3Results')
def T3results():
	cur = conn.cursor()
	cur.execute('''select Entries.Driver, class, RawResults.Car, min(Finish) AS Best From RawResults INNER JOIN Entries on Entries.Car = RawResults.Car WHERE timeofday > '2021 07 31 10:00:00' and class = 'T3' GROUP BY RawResults.Car Order by Best limit 12;''') 
	results = cur.fetchall()
	conn.commit()
	return jsonify(results)
	
@app.route('/T4Results')
def T4results():
	cur = conn.cursor()
	cur.execute('''select Entries.Driver, class, RawResults.Car, min(Finish) AS Best From RawResults INNER JOIN Entries on Entries.Car = RawResults.Car WHERE timeofday > '2021 07 31 10:00:00' and class = 'T4' GROUP BY RawResults.Car Order by Best limit 12;''') 
	results = cur.fetchall()
	conn.commit()
	return jsonify(results)



if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')
