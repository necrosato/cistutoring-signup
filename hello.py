from flask import Flask
app = Flask(__name__)
 
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/signup")
def signup():
    return "Here is where a new tutee can register"
 
@app.route("/reserve")
def reserve():
    return "Here is where a new tutee can reserve"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
