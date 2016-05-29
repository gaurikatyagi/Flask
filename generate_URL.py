#This program is used to generate the urls and help the user understand how the urls will look to the user when accessing this application on a website

from flask import Flask, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return "I am the home page"

@app.route("/login")
def login():
    return "Please enter your username and password"

@app.route("/profile/<username>")
def profile(username):
    return "Welcome %s"%username

with app.test_request_context():
    print url_for("index")
    print url_for("login")
    print url_for("login", next = "/")
    print url_for("profile", username = "Gaurika")