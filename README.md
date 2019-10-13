# housekeeping.py

List of amenities and stuffs forgotten by your housekeeping department.

Source code of this software is made public, assuming that it would be helpful for the related industry.
If you use this software, a feedback is expected.


## Built Using:

* [Python 3](https://www.python.org/downloads/)
* [Flask](https://palletsprojects.com/p/flask/)
* [AngularJS](https://angularjs.org/)
* [SQLite 3](https://www.sqlite.org/)
* [W3CSS](https://www.w3schools.com/w3css/)
* IDEs: [Idle (Python)](https://www.python.org/downloads/), [Notepad++](https://notepad-plus-plus.org), [NetBeans](https://netbeans.org), [PHPStorm](https://www.jetbrains.com/?from=anytizer), [DB Browser for SQLite](https://sqlitebrowser.org), [PyCharm](https://www.jetbrains.com/pycharm/)


## Useful Python Scripts

* [install.py](install.py)
* [realer.py](realer.py) - Installs the database contents
* [faker.py](faker.py) - Optionally populate the dummy data
* [importer.py](importer.py) - Imports data from another database - sample
* [housekeeping.py](housekeeping.py) - Main web server API scripts


### Database

* **housekeeping.db** - SQLite database file


## Installation

* Install `python 3` and `pip 3` on a server.
* [Install Flask](https://flask.palletsprojects.com/en/1.1.x/installation/): `pip install flask`
* Checkout this project using Git.
* `cd housekeeping.py`
* Run `python3 install.py` to create database structure.
* Edit `realer.py` with your own list of associates and amenities.
* Run `python3 realer.py`
* Optionally, run sample data: `python3 faker.py`
* touch static/images/missing-amenities.png
* touch static/images/missing-associates.png
* Run the script from terminal: `python3 housekeeping.py`
* Browse the website: [http://0.0.0.0:5000/](http://0.0.0.0:5000/) with your own IP Addresses over the LAN
* Port 5000 - This is the default port number to access the website


## Features

* Data entry of  items forgotten by an associate
* List of Associates (Workers)
  - Total number of records
* Import amenities from data entry list
* List of amenities that the associates forgot to replace on specified dates and rooms.
  - Number of records
  - Enter new forgotten amenity
* Reports
  - Reports for today
  - Reports per amenity

All pages are printer friendly.


## Tested in

This product has been tested to run in:


### Operating Systems

Server script of this product has been tested to run in:

* [Raspberry Pi](https://www.raspberrypi.org)
* [macOS](https://en.wikipedia.org/wiki/MacOS)
* [MX Linux](https://mxlinux.org)
* [Windows 10](https://www.microsoft.com/en-ca/windows/get-windows-10)


### Browsers

* [Firefox](https://www.mozilla.org/en-CA/firefox/new/)
* [Opera](https://www.opera.com/download)
* [Chrome](https://www.google.com/chrome/)
* [Safari](https://support.apple.com/downloads/safari): ([DATALIST](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/datalist) not supported)


# Routes Extraction

    set FLASK_APP=housekeeping.py
    flask routes > routes.txt

