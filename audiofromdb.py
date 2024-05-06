import pyttsx3  # pip install pyttsx3
import mysql.connector  # pip install mysql-connector-python
from datetime import datetime
import time

engine = pyttsx3.init()

# Connect to the MySQL database
mydb = mysql.connector.connect(
    user="Results",
    passwd="Results",
    host="192.168.69.32",
    port=3306,
    db="SpeedOnScreen",
)


class RawResultsReader:
    """Reads the last row from the RawResults table."""

    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.port = 3306
        self.cursor = None
        self.lastspoken = datetime.now()

    def connect(self):
        """Connects to the database."""
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database,
            port=self.port,
            autocommit=False,
        )
        self.cursor = self.connection.cursor()

    def get_driver_name(self, car):
        """Gets the driver name from the database."""
        if not self.connection:
            self.connect()

        # Get the driver name from the database
        sql = "SELECT Driver FROM Entries WHERE Car = %s"
        val = (car,)
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()

        # Print the results
        if result:
            driver = result[0]
            print("Driver:", driver)
            self.connection.commit()
            return driver
        else:
            print("No driver found for car", car)

        # Close the connection
        self.cursor.close()

    def get_latest_from_mysql(self):
        """Gets the last row from table RawResults"""
        if not self.connection:
            self.connect()

        # Get the last row of the RawResultsd table
        sql = "SELECT TimeOfDay,Car,SixtyFour,Split,Finish,RunState,Colour FROM RawResults ORDER BY TimeOfDay DESC LIMIT 1"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        # Print the results
        if result:
            # Accessing columns by name (assuming you know the column names)
            print("last received time:", result[0])
            print("last spoken time:", self.lastspoken)
            self.connection.commit()
            if result[6]:
                runtype = result[6]
            if self.lastspoken < result[0]:
                speak_finish_time(result[1], result[4], result[3], result[2], runtype)
                self.lastspoken = result[0]
        else:
            print("No data found in the RawResults table")
            return None

        # Close the connection
        # self.cursor.close()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


def speak_finish_time(car, finishtime, split, sixtyfour=None, runtype=None):
    """Function to speak the finish time of the driver."""
    if car and finishtime:
        driver = reader.get_driver_name(car)
        if runtype == "improved":
            message = "Improvement for "
        elif runtype == "classfastest":
            message = "Fastest in class for "
        else:
            message = " "
        message = (
            message
            + " Car number "
            + str(car)
            + " driven by "
            + driver
            + " finished in "
            + "{:.2f}".format(finishtime)
            + " seconds"
        )
        if split:
            message = (
                message + " with a split of " + "{:.2f}".format(split) + " seconds"
            )
        if sixtyfour:
            message = (
                message
                + " and a sixty four foot time of "
                + "{:.2f}".format(sixtyfour)
                + " seconds"
            )

        print(message)
        engine.say(message)
        engine.runAndWait()
        engine.startLoop(False)
        engine.endLoop()


def speak_class_results(thisclass):
    """Function to speak the results of a class."""
    print("Results for class " + thisclass)


def car_finished(car):
    # speak_finish_time(car, "Archie Laurence", "91.34", "46.63")
    return "Hello, World!"

    # user = ("Results",)
    # passwd = ("Results",)
    # host = ("192.168.69.32",)
    # port = (3306,)
    # db = ("SpeedOnScreen",)


reader = RawResultsReader("192.168.69.32", "Results", "Results", "SpeedOnScreen")

while True:
    try:
        reader.get_latest_from_mysql()
        time.sleep(3)
    except:
        print("failed to get time")
        reader.close()
        reader = RawResultsReader("192.168.69.32", "Results", "Results", "SpeedOnScreen")
        time.sleep(5)
reader.close()
