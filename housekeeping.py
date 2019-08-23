from flask import Flask, url_for, render_template, request
from flask import Response
import json
import sys
import sqlite3
import uuid
from os import path

APP_ROOT = "."
#APPROOT = "/home/tutor/Desktop/housekeeping"
DATABASE = "./housekeeping.db"
LIMITS = 400

app = Flask(__name__)
# app = Flask(__name__, static_folder='static', static_url_path='')
# https://flask-httpauth.readthedocs.io/en/latest/

#app.add_url_rule("/favicon.ico", redirect_to=url_for("static", filename="favicon.ico"))

@app.route("/", methods=["GET"])
def index():
    return render_template("housekeeping.html")


# http://127.0.0.1:5000/html/configs ==> static/html/configs.html
@app.route("/html/<string:rawpath>", methods=["GET"])
def html_templates_for_angularjs(rawpath=""):
    html = ""

    # prevent hacks to download other unspefied files
    rawpath = rawpath.replace("/", "")
    rawpath = rawpath.replace("..", "")
    rawpath = rawpath.lower()
    template_file = "{0}/static/html/{1}.html".format(APP_ROOT, rawpath)
    if path.isfile(template_file):
        with open(template_file, "r") as f:
            html = f.read()
    else:
        html = "Template file not found." # {0} and {1}".format(rawpath, template_file)

    #return html
    r = Response(response=html, status=200, mimetype="text/html")
    r.headers["Content-Type"] = "text/html; charset=utf-8"
    return r


# http://127.0.0.1:5000/api/missing/list
@app.route("/api/missing/list", methods=["GET", "POST"])
def api_missing_list():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT id, SUBSTR(`date`, 0, 11) `date`, associate, room_number, missingstuffs, anc, remarks FROM missing WHERE deleted=0 AND created_on LIKE DATE('NOW', 'LOCALTIME')||'%' ORDER BY created_on DESC LIMIT ?;", (LIMITS,))
    data = cursor.fetchall()
    connection.close()

    return json.dumps(data)


# http://127.0.0.1:5000/api/missing/reports
@app.route("/api/missing/reports", methods=["GET", "POST"])
def api_missing_reports():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT id, SUBSTR(`date`, 0, 11) `date`, associate, room_number, missingstuffs, anc, remarks FROM missing WHERE deleted=? ORDER BY date DESC LIMIT ?;", (0, LIMITS,))
    data = cursor.fetchall()
    connection.close()

    return json.dumps(data)


# http://127.0.0.1:5000/api/missing/reports/individual
@app.route("/api/missing/reports/individual", methods=["POST"])
def api_missing_reports_individual():
    data = json.loads(request.data.decode())
    #print("Data received: ", data)
    connection = sqlite3.connect(DATABASE)

    # get unique name of the associate
    cursor = connection.cursor()
    cursor.execute("select associate_name name from associates where associate_id=? LIMIT 1;", (data["id"],))
    associate = cursor.fetchone()
    #print("Associate found: ", associate)
    
    cursor.execute("SELECT id, SUBSTR(`date`, 0, 11) `date`, associate, room_number, missingstuffs, anc, remarks FROM missing WHERE deleted=0 AND associate=? ORDER BY date DESC LIMIT ?;", (associate[0], LIMITS,))
    data = cursor.fetchall()
    connection.close()

    return json.dumps(data)


# http://127.0.0.1:5000/api/missing/save
@app.route("/api/missing/save", methods=["POST"])
def api_missing_save():
    # https://realpython.com/flask-by-example-integrating-flask-and-angularjs/
    # {'associate': 'arj', 'room_number': 'asdf', 'missingstuffs': 'asdf', 'anc': 'asdf', 'remarks': 'dfs', 'date': None}
    data = json.loads(request.data.decode())
    id = str(uuid.uuid4()).upper()

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    fields = (id, data["associate"], data["room_number"], data["missingstuffs"], data["anc"], data["remarks"], data["date"], 0)
    cursor.execute("INSERT INTO missing VALUES (?, DATETIME('NOW', 'LOCALTIME'), ?, ?, ?, ?, ?, ?, ?)", fields)
    connection.commit()
    connection.close()

    return "Missing record saved"


