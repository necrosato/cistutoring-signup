#!/usr/bin/python3
import os
from flask import Flask, render_template, session, redirect, escape, request, url_for
from flaskext.mysql import MySQL
from datetime import datetime, timedelta

from users_functions import *
from events_functions import *

app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)
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

@app.route("/")
@app.route("/schedule")
def schedule():
    if 'display_weeknum' in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        tdelt = timedelta(weeks=session['display_weeknum'])
        dt = datetime.today()+tdelt
        days = get_week_events(cursor, dt)
        conn.close()
        ws = week_begin(dt).strftime('%Y-%m-%d')
        we = week_end(dt).strftime('%Y-%m-%d')
        return render_template('schedule.html',days=days[1:6], week_start=ws, week_end=we)
    else:
        session['display_weeknum']=0
        return schedule()

@app.route("/week-next")
def schedule_week_next():
    if 'display_weeknum' in session:
        session['display_weeknum']+=1
    return redirect(url_for('schedule'))
@app.route("/week-prev")
def schedule_week_prev():
    if 'display_weeknum' in session:
        session['display_weeknum']-=1
    return redirect(url_for('schedule'))

@app.route("/signup")
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
