from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
from bs4 import BeautifulSoup
from urllib.request import urlopen

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "https://rhul.buggyrace.net"
LINK = "https://rhul.buggyrace.net/specs/"


#
# COST
#
def cost_search():
    page = urlopen(LINK)
    html_page = page.read().decode("utf-8")
    soup = BeautifulSoup(html_page, "html.parser")
    mess = soup.get_text()
    print(soup.get_text)


#
# DATA
#
def data_search():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))

    return dict(zip([column[0] for column in cur.description], cur.fetchone())).items()


def get_buggy():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone();
    return record


# ------------------------------------------------------------
# Confirm
# ------------------------------------------------------------
def valid(item, step, id):
    value = request.form[item]
    if step == "check item":
        if not value.isdigit():
            return f"Wrong Input chief, Try Again: {value}"
        if item == "qty_wheels":
            value = int(value)
            if (value % 2) == 1:
                return f"Odd Value Detected: {value}"

    try:
        with sql.connect(DATABASE_FILE) as con:

            cur = con.cursor()

            cur.execute(
                f"UPDATE buggies set {item}=? WHERE id=?",
                (value, id)
            )

            con.commit()
            msg = "Record successfully saved"
    except:
        con.rollback()
        msg = "error in update operation"

    finally:
        con.close()
        return f"your {item} is now a {value}"

    #
    # insert
    #


def insert():
    try:
        with sql.connect(DATABASE_FILE) as con:

            cur = con.cursor()

            cur.execute("INSERT INTO buggies (qty_wheels) VALUES (?)", (4,))

            con.commit()
            msg = "Record successfully saved"
    except:
        con.rollback()
        msg = "error in update operation"

    finally:
        con.close()
        return f"your New Buggy"


# ------------------------------------------------------------
# the index page
# ------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)


# ------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
# ------------------------------------------------------------
@app.route('/new', methods=['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
        return render_template("buggy-form.html", buggy=get_buggy())
    elif request.method == 'POST':

        buggy_id = request.form["id"]

        msg1 = valid("qty_wheels", "check item", buggy_id)
        msg2 = valid("flag_color", "", buggy_id)
        msg3 = valid("power_type", "", buggy_id)
        msg11 = valid('aux_power_units', "", buggy_id)
        msg4 = valid("flag_pattern", "", buggy_id)
        msg8 = valid("flag_color_secondary", "", buggy_id)
        msg9 = valid("tyres", "", buggy_id)
        msg10 = valid("qty_tyres", "", buggy_id)

        return render_template("updated.html", msg1=msg1, msg2=msg2, msg3=msg3, msg4=msg4, msg8=msg8, msg9=msg9,
                               msg10=msg10, msg11=msg11)


@app.route('/real', methods=['POST', 'GET'])
def create_buggy2():
    if request.method == 'GET':
        return render_template("buggy-form-REAL.html")
    elif request.method == 'POST':

        msg1 = insert()

        return render_template("updated.html", msg1=msg1)


#
#
#
@app.route('/war', methods=['POST', 'GET'])
def create_war():
    if request.method == 'GET':
        return render_template("buggy-war.html", buggy=get_buggy())
    elif request.method == 'POST':

        msg1 = valid("armour", "")
        msg2 = valid('attack', "")
        msg3 = valid('qty_attacks', "")
        msg4 = valid('fireproof', "")
        msg5 = valid('insulated', "")
        msg6 = valid('antibiotic', "")
        msg7 = valid('banging', "")
        msg12 = valid('hamster_booster', "")

        return render_template("updated.html", msg1=msg1, msg2=msg2, msg3=msg3, msg4=msg4, msg5=msg5, msg6=msg6,
                               msg7=msg7, msg12=msg12)


#
# Poster
#
@app.route('/poster')
def poster():
    return render_template('poster.html')


#


# ------------------------------------------------------------
# a page for displaying the buggy
# ------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    records = cur.fetchall();
    return render_template("buggy.html", buggies=records)


# ------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
# ------------------------------------------------------------
@app.route('/edit/<buggy_id>')
def edit_buggy(buggy_id):
    print(f"I want to edit buggy #{buggy_id}")
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=?", (buggy_id,))
    record = cur.fetchone();
    return render_template("buggy-form.html", buggy=record)


# ------------------------------------------------------------
# You probably don't need to edit this... unless you want to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning
#  the data, so in effect jsonify() is rendering the data.
# ------------------------------------------------------------
@app.route('/json')
def summary():
    buggies = data_search()
    cost_search()
    return jsonify({key: val for key, val in buggies if (val != "" and val is not None)})


# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
