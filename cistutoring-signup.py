#!/usr/bin/python3
import os
from flask import Flask, render_template, session, redirect, escape, request, url_for
from flaskext.mysql import MySQL
#from flask_wtf import RecaptchaField
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
#RECAPTCHA_PUBLIC_KEY="6Leey0IUAAAAAFnE1Uf4QQsbkLfn1HYb17IwMzNj"
#RECAPTCHA_PRIVATE_KEY="6Leey0IUAAAAAA7EG-eQxdeGewiSuKPzuvEzQKIZ"
mysql.init_app(app)

@app.route("/")
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        if (request.form['inputEmail'] != (None or '') and
        request.form['inputPassword'] != (None or '')):
            conn = mysql.connect()
            cursor = conn.cursor()
            if (valid_user(cursor, request.form['inputEmail']) and 
            valid_password(cursor, request.form['inputEmail'], request.form['inputPassword'])):
                session['logged_in']=True
                session['user_id']=user_get_id(cursor, request.form['inputEmail'])
                print(session['user_id'])
                return redirect(url_for('schedule'))
    return render_template('signin.html')

@app.route("/schedule")
def schedule():
    if 'logged_in' in session:
        if session['logged_in']==True:
            if 'display_weeknum' in session:
                conn = mysql.connect()
                cursor = conn.cursor()
                tdelt = timedelta(weeks=session['display_weeknum'])
                dt = datetime.today()+tdelt
                days = get_week_events(cursor, dt)
                conn.close()
                ws = week_begin(dt).strftime('%Y-%m-%d')
                we = week_end(dt).strftime('%Y-%m-%d')
                return render_template('schedule.html', session=session, days=days[1:6], week_start=ws, week_end=we)
            else:
                session['display_weeknum']=0
                return schedule()
    return redirect(url_for('signin'))
        

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

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if (request.form['inputEmail'] != (None or '') and
        request.form['inputName'] != (None or '') and
        request.form['inputPhone'] != (None or '') and
        request.form['inputPassword'] != (None or '') and
        request.form['inputPasswordConfirm'] != (None or '') and
        request.form['inputPassword'] == request.form['inputPasswordConfirm'] and
        request.form['g-recaptcha-response'] != (None or '')):
            conn = mysql.connect()
            cursor = conn.cursor()
            if not valid_user(cursor, request.form['inputEmail']):
                email = request.form['inputEmail']
                phone = request.form['inputPhone']
                name = request.form['inputName']
                passw = request.form['inputPassword']
                user_create(cursor, name, email, passw, phone)
                conn.commit()                
            conn.close()
            return "Successful sign up!"
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)


