#!/usr/bin/python3
from flask import Flask, render_template
from flaskext.mysql import MySQL
from flask_table import Table, Col
from datetime import datetime, timedelta

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

@app.route("/signin")
def signin():
    return render_template('signin.html')

display_weeknum = 0
@app.route("/")
@app.route("/schedule")
def schedule():
    conn = mysql.connect()
    cursor = conn.cursor()
    tdelt = timedelta(weeks=display_weeknum)
    dt = datetime.today()+tdelt
    days = get_week_events(cursor, dt)
    conn.close()

    ws = week_begin(dt).strftime('%Y-%m-%d')
    we = week_end(dt).strftime('%Y-%m-%d')
    return render_template('schedule.html',days=days[1:6], week_start=ws, week_end=we)

@app.route("/week-next")
def schedule_week_next():
    global display_weeknum
    display_weeknum+=1
    return schedule()
@app.route("/week-prev")
def schedule_week_prev():
    global display_weeknum
    display_weeknum-=1
    return schedule()

@app.route("/signup")
def signup():
    return render_template('signup.html')
 

@app.route("/sqltest")
def sqltest():
    conn = mysql.connect()
    cursor = conn.cursor()

    #events = datetime_range_strings(2018, 1, 23, 18, 0, 19, 0, 1)
    #event_reserve_range(cursor, 1, events)
    #days = get_week_events(cursor, datetime.today()+timedelta(weeks=1))

    conn.commit() # this is important to save changes to the db, must include
    conn.close()
    return schedule()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
