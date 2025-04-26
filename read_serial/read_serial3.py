#!/usr/bin/env python

import serial
import mysql.connector
from dotenv import load_dotenv  # pip install python-dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize serial interface
print("Initializing serial interface...")
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=1200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Connect to MySQL
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=3306,
            database=os.getenv("DB_NAME")
        )
        print("Connected to database")
        return conn
    except mysql.connector.Error as e:
        print(e)
        return None

conn = connect_to_database()
if conn:
    cur = conn.cursor()
    print("Database cursor created")

def speak_finish_time(car, driver, time, split, sixtyfour=None):
    """Function to speak the finish time of the driver."""
    message = f"Car number {car}"
    if driver:
        message += f" driven by {driver}"
    message += f" finished in {time} seconds"
    if split:
        message += f" with a split of {split} seconds"
    if sixtyfour:
        message += f" and a sixty four foot time of {sixtyfour} seconds"

    print(message)

# Update results table
def update_results(carno="", ftime="", rs=""):
    # Establish the class for the car
    cur.execute("SELECT * FROM Entries WHERE Car=%s", (carno,))
    if cur.rowcount:
        entry = cur.fetchone()
        vclass = entry[5]
        cur.execute(
            """SELECT Car, Best FROM (
            SELECT Car, LEAST(
                COALESCE(Timed1, Timed2),
                COALESCE(Timed2, Timed1),
                COALESCE(Timed3, Timed1),
                COALESCE(Timed4, Timed1)
            ) AS Best FROM ClassResults WHERE Class = %s ORDER BY Best
            ) AS Dave WHERE Best > 0 ORDER BY Best;""",
            (vclass,)
        )
        classfastest = cur.fetchone() if cur.rowcount else ["Nobody", 999.999]
    else:
        print("unknown class")
        vclass = "Unknown"
        classfastest = ["Nobody", 999.999]

    # Get results so far
    while cur.nextset():
        pass
    cur.execute("SELECT * FROM ClassResults WHERE Car=%s", (carno,))
    if cur.rowcount:
        results = cur.fetchone()
        if rs == "FAIL":
            ftime = 999.999
        RunColumns = ["", "Practice1", "Practice2", "Timed1", "Timed2", "Timed3", "Timed4"]
        fastest = 999.999
        for x in range(1, 6):
            if results[x] is None:
                if results[x] is None:
                    cur.execute(
                        f"UPDATE ClassResults SET {RunColumns[x]} = %s WHERE Car = %s",
                        (ftime, carno),
                    )
                    conn.commit()
                break
    else:
        while cur.nextset():
            pass
        cur.execute(
            "INSERT INTO ClassResults(Car, Practice1, Class) VALUES(%s, %s, %s)",
            (carno, ftime, vclass),
        )
        conn.commit()

# Record the raw result
def record_finish(result):
    carnumber = result.split("Car: ")[1].split(" ")[0]
    finishtime = result.split("Time: ")[1].split("\r")[0]
    x = result.split("\r")[1]
    sixtyfour = x.split("   ")[1].split(" ")[0]
    splittime = x.split("  ")[2].split("\r")[0]
    print(f"Car: {carnumber}, Time: {finishtime}, 64ft: {sixtyfour}, Split: {splittime}")

    if finishtime in ["NTR", "Red Flag"]:
        finishtime = "999.999"
        runstate = "RERUN"
    elif finishtime == "FAIL":
        runstate = "FAIL"
        print("updating results (%s, %s, %s)" % (carnumber, finishtime, runstate))
        update_results(carnumber, finishtime, runstate)
    else:
        runstate = "Normal"
        print("updating results (%s, %s, %s)" % (carnumber, finishtime, runstate))
        update_results(carnumber, finishtime, runstate)

    print("Inserting into RawResults (%s, %s, %s, %s, %s)" % (carnumber, sixtyfour, splittime, finishtime, runstate))
    # Insert into RawResults
    cur.execute(
        "INSERT INTO RawResults(Car, SixtyFour, Split, Finish, RunState) VALUES(%s, %s, %s, %s, %s)",
        (carnumber, sixtyfour, splittime, finishtime, runstate),
    )
    conn.commit()

    # speak_finish_time(carnumber, None, finishtime, splittime, sixtyfour)

# Main loop
while True:
    x = ser.readline().decode("utf-8")
    if "Car:" in x:
        print(f"Received: {x}")
        record_finish(x)

