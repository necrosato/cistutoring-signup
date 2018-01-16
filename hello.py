from flask import Flask, render_template
app = Flask(__name__)
 
@app.route("/")
def hello():
    return render_template('signup.html')

@app.route("/signup")
def signup():
    print('test')
    return "Here is where a new tutee can register"
 
@app.route("/reserve")
def reserve():
    return "Here is where a new tutee can reserve"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
