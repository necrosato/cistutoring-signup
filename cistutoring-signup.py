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

## these are the settings for Spring 2018
#year = 2018
#month = 4
#day = 2
#start_hour = 8
#end_hour = 20
#num_days = (10*7)
#weekends = False
#populate_events_table(cursor, year, month, day, start_hour, end_hour, num_days, weekends)


 
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
    query = "SELECT * from users where name='Naookie Sato'"
    cursor.execute(query)
    print(valid_user(cursor, 'nsato@cistutoring.com'))
    print(valid_password(cursor, 'nicholasyanez@icloud.com', 'goodpassword'))
    print(is_reserved(cursor, '2018-10-10 12:30:00', 1))
    return "SQL TEST"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
