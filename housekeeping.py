from flask import Flask, url_for, render_template, request
from flask import Response
from flask import g
import json
import sys
import sqlite3
import uuid
import datetime
from os import path

app = Flask(__name__)

ROOT_PATH = app.root_path

DATABASE = ROOT_PATH+"/housekeeping.db"
LIMITS = 400

# @todo Use context: https://flask.palletsprojects.com/en/1.0.x/appcontext/
connection = sqlite3.connect(DATABASE, check_same_thread=False)

# For long SQLs, read them from file
def sqlfile(file=""):
    f=open(ROOT_PATH + "/sqls/" + file, "r")
    contents = f.read()
    return contents


@app.route("/", methods=["GET"])
def index():
    timestamp = str(datetime.datetime.now().date())
    return render_template("housekeeping.html", timestamp=timestamp)


# prints app root path
# http://127.0.0.1:5000/test
@app.route("/test", methods=["GET"])
def test():
    return app.root_path


# SET FLASK_APP = "housekeeping.py"
# flask routes > routes.txt
@app.route("/endpoints", methods=["GET"])
def endpoints():
    links = []
    for rule in app.url_map.iter_rules():
        links.append({"endpoint":rule.endpoint, "method":rule.methods})

    r = Response(response=str(links), status=200, mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r


# http://127.0.0.1:5000/html/configs ==> static/html/configs.html
@app.route("/html/<string:rawpath>", methods=["GET"])
def html_templates_for_angularjs(rawpath=""):
    # prevent hacks to download other unspecified files
    rawpath = rawpath.replace("/", "")
    rawpath = rawpath.replace("\\", "")
    rawpath = rawpath.replace("..", "")
    rawpath = rawpath.lower()
    template_file = "{0}/static/html/{1}.html".format(ROOT_PATH, rawpath)

    html = ""
    if path.isfile(template_file):
        with open(template_file, "r") as f:
            html = f.read()
    else:
        html = "Template file not found. {0} and {1}. Check for <strong>spelling errors</strong>, or <strong>JS</strong> being cached.".format(rawpath, template_file)

    r = Response(response=html, status=200, mimetype="text/html")
    r.headers["Content-Type"] = "text/html; charset=utf-8"
    return r


# http://127.0.0.1:5000/api/missing/list
@app.route("/api/missing/list", methods=["POST"])
def api_missing_list():
    cursor = connection.cursor()
    cursor.execute(sqlfile("missing-list.sql"), (LIMITS,))
    data = cursor.fetchall()

    return json.dumps(data)


# http://127.0.0.1:5000/api/missing/reports
@app.route("/api/missing/reports", methods=["POST"])
def api_missing_reports():
    cursor = connection.cursor()

    cursor.execute(sqlfile("raw.sql"), (0, LIMITS,))
    data_raw = cursor.fetchall()

    missingstuffs_counter_sql=sqlfile("missingstuffs-counter.sql")
    cursor.execute(missingstuffs_counter_sql, ())
    data_missingstuffs_counter = cursor.fetchall()

    associates_reporting_sql=sqlfile("associates-reporting.sql")
    cursor.execute(associates_reporting_sql, ())
    associates_reporting = cursor.fetchall()

    data = {
        "raw": data_raw,
        "missingstuffs_counter": data_missingstuffs_counter,
        "associates_reporting": associates_reporting,
    }
    return json.dumps(data)


# http://127.0.0.1:5000/api/missing/reports/individual
@app.route("/api/missing/reports/individual", methods=["POST"])
def api_missing_reports_individual():
    data = json.loads(request.data.decode())

    cursor = connection.cursor()
    cursor.execute("SELECT associate_name NAME FROM associates WHERE associate_id=? LIMIT 1;", (data["id"],))
    associate = cursor.fetchone()

    cursor.execute("SELECT id, SUBSTR(`date`, 0, 11) `date`, associate, room_number, missingstuffs, anc, remarks FROM missing WHERE deleted=0 AND associate=? ORDER BY DATE DESC LIMIT ?;", (associate[0], LIMITS,))
    data = cursor.fetchall()

    return json.dumps(data)


# Individual report of an amenity
# http://127.0.0.1:5000/api/missing/reports/amenity
@app.route("/api/missing/reports/amenity", methods=["POST"])
def api_missing_reports_amenity():
    data = json.loads(request.data.decode())
    cursor = connection.cursor()
    sql = "SELECT id, SUBSTR(`date`, 0, 11) `date`, associate, room_number, missingstuffs, anc, remarks FROM missing WHERE deleted=0 AND missingstuffs=? ORDER BY date DESC LIMIT ?;"
    cursor.execute(sql, (data["amenity"], LIMITS,))
    data = cursor.fetchall()

    return json.dumps(data)


# http://127.0.0.1:5000/api/missing/save
@app.route("/api/missing/save", methods=["POST"])
def api_missing_save():
    # https://realpython.com/flask-by-example-integrating-flask-and-angularjs/
    # {'associate': 'arj', 'room_number': 'asdf', 'missingstuffs': 'asdf', 'anc': 'asdf', 'remarks': 'dfs', 'date': None}
    data = json.loads(request.data.decode())
    id = str(uuid.uuid4()).upper()

    cursor = connection.cursor()
    fields = (id, data["associate"], data["room_number"], data["missingstuffs"].upper(), data["anc"], data["remarks"], data["date"], 0)
    cursor.execute("INSERT INTO missing VALUES (?, DATETIME('NOW', 'LOCALTIME'), ?, ?, ?, ?, ?, ?, ?)", fields)
    connection.commit()

    return "Missing stuffs saved"


# http://127.0.0.1:5000/api/missing/remove
@app.route("/api/missing/remove", methods=["POST"])
def api_missing_remove():
    data = json.loads(request.data.decode())

    cursor = connection.cursor()
    cursor.execute("UPDATE missing SET deleted=1 WHERE id=?", (data["id"],))
    connection.commit()

    return "Deleted a wrong entry"
    

# http://127.0.0.1:5000/api/associates/list
@app.route("/api/associates/list", methods=["POST"])
def api_associates_list():
    cursor = connection.cursor()
    cursor.execute("SELECT associate_id id, associate_name name FROM associates WHERE deleted=0 ORDER BY associate_name;", ())
    data = cursor.fetchall()

    return json.dumps(data)


# http://127.0.0.1:5000/api/associate/details
@app.route("/api/associate/details", methods=["POST"])
def api_associate_details():
    data = json.loads(request.data.decode())
    cursor = connection.cursor()
    cursor.execute("SELECT associate_id id, associate_name name FROM associates WHERE deleted=0 AND associate_id=?;", (data["id"],))
    data = cursor.fetchone()

    return json.dumps(data)


# http://127.0.0.1:5000/api/associates/entries
@app.route("/api/associates/entries", methods=["POST"])
def api_associates_entries():
    data = json.loads(request.data.decode())

    cursor = connection.cursor()
    sql = sqlfile("associates-entries.sql")
    # print(sql, data)
    cursor.execute(sql, (0, data["id"],))
    report = cursor.fetchone()

    if not report:
        report = ["", "", 0,]

    return json.dumps(report)


# http://127.0.0.1:5000/api/associates/amenities
@app.route("/api/associates/amenities", methods=["POST"])
def api_associates_amenities():
    data = json.loads(request.data.decode())
    cursor = connection.cursor()
    sql = sqlfile("associates-amenities.sql")
    # print(sql, data)
    cursor.execute(sql, (data["amenity"],))
    report = cursor.fetchone()

    if not report:
        report = [0,]

    return json.dumps(report)


# http://127.0.0.1:5000/api/configs/list
@app.route("/api/configs/list", methods=["POST"])
def api_configs_list():
    cursor = connection.cursor()
    cursor.execute("SELECT config_name name, config_value value, config_notes FROM configs WHERE show='Y' ORDER BY config_name;")
    data = cursor.fetchall()

    # return json.dumps(data)
    r = Response(response=json.dumps(data), status=200, mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r


# http://127.0.0.1:5000/api/amenities/list
@app.route("/api/amenities/list", methods=["POST"])
def api_amenities_list():
    cursor = connection.cursor()
    cursor.execute("SELECT amenity_id id, amenity_name name FROM amenities WHERE deleted=0 ORDER BY amenity_name COLLATE NOCASE;")
    data = cursor.fetchall()

    return json.dumps(data)


# http://127.0.0.1:5000/api/amenities/remove
@app.route("/api/amenities/remove", methods=["POST"])
def api_amenities_remove():
    data = json.loads(request.data.decode())
    cursor = connection.cursor()
    cursor.execute("UPDATE amenities SET deleted=1 WHERE amenity_id=?", (data["id"],))
    connection.commit()

    return "Amenity deleted"


# http://127.0.0.1:5000/api/amenities/save
@app.route("/api/amenities/save", methods=["POST"])
def api_amenities_save():
    data = json.loads(request.data.decode())
    id = str(uuid.uuid4()).upper()
    cursor = connection.cursor()
    fields = (id, data["name"].upper(), 0,)
    cursor.execute("INSERT INTO amenities VALUES (?, ?, ?)", fields)
    connection.commit()

    return "Amenity saved: " + data["name"]


# http://127.0.0.1:5000/api/amenities/import
@app.route("/api/amenities/import", methods=["POST"])
def api_amenities_import():
# get list of all amenities
# for each amenity
# if does not exist in destination
# insert
    cursor = connection.cursor()
    suggestions_sql="SELECT UPPER(missingstuffs) amenity, COUNT(missingstuffs) total FROM missing GROUP BY UPPER(missingstuffs) ORDER BY amenity;"
    cursor.execute(suggestions_sql, ())
    data = cursor.fetchall()

    for amenity in data:
        check_sql="SELECT * FROM amenities WHERE amenity_name=?;"
        cursor.execute(check_sql, (amenity[0],))
        existing = cursor.fetchone()
        if not existing:
            id = str(uuid.uuid4()).upper()
            fields = (id, amenity[0].upper(), 0,)
            cursor.execute("INSERT INTO amenities VALUES (?, ?, ?)", fields)
    
    connection.commit()
    return json.dumps(data)


if __name__ == "__main__":
    # python3 housekeeping.py >> log.txt 2>&1 &
    # ps aux | grep housekeeping
    app.run(host="0.0.0.0", port=5000, debug=True)
