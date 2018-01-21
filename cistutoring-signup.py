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


class TimeTable(Table):
    mon = Col('Monday')
    tue = Col('Tuesday')
    wed = Col('Wednesday')
    thu = Col('Thursday')
    fri = Col('Friday')
class TableRow(object):
    def __init__(self,mon,tue,wed,thu,fri):
        self.mon = mon
        self.tue = tue
        self.wed = wed
        self.thu = thu
        self.fri = fri

@app.route("/")
@app.route("/signin")
def signin():
    return render_template('signin.html')

@app.route("/schedule")
def schedule():
    conn = mysql.connect()
    cursor = conn.cursor()
    days = get_week_events(cursor, datetime.today()+timedelta(weeks=0))
    conn.close()
    return render_template('schedule.html',days=days)

@app.route("/signup")
def signup():
    return render_template('signup.html')
 

@app.route("/sqltest")
def sqltest():
    conn = mysql.connect()
    cursor = conn.cursor()
    days = get_week_events(cursor, datetime.today()+timedelta(weeks=1))
    trs = [[] for i in range(24)]
    for day in days:
        for i in range(len(day)):
            trs[i].append((day[i][1].strftime('%I:%M %p')+("-  OPEN  -" if day[i][3]==None else "-  RSVD  -")))
    trsn = []
    for tr in trs:
        trsn.append(TableRow(*tr))

    conn.commit() # this is important to save changes to the db, must include
    conn.close()
    return (TimeTable(trsn).__html__())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
