import json
import sys
import sqlite3
import uuid
from os import path
import random

import config

# Generate random database

connection = sqlite3.connect(config.DATABASE)
cursor = connection.cursor()

for i in range(1, 2000):
    date = str(random.randint(2018, 2019))+"-"+str(random.randint(1, 12)).zfill(2)+"-"+str(random.randint(1, 28)).zfill(2)

    cursor.execute("SELECT associate_name `associate` FROM associates ORDER BY RANDOM() LIMIT 1;")
    associate_info = cursor.fetchone()
    associate = associate_info[0]

    room_number = str(random.randint(100, 999)).zfill(3)

    amenity_sql="SELECT amenity_name `amenity` FROM amenities ORDER BY RANDOM() LIMIT 1;"
    cursor.execute(amenity_sql)
    amenity_info = cursor.fetchone()
    missingstuffs = random.choice(["", amenity_info[0],])

    # area not cleaned
    anc = random.choice(["", random.choice(["washroom", "sink", "floor", "window", "cabinets", "entrance", "lobby", "sofa"])])

    remarks = random.choice(["", random.choice(["stain", "hair", "dusts", "bugs"])])

    data = {"date": date, "associate": associate, "room_number": room_number, "missingstuffs": missingstuffs, "anc": anc, "remarks": remarks,}
    id = str(uuid.uuid4()).upper()
    deleted = 0

    # Portion of live code
    fields = (id, data["associate"], data["room_number"], data["missingstuffs"].upper(), data["anc"], data["remarks"], data["date"], deleted,)
    cursor.execute("INSERT INTO missing VALUES (?, DATETIME('NOW', 'LOCALTIME'), ?, ?, ?, ?, ?, ?, ?)", fields)

cleanup_sql="DELETE FROM missing WHERE missingstuffs=? AND anc=? AND remarks=?;"
cursor.execute(cleanup_sql, ["", "", ""])

connection.commit()

connection.execute("VACUUM;")
connection.close()
