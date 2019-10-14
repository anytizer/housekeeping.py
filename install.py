import sqlite3

import config

connection = sqlite3.connect(config.DATABASE)
cursor = connection.cursor()

files = [
    "sqlite/amenities.sql",
    "sqlite/associates.sql",
    "sqlite/configs.sql",
    "sqlite/missing.sql",
]

for sqlfile in files:
    print(sqlfile)
    with open(sqlfile, "r") as f:
        sqllines = f.read()
        print(sqllines)

        connection.executescript(sqllines)

connection.commit()

connection.execute("VACUUM;")
connection.close()
