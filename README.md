# housekeeping.py
List of amenities and stuffs forgotten by your housekeeping department.

## Built Using:
 * [Python 3](https://www.python.org/downloads/)
 * [Flask](https://palletsprojects.com/p/flask/)
 * [AngularJS](https://angularjs.org/)
 * [SQLite 3](https://www.sqlite.org/)
 * [W3CSS](https://www.w3schools.com/w3css/)

## Features
 * List of amenities
 * List of Associates (Workers)
 * List of amenities that the associates forgot to replace on specified dates and rooms.
 * Data Entry
 * Reports
 * All pages are printer friendly

## Scripts
 * [realer.py](realer.py) - Installs the database contents.
 * [faker.py](faker.py) - Installs dummy data, optional
 * [importer.py](importer.py) - Imports data from another database
 * [housekeeping.py](housekeeping.py) - Main web server scripts

### Installation
 * Install python 3.
 * Install pip 3.
 * Install Flask: `pip install flask`
 * Checkout this project using Git.
 * `cd housekeeping.py`
 * Edit `realer.py` with your own associates and amenities.
 * Run `python3 realer.py`
 * Optionally, run sample data: `python3 faker.py`
 * Run the script from terminal: `python3 housekeeping.py`
 * Browse the website: [http://0.0.0.0:5000/](http://0.0.0.0:5000/) with your own IP Addresses over the LAN
 * Port 5000 - This is the default port number to access the website

### Operations
 * Forgotten data entry
 * Reports for today
 * Whole reports of amenities forgotten
 * List of associates
   - Number of records
   - Enter new forgotten amenity
 * Reports per amenity
 * List of amentities for suggestions
