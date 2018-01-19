from flask import Flask, render_template
from flaskext.mysql import MySQL

from users_functions import *
from events_functions import *

app = Flask(__name__)
mysql = MySQL()

#mysql config
app.config['MYSQL_DATABASE_USER'] = 'cistutoring'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cistutoring'
app.config['MYSQL_DATABASE_DB'] = 'cistutoring'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

 
@app.route("/")
@app.route("/index")
def hello():
    return render_template('index.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')
 
@app.route("/reserve")
def reserve():
    return "Here is where a new tutee can reserve"

@app.route("/sqltest")
def sqltest():
    dtt = "2018-1-15 00:00:00"
    dtt2 = "2018-1-22 00:00:00"
    #set_winter_schedule(cursor) # this works
    query = "SELECT * from events WHERE start BETWEEN %s AND %s"
    cursor.execute(query, (dtt, dtt2,))
    rows = cursor.fetchall()
    res = ''
    for row in rows:
        res = res + str(row) + "\r\n"
    conn.commit() # this is important to save changes to the db, must include
    return res

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
