@echo off
set FLASK_APP=housekeeping.py
flask routes > routes.txt
