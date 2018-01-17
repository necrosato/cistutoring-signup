from flask import Flask, render_template
app = Flask(__name__)
 
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
