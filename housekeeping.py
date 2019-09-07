from flask import Flask, url_for, render_template, request
from flask import Response
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

# app = Flask(__name__, static_folder='static', static_url_path='')
# https://flask-httpauth.readthedocs.io/en/latest/

# app.add_url_rule("/favicon.ico", redirect_to=url_for("static", filename="favicon.ico"))


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
        # print(rule)
        # rule.methods
        # url = url_for(rule.endpoint, **(rule.defaults or {}))
        # links.append((url, rule.endpoint))
        links.append({"endpoint":rule.endpoint, "method":rule.methods})
    # links.sort()

    # return str(links)
    # json.dumps(links)
    r = Response(response=str(links), status=200, mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r


# http://127.0.0.1:5000/html/configs ==> static/html/configs.html
@app.route("/html/<string:rawpath>", methods=["GET"])
def html_templates_for_angularjs(rawpath=""):
    # prevent hacks to download other unspecified files
    # replaces = ["\\", "/", "..", "."]
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
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT id, SUBSTR(`date`, 0, 11) `date`, associate, room_number, missingstuffs, anc, remarks FROM missing WHERE deleted=0 AND created_on LIKE DATE('NOW', 'LOCALTIME')||'%' ORDER BY created_on DESC LIMIT ?;", (LIMITS,))
    data = cursor.fetchall()
    connection.close()

    return json.dumps(data)


# http://127.0.0.1:5000/api/missing/reports
@app.route("/api/missing/reports", methods=["POST"])
def api_missing_reports():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT id, SUBSTR(`date`, 0, 11) `date`, associate, room_number, missingstuffs, anc, remarks FROM missing WHERE deleted=? ORDER BY `date` DESC, associate ASC, room_number ASC LIMIT ?;", (0, LIMITS,))
    data_raw = cursor.fetchall()

    missingstuffs_counter_sql="""
select
	m.missingstuffs stuff,
	count(m.missingstuffs) total
from associates a
inner join missing m on m.associate = a.associate_name
where m.missingstuffs!=""
group by
	m.missingstuffs
order by total desc
;
"""
    cursor.execute(missingstuffs_counter_sql, ())
    data_missingstuffs_counter = cursor.fetchall()

    associates_reporting_sql="""
select
	a.associate_name associate,
	sum(case when m.missingstuffs == "" then 0 else 1 end) missingstuffs_total,
	sum(case when m.anc == "" then 0 else 1 end) anc_total,
	count(a.associate_name) total
from associates a
inner join missing m on m.associate = a.associate_name
group by
	a.associate_name
order by total desc
;
"""
    cursor.execute(associates_reporting_sql, ())
    associates_reporting = cursor.fetchall()

    connection.close()

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
    # print("Data received: ", data)
    connection = sqlite3.connect(DATABASE)

    # get unique name of the associate
    cursor = connection.cursor()
    cursor.execute("SELECT associate_name NAME FROM associates WHERE associate_id=? LIMIT 1;", (data["id"],))
    associate = cursor.fetchone()
    # print("Associate found: ", associate)
    
    cursor.execute("SELECT id, SUBSTR(`date`, 0, 11) `date`, associate, room_number, missingstuffs, anc, remarks FROM missing WHERE deleted=0 AND associate=? ORDER BY DATE DESC LIMIT ?;", (associate[0], LIMITS,))
    data = cursor.fetchall()
    connection.close()

    return json.dumps(data)


# Individual report of an amenity
# http://127.0.0.1:5000/api/missing/reports/amenity
@app.route("/api/missing/reports/amenity", methods=["POST"])
def api_missing_reports_amenity():
    data = json.loads(request.data.decode())
    # print("Data received: ", data)
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    sql = "SELECT id, SUBSTR(`date`, 0, 11) `date`, associate, room_number, missingstuffs, anc, remarks FROM missing WHERE deleted=0 AND missingstuffs=? ORDER BY date DESC LIMIT ?;"
    cursor.execute(sql, (data["amenity"], LIMITS,))
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
    fields = (id, data["associate"], data["room_number"], data["missingstuffs"].upper(), data["anc"], data["remarks"], data["date"], 0)
    cursor.execute("INSERT INTO missing VALUES (?, DATETIME('NOW', 'LOCALTIME'), ?, ?, ?, ?, ?, ?, ?)", fields)
    connection.commit()
    connection.close()

    return "Missing stuffs saved"


# http://127.0.0.1:5000/api/missing/remove
@app.route("/api/missing/remove", methods=["POST"])
def api_missing_remove():
    data = json.loads(request.data.decode())

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE missing SET deleted=1 WHERE id=?", (data["id"],))
    connection.commit()
    connection.close()

    return "Deleted a wrong entry"
    

# http://127.0.0.1:5000/api/associates/list
@app.route("/api/associates/list", methods=["POST"])
def api_associates_list():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT associate_id id, associate_name name FROM associates WHERE deleted=0 ORDER BY associate_name;", ())
    data = cursor.fetchall()
    connection.close()

    return json.dumps(data)


# http://127.0.0.1:5000/api/associate/details
@app.route("/api/associate/details", methods=["POST"])
def api_associate_details():
    data = json.loads(request.data.decode())
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT associate_id id, associate_name name FROM associates WHERE deleted=0 AND associate_id=?;", (data["id"],))
    data = cursor.fetchone()
    connection.close()

    return json.dumps(data)

# http://127.0.0.1:5000/api/associates/entries
@app.route("/api/associates/entries", methods=["POST"])
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
WHERE
    m.deleted=? AND a.associate_id=?
GROUP BY a.associate_name
ORDER BY a.associate_name ASC;
"""
    # print(sql, data)
    cursor.execute(sql, (0, data["id"],))
    report = cursor.fetchone()
    connection.close()

    if not report:
        report = ["", "", 0,]

    return json.dumps(report)


# http://127.0.0.1:5000/api/associates/amenities
@app.route("/api/associates/amenities", methods=["POST"])
def api_associates_amenities():
    data = json.loads(request.data.decode())

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    sql = """
SELECT
	COUNT(*) total
FROM missing m
INNER JOIN amenities a ON a.amenity_name = m.missingstuffs
WHERE
	a.amenity_name=?
;"""
    # print(sql, data)
    cursor.execute(sql, (data["amenity"],))
    report = cursor.fetchone()
    connection.close()

    if not report:
        report = [0,]

    return json.dumps(report)


# http://127.0.0.1:5000/api/configs/list
@app.route("/api/configs/list", methods=["POST"])
def api_configs_list():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT config_name name, config_value value, config_notes FROM configs WHERE show='Y' ORDER BY config_name;")
    data = cursor.fetchall()
    connection.close()

    # return json.dumps(data)
    r = Response(response=json.dumps(data), status=200, mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r


# http://127.0.0.1:5000/api/amenities/list
@app.route("/api/amenities/list", methods=["POST"])
def api_amenities_list():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT amenity_id id, amenity_name name FROM amenities WHERE deleted=0 ORDER BY amenity_name COLLATE NOCASE;")
    data = cursor.fetchall()
    connection.close()

    return json.dumps(data)


# http://127.0.0.1:5000/api/amenities/remove
@app.route("/api/amenities/remove", methods=["POST"])
def api_amenities_remove():
    data = json.loads(request.data.decode())

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE amenities SET deleted=1 WHERE amenity_id=?", (data["id"],))
    connection.commit()
    connection.close()

    return "Amenity deleted"


# http://127.0.0.1:5000/api/amenities/save
@app.route("/api/amenities/save", methods=["POST"])
def api_amenities_save():
    data = json.loads(request.data.decode())
    id = str(uuid.uuid4()).upper()

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    fields = (id, data["name"].upper(), 0,)
    cursor.execute("INSERT INTO amenities VALUES (?, ?, ?)", fields)
    connection.commit()
    connection.close()

    return "Amenity saved: "+data["name"]


# http://127.0.0.1:5000/api/amenities/import
@app.route("/api/amenities/import", methods=["POST"])
def api_amenities_import():
# get list of all amenities
# for each amenity
# if does not exist in destination
# insert
    connection = sqlite3.connect(DATABASE)
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
    connection.close()
    return json.dumps(data)


if __name__ == "__main__":
    # python3 housekeeping.py >> log.txt 2>&1 &
    # ps aux | grep housekeeping
    app.run(host="0.0.0.0", port=5000, debug=True)
