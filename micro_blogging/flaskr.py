import sqlite3
from flask import Flask, request, session, redirect, g, url_for, abort, render_template, flash

#database configuration
DATABASE = "/tmp/microblog.db"
DEBUG = True
SECRET_KEY = "development key"
USERNAME = "admin"
PASSWORD = "defaultpass"

#main application
app = Flask(__name__)
app.config.from_object(__name__)
##from_object() will look at the given object (if it's a string it will import it) and then
##look for all uppercase variables defined there

def connect_db():
    return sqlite3.connect(app.config["DATABASE"])

if __name__ == "__main__":
    app.run()