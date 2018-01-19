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
    print(is_unreserved(cursor, "2018-3-16 19:30:00"))
    event_reserve(cursor, "2018-3-16 19:30:00", 1)
    print(is_reserved(cursor, "2018-3-16 19:30:00"))
    user_change_password(cursor, "nicholasyanez@icloud.com","goodpassword")
    conn.commit() # this is important to save changes to the db, must include
    return "SQL TEST"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
