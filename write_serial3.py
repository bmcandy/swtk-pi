#!/usr/bin/env python3

import time
import serial
import random
from dotenv import load_dotenv  # pip install python-dotenv
import os

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=1200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

f = open("serialoutput.txt", "w")

try:
    db_host = os.getenv("DB_HOST")
    if db_host:
        import MySQLdb  # apt-get install python3-mysqldb
        conn = MySQLdb.connect(
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            host=db_host,
            port=3306,
            db=os.getenv("DB_NAME")
        )
    else:
        conn = None
except MySQLdb.Error as e:
    print(e)

while True:
    if conn:
        # Select a random entry from the database
        cur = conn.cursor()
        cur.execute('''SELECT Car FROM Entries;''')
        entries = cur.fetchall()
        conn.commit()
        randomentry = random.randint(0, len(entries) - 1)
        car = str(''.join(entries[randomentry]))
    else:
        # Iterate through car numbers 1 to 100
        car = str(random.randint(1, 100))

    # Add an "A" car that probably doesn't exist every ~20 cars
    if random.randint(1, 20) == 1:
        print("Invalid car")
        car = car + "A"
    finish = str(random.randint(34, 63)) + "." + str(random.randint(10, 99))
    # Report car as no time recorded every ~40 cars
    if random.randint(1, 40) == 1:
        print("NTR")
        finish = "NTR"
    # Report car as red flagged every ~100 cars
    if random.randint(1, 100) == 1:
        print("Red Flag")
        finish = "Red Flag"
    # Generate a 64ft/split time 99% of the time
    if random.randint(1, 100) > 1:
        sixfour = str(random.randint(2, 4)) + "." + str(random.randint(10, 99))
    else:
        print("No 64ft time")
    if random.randint(1, 100) > 1:
        splittime = str(random.randint(22, 28)) + "." + str(random.randint(10, 99))
    else:
        print("No split time")
    print(f"Car: {car}  Time: {finish}\r\n   {sixfour}  {splittime}\r\n\nxxx\n")
    ser.write(f"Car: {car}  Time: {finish}\r   {sixfour}  {splittime}\rxxx".encode())
    f.write(f"Car: {car}  Time: {finish}\r\n   {sixfour}  {splittime}\r\n\nxxx\n")
    # Wait until starting the next car
    interval = random.randint(2, 5)  # 2-5 seconds (fast testing)
    # interval = random.randint(22, 30) # 22-30 seconds (realistic)
    print(f"waiting {interval} seconds")
    time.sleep(interval)
    # Add end of batch every ~20 cars
    if random.randint(1, 20) == 1:
        ser.write("End of Batch\n".encode())
        f.write("End of Batch\n")
        endbatch = random.randint(300, 600)
        print(f"End of batch.  Sleeping {endbatch} seconds")
        # time.sleep(endbatch)
