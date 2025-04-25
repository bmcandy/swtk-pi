#!/usr/bin/env python3

# Provides the following APIs:
# 1. /RecentFinishers - Finishers in the last x seconds
# 2. /LastFinishers - The last x finishers
# 3. /ClassResults - The current results by class
# 4. /EntryList - The entry list including car number, name, vehicle and class

import datetime
import MySQLdb  # apt-get install python3-mysqldb
from flask import Flask, render_template, jsonify  # pip install flask
from dotenv import load_dotenv  # pip install python-dotenv
import os

# Load environment variables from .env
load_dotenv()

# Connect to MySQL using environment variables
try:
    conn = MySQLdb.connect(
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=3306,
        db=os.getenv("DB_NAME")
    )
except MySQLdb.Error as e:
    print(f"Database connection error: {e}")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/RecentFinishers/<int:seconds>')
def recentfinishers(seconds):
    cur = conn.cursor()
    query = '''
        SELECT Car, SixtyFour, Split, Finish 
        FROM RawResults 
        WHERE (TimeOfDay > (NOW() - INTERVAL %s SECOND)) 
        ORDER BY TimeOfDay DESC;
    '''
    cur.execute(query, (seconds,))
    recentfew = cur.fetchall()
    conn.commit()
    return jsonify(recentfew)

@app.route('/LastFinishers')
def lastfinishers():
    # Return last x cars
    numberoffinishers = 2
    cur = conn.cursor()
    query = '''
        SELECT Car, SixtyFour, Split, Finish 
        FROM RawResults 
        ORDER BY TimeOfDay DESC 
        LIMIT %s;
    '''
    cur.execute(query, (numberoffinishers,))
    lastfew = cur.fetchall()
    conn.commit()
    return jsonify(lastfew)

@app.route('/AllClassResults')
def allclassresults():
    cur = conn.cursor()
    cur.execute('SELECT * FROM ClassResults;')
    currentresults = cur.fetchall()
    conn.commit()
    return jsonify(currentresults)

@app.route('/AllClassResults/<thisclass>')
def thisallclassresults(thisclass):
    cur = conn.cursor()
    query = '''
        SELECT * FROM (
            SELECT Car, LEAST(
                COALESCE(Timed1, Timed2), 
                COALESCE(Timed2, Timed1), 
                COALESCE(Timed3, Timed1), 
                COALESCE(Timed4, Timed1)
            ) AS Best 
            FROM ClassResults 
            WHERE Class = %s 
            ORDER BY Best
        ) AS Dave 
        WHERE Best > 0;
    '''
    cur.execute(query, (thisclass,))
    thisclassresults = cur.fetchall()
    conn.commit()
    position = 1
    stilltorun = []
    tabularresults = []
    for thisresult in thisclassresults:
        # Find driver/car
        cur.execute('SELECT Driver, MakeModel, Class FROM Entries WHERE Car=%s;', (thisresult[0],))
        entry = cur.fetchone()
        driver = entry[0] if entry else "tbc"
        car = entry[1] if entry else "tbc"

        # Add row to table
        if thisresult[1]:
            thislist = [position, driver, car, str(thisresult[1])]
            tabularresults.append(thislist)
            position += 1
        else:
            thislist = ["", driver, car, str(thisresult[1])]
            stilltorun.append(thislist)
    conn.commit()
    tabularresults += stilltorun
    return render_template('classresults.html', rows=tabularresults, thisclass=thisclass)

@app.route('/EntryList')
def entrylist():
    cur = conn.cursor()
    cur.execute('SELECT * FROM Entries;')
    entries = cur.fetchall()
    conn.commit()
    return jsonify(entries)

@app.route('/ClassResults/<myclass>')
def classresults(myclass):
    rightnow = datetime.datetime.now()
    thistime = '00:00:00'
    timestampstring = f"{rightnow.year}-0{rightnow.month}-{rightnow.day} {thistime}"
    cur = conn.cursor()
    query = '''
        SELECT Entries.Driver, class, RawResults.Car, MIN(Finish) AS Best 
        FROM RawResults 
        INNER JOIN Entries ON Entries.Car = RawResults.Car 
        WHERE timeofday > %s AND class = %s 
        GROUP BY RawResults.Car 
        ORDER BY Best 
        LIMIT 12;
    '''
    cur.execute(query, (timestampstring, myclass))
    results = cur.fetchall()
    conn.commit()
    return jsonify(results)

@app.route('/RunOff')
def RunOff():
    cur = conn.cursor()
    query = '''
        SELECT Entries.Driver, class, RawResults.Car, MIN(Finish) AS Best 
        FROM RawResults 
        INNER JOIN Entries ON Entries.Car = RawResults.Car 
        WHERE timeofday > '2021-08-01 16:07:00' AND finish > 0 
        GROUP BY RawResults.Car 
        ORDER BY Best 
        LIMIT 12;
    '''
    cur.execute(query)
    results = cur.fetchall()
    conn.commit()
    return jsonify(results)

@app.route('/T1Results')
def T1results():
    cur = conn.cursor()
    query = '''
        SELECT Entries.Driver, class, RawResults.Car, MIN(Finish) AS Best 
        FROM RawResults 
        INNER JOIN Entries ON Entries.Car = RawResults.Car 
        WHERE timeofday > '2021-07-31 10:00:00' AND class = 'T1' 
        GROUP BY RawResults.Car 
        ORDER BY Best 
        LIMIT 12;
    '''
    cur.execute(query)
    results = cur.fetchall()
    conn.commit()
    return jsonify(results)

@app.route('/T2Results')
def T2results():
    cur = conn.cursor()
    query = '''
        SELECT Entries.Driver, class, RawResults.Car, MIN(Finish) AS Best 
        FROM RawResults 
        INNER JOIN Entries ON Entries.Car = RawResults.Car 
        WHERE timeofday > '2021-07-31 10:00:00' AND class = 'T2' 
        GROUP BY RawResults.Car 
        ORDER BY Best 
        LIMIT 12;
    '''
    cur.execute(query)
    results = cur.fetchall()
    conn.commit()
    return jsonify(results)

@app.route('/T3Results')
def T3results():
    cur = conn.cursor()
    query = '''
        SELECT Entries.Driver, class, RawResults.Car, MIN(Finish) AS Best 
        FROM RawResults 
        INNER JOIN Entries ON Entries.Car = RawResults.Car 
        WHERE timeofday > '2021-07-31 10:00:00' AND class = 'T3' 
        GROUP BY RawResults.Car 
        ORDER BY Best 
        LIMIT 12;
    '''
    cur.execute(query)
    results = cur.fetchall()
    conn.commit()
    return jsonify(results)

@app.route('/T4Results')
def T4results():
    cur = conn.cursor()
    query = '''
        SELECT Entries.Driver, class, RawResults.Car, MIN(Finish) AS Best 
        FROM RawResults 
        INNER JOIN Entries ON Entries.Car = RawResults.Car 
        WHERE timeofday > '2021-07-31 10:00:00' AND class = 'T4' 
        GROUP BY RawResults.Car 
        ORDER BY Best 
        LIMIT 12;
    '''
    cur.execute(query)
    results = cur.fetchall()
    conn.commit()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