# http://127.0.0.1:5000/api/missing/remove
@app.route("/api/missing/remove", methods=["GET", "POST"])
def api_missing_remove():
    data = json.loads(request.data.decode())

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE missing SET deleted=1 WHERE id=?", (data["id"],))
    connection.commit()
    connection.close()

    return "Deleted"
    

# http://127.0.0.1:5000/api/associates/list
@app.route("/api/associates/list", methods=["GET", "POST"])
def api_associates_list():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT associate_id id, associate_name name FROM associates WHERE deleted=0 ORDER BY associate_name LIMIT ?;", (LIMITS,))
    data = cursor.fetchall()
    connection.close()

    return json.dumps(data)


# http://127.0.0.1:5000/api/associate/details
@app.route("/api/associate/details", methods=["GET", "POST"])
def api_associate_details():
    data = json.loads(request.data.decode())
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT associate_id id, associate_name name FROM associates WHERE deleted=0 AND associate_id=?;", (data["id"],))
    data = cursor.fetchone()
    connection.close()

    return json.dumps(data)

# http://127.0.0.1:5000/api/associates/entries
@app.route("/api/associates/entries", methods=["GET", "POST"])
def api_associates_entries():
    data = json.loads(request.data.decode())

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    sql = """
SELECT
	a.associate_id,
	a.associate_name,
	COUNT(*) entries
FROM missing m
INNER JOIN associates a ON a.associate_name = m.associate
WHERE m.deleted=? AND a.associate_id=?
GROUP BY a.associate_name
ORDER BY a.associate_name ASC;
"""
    #print(sql, data)
    cursor.execute(sql, (0, data["id"],))
    report = cursor.fetchone()
    connection.close()

    if not report:
        report = ["", "", 0]

    return json.dumps(report)


# http://127.0.0.1:5000/api/configs/list
@app.route("/api/configs/list", methods=["GET", "POST"])
def api_configs_list():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT config_name name, config_value value, config_notes FROM configs WHERE show='Y' ORDER BY config_name;")
    data = cursor.fetchall()
    connection.close()

    #return json.dumps(data)
    r = Response(response=json.dumps(data), status=200, mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r


# http://127.0.0.1:5000/api/amenities/list
@app.route("/api/amenities/list", methods=["GET", "POST"])
def api_amenities_list():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT amenity_id id, amenity_name name FROM amenities WHERE deleted=0 ORDER BY amenity_name COLLATE NOCASE;")
    data = cursor.fetchall()
    connection.close()

    return json.dumps(data)


# http://127.0.0.1:5000/api/amenities/save
@app.route("/api/amenities/save", methods=["POST"])
def api_amenities_save():
    data = json.loads(request.data.decode())
    id = str(uuid.uuid4()).upper()

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    fields = (id, data["name"], 0,)
    cursor.execute("INSERT INTO amenities VALUES (?, ?, ?)", fields)
    connection.commit()
    connection.close()

    return "Amentiy saved"


# http://127.0.0.1:5000/api/amenities/remove
@app.route("/api/amenities/remove", methods=["POST"])
def api_amenities_remove():
    data = json.loads(request.data.decode())

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE amenities SET deleted=1 WHERE amenity_id=?", (data["id"],))
    connection.commit()
    connection.close()

    return "Amentiy deleted"


if __name__ == "__main__":
    # python3 housekeeping.py >> log.txt 2>&1 &
    # ps aux | grep housekeeping

    # http://192.168.0.101:5000/#!/missing
    
    #app.run(host="192.168.1.80", port=5000, debug=True)
    #app.run(host="192.168.1.76", port=5000, debug=True)
    #app.run(host="192.168.0.101", port=5000, debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
    #app.run(port=1001, debug=True)
    #app.run(debug=True)
 
