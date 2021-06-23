# swtk-pi
Scripts to receive timing data from SW Timekeeping

Data is received over RS232 using a MAX232 converter at 1200 baud.  The data is parsed and inserted into a MariaDB database on the Pi.  A flask app returns this data over a web interface.

## Pre-requisites
- MariaDB installed on the Pi
- Python (obvs, but running v2 because Pi & dependencies)

## Components
### api.py
Flask API that returns data from the MySQL Database.

### createentries.py
A short script to make up an entry list and populate the databaase for testing.

### read_serial.py
The script to read the serial data and push timing data into the database.  read_serial3.py is a fork of a previous version for Python3 that doesn't work.

### write_serial.py
A generator for serial data to emulate the timing system.  Used for testing.

### /templates
HTML templates for writing HTML pages through flask.  Used for the index page at the moment.
