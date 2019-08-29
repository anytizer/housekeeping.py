import uuid
import datetime
import sqlite3

source = sqlite3.connect("RawFile.db")
cursor = source.cursor()

sql="SELECT * FROM missing;"
cursor.execute(sql, ())
data = cursor.fetchall()
source.commit()
source.close()
#print(data)
#print(data[0])
print("Completed reading the source...");
print("Found entries: ", len(data))

last_associate = list(data[0])[2]

destination = sqlite3.connect("housekeeping.db")
dcursor = destination.cursor()
dcursor.execute("DELETE FROM missing;", ())
insert_sql="""
INSERT INTO missing (
    id, created_on,
    associate, room_number, missingstuffs, anc, remarks,
    date, deleted
) VALUES (
    ?, ?, ?, ?, ?, ?, ?, ?, ?
);"""
for raw1 in data:
    raw = list(raw1)
    # (0, 1, 'Trina', 122, 'Tea', '', '2019-08-01')

    # replace null with ""
    for r in range(0, len(raw)):
        raw[r] = str(raw[r]).strip() if raw[r] else ""

    if raw[2] == "":
        raw[2] = last_associate
    else:
        last_associate = raw[2]
    
    final = [
        str(uuid.uuid4()).upper(),
        str(datetime.datetime.today()),
        raw[2], # associate
        raw[3], # room number
        raw[4], # missingstuffs
        raw[5], # anc
        "", # remarks
        raw[6], # date
        0, # deleted
    ]
    dcursor.execute(insert_sql, final)

print("Inserting the records...")

# Adjustments
dcursor.execute("UPDATE missing SET missingstuffs='Pens' WHERE missingstuffs='Pen';")
dcursor.execute("UPDATE missing SET missingstuffs='Bath Mat' WHERE missingstuffs='bath mat';")
dcursor.execute("UPDATE missing SET missingstuffs='Ice Bag' WHERE missingstuffs='Ice bag';")
dcursor.execute("UPDATE missing SET missingstuffs='Ice Bag' WHERE missingstuffs='ice bag';")
dcursor.execute("UPDATE missing SET missingstuffs='Garbage Bag' WHERE missingstuffs='Garbage bag';")
dcursor.execute("UPDATE missing SET missingstuffs='Memo Pad (Note Book)' WHERE missingstuffs='Memo pad';")
dcursor.execute("UPDATE missing SET missingstuffs='Memo Pad (Note Book)' WHERE missingstuffs='Memo Pad';")
dcursor.execute("UPDATE missing SET missingstuffs='Toilet Paper' WHERE missingstuffs='toilet paper';")
dcursor.execute("UPDATE missing SET missingstuffs='Toilet Paper' WHERE missingstuffs='Toilet paper';")
dcursor.execute("UPDATE missing SET missingstuffs='Face Clothes (Towel)' WHERE missingstuffs='Face clothes';")

dcursor.execute("UPDATE missing SET associate='Allyn' WHERE associate='allyn';");

# SELECT missingstuffs, COUNT(missingstuffs) total FROM missing GROUP BY missingstuffs ORDER BY missingstuffs;

#print(final)
destination.commit()
destination.close()

print("Manual Query Adjustments...")
print("Done!")
