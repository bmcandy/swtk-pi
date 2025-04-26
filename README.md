# swtk-pi
Scripts to receive timing data from SW Timekeeping

Data is received over RS232 using a MAX232 converter at 1200 baud.  The data is parsed and inserted into a MariaDB database on the Pi.  A flask app returns this data over a web interface.

## Pre-requisites (v2)
- MariaDB installed on the Pi
- Python (obvs, but running v2 because Pi & dependencies)

## Pre-requisites (v3)
- Raspberry Pi (tested on Pi4)
- Raspbian OS (latest as of 26/04/2025)

## v3 Installation
- git clone https://github.com/bmcandy/swtk-pi.git
- cd swtk-pi
- cp .env-example .env
- edit the values of .env to match your setup, although it'll work out of the box as it's all internal (insecure) passwords
- ./install.sh
- ./run.sh

## Requirements
- **Database**: MariaDB with the following tables:
  - `Entries`: Stores car, driver, and class information.
  - `RawResults`: Stores timing data such as `SixtyFour`, `Split`, and `Finish`.
  - `ClassResults`: Stores class-specific timing data.
- **Python Libraries**:
  - `MySQLdb`: For database interaction.
  - `Flask`: For creating the API.
  - `serial`: For reading RS232 data.
- **Web Server**:
  - PHP scripts for fetching data (`getlatest.php`, `getranked.php`, etc.).
  - HTML/CSS/JavaScript for rendering data (e.g., `Latest.html`, `Ranked.html`).
- **RS232 Connection**:
  - Data received at 1200 baud using a MAX232 converter.
- **Environment**:
  - Python 2.x (due to compatibility with dependencies).
  - Linux-based system (e.g., Raspberry Pi).

## User Stories
- **As a race official**, I want to record car finish times, split times, and 64-foot times from RS232 data so that I can track race results in real-time.
- **As a database administrator**, I want to store raw results and class results in a MariaDB database so that I can query and analyze race data.
- **As a race official**, I want to handle special cases like failed runs or reruns so that the system reflects accurate race statuses.
- **As a race announcer**, I want the system to generate spoken messages for finish times so that I can announce results to the audience.
- **As a developer**, I want the system to automatically determine the fastest times and improvements so that I can highlight notable performances.
- **As a user**, I want the system to continuously monitor the serial interface so that race data is updated in real-time.

## Components
### api.py
Flask API that returns data from the MySQL Database.

### createentries.py
A short script to make up an entry list and populate the databaase for testing.

### read_serial.py
The script to read the serial data and push timing data into the database.  read_serial3.py is a fork of a previous version for Python3 that doesn't work.

### write_serial.py
A generator for serial data to emulate the timing system.  Used for testing that read_serial.py is functioning correctly.

### /templates
HTML templates for writing HTML pages through flask.  Used for the index page at the moment.
