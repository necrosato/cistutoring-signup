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

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        if (request.form['inputEmail'] != (None or '') and
        request.form['inputPassword'] != (None or '')):
            conn = mysql.connect()
            cursor = conn.cursor()
            if (valid_user(cursor, request.form['inputEmail']) and 
            valid_password(cursor, request.form['inputEmail'], request.form['inputPassword'])):

                user = user_get(cursor, request.form['inputEmail'])
                session['logged_in']=True
                session['user_id']=user[0]
                session['user_name']=user[1]
                session['user_email']=user[2]
                session['user_phone']=user[3]
                session['user_priv']=user[4]
                session['display_weeknum']=0
                return redirect(url_for('schedule'))
    return render_template('signin.html')

@app.route("/")
@app.route("/schedule")
def schedule():
    if 'logged_in' in session:
        if session['logged_in']==True:
            conn = mysql.connect()
            cursor = conn.cursor()
            tdelt = timedelta(weeks=session['display_weeknum'])
            dt = datetime.today()+tdelt
            days = get_week_events(cursor, dt)
            names = user_get_names(cursor)
            names_dict = {}
            for name in names:
                names_dict[name[0]]=name[1]
            conn.close()
            ws = week_begin(dt).strftime('%Y-%m-%d')
            we = week_end(dt).strftime('%Y-%m-%d')
            return render_template('schedule.html', session=session, days=days[1:6], week_start=ws, week_end=we, names_dict=names_dict)
    return redirect(url_for('signin'))
        

@app.route("/update_schedule", methods=["GET", "POST"])
def schedule_modify():
    if 'logged_in' in session and request.method == "POST":
        if session['logged_in']==True:
            conn = mysql.connect()
            cursor = conn.cursor()
            if session['user_priv'] == 0:
                for val in request.form:
                    if is_unreserved_id(cursor, val) and request.form[val] == 'reserve_once':
                        event_reserve_id(cursor, val, session['user_id'])
                    elif is_reserved_id(cursor, val, session['user_id']) and request.form[val] == 'unreserve':
                        event_unreserve_id(cursor, val)
            elif session['user_priv'] == 1:
                for val in request.form:
                    if request.form[val] == 'reserve_once':
                        event_reserve_id(cursor, val, session['user_id'])
                    elif request.form[val] == 'unreserve':
                        event_unreserve_id(cursor, val)
            conn.commit()                
            conn.close()
    return redirect(url_for('schedule'))

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

@app.route("/some_shit")
def some_shit():
    conn = mysql.connect()
    cursor = conn.cursor()
    #days = datetime_range_strings(2018, 1, 29, 17, 0, 18, 0, 1, weekends=False, weekly=True)
    #event_reserve_range(cursor, 4, days, force=True)
    conn.commit()
    conn.close()
    return "some_shit"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)


