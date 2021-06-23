#!/usr/bin/env python

# Provides the following APIs:
# 1. /RecentFinishers - Finishers in the last x seconds
# 2. /LastFinishers - The last x finishers
# 3. /ClassResults - The current results by class
# 4. /EntryList - The entry list including car number, name, vehicle and class

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
	print e
cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/RecentFinishers/<seconds>')
def recentfinishers(seconds):
	cur.execute('''SELECT Car,SixtyFour,Split,Finish FROM RawResults WHERE TimeOfDay > NOW() - INTERVAL %s SECOND ORDER BY TimeOfDay Desc;''' % (str(seconds)))
	recentfew=cur.fetchall()
	return jsonify(recentfew)
		
@app.route('/LastFinishers')
def lastfinishers():
	# Return last x cars
	numberoffinishers=3
	cur.execute('''SELECT Car,SixtyFour,Split,Finish FROM RawResults order by TimeOfDay Desc limit %d;''' % (numberoffinishers))
	lastfew=cur.fetchall()
	return jsonify(lastfew)
	
	#Set variables to display first item returned (messy and doesn't scale)
#	carno1=lastfew[0][0]
#	sixtyfour1=lastfew[0][1]
#	split1=lastfew[0][2]
#	finish1=lastfew[0][3]
#
	# Find driver/car
#	cur.execute('''SELECT Driver,MakeModel,Class FROM Entries WHERE Car=%s;''' % ("'"+carno1+"'"))
#	entry=cur.fetchone()
#	class1=entry[2]  #Breaks if no car in entry list
#	driver1=entry[0]
#	car1=entry[1]

#	return render_template('lastfinishers.html',carno1=carno1,driver1=driver1,car1=car1,sixtyfour1=sixtyfour1,split1=split1,finish1=finish1,numberoffinishers=numberoffinishers)

@app.route('/ClassResults')
def classresults():
	cur.execute('''SELECT * FROM ClassResults;''')
	currentresults=cur.fetchall()
	return jsonify(currentresults)

@app.route('/EntryList')
def entrylist():
	cur.execute('''SELECT * FROM Entries;''')
	entries=cur.fetchall()
	return jsonify(entries)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')