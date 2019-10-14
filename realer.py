import json
import sys
import sqlite3
import uuid
from os import path
import random
import hashlib
import shutil
from datetime import datetime

import config

# Real database entries
# copy the database file into different name
# enter the data in order

# Backup the older database
today = datetime.today()
shutil.copy(config.DATABASE, "backup-{0}-{1}.db".format(today.strftime("%Y%m%d%H%M%S"), random.randint(1000, 9999)))

connection = sqlite3.connect(config.DATABASE)

# Remove entries
connection.execute("DELETE FROM missing;")
connection.execute("DELETE FROM amenities;")
connection.execute("DELETE FROM associates;")

cursor = connection.cursor()

associates = ["David", "John", "Jane", "Kate", "Richard", "Marta", "Mary", "Norma", "Ralph", "Vince"]
for associate in associates:
    id = str(uuid.uuid4()).upper()
    password = hashlib.md5(id.encode()).hexdigest()
    data = [id, associate, password, 0,]
    sql="INSERT INTO associates VALUES(?, ?, ?, ?);"
    cursor.execute(sql, data)

amenities = [
    "Bath Mat",
    "Clinex", "Coffee", "Condiments",
    "DND Card",
    "Face Clothes (Towel)", "Garbage Bag", "Hair Dryer", "Hand Towel", "Ice Bag",
    "Laundry Bag", "Laundry List", "Lids",
    "Memo Pad (Note Book)", "Micro Oven", "Paper Towel", "Pens", "Pillow",
    "Shampoo", "Soap", "TV Set", "Tea", "Towel", "Water Cups"
]
for amenity in amenities:
    id = str(uuid.uuid4()).upper()
    data = [id, amenity, 0]
    sql="INSERT INTO amenities VALUES(?, ?, ?);"
    cursor.execute(sql, data)

connection.commit()

connection.execute("VACUUM;")
connection.close()
