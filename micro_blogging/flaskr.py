import sqlite3
from flask import Flask, request, session, redirect, g, url_for, abort, render_template, flash

from contextlib import closing
##The closing() helper function allows us to keep a connection open for the duration
##of the with block. The open_resource() method of the application object supports that
##functionality out of the box, so it can be used in the with block directly. This function
##opens a file from the resource location (your flaskr folder) and allows you to read from
##it. We are using this here to execute a script on the database connection.

#database configuration
DATABASE = "/tmp/microblog.db"
DEBUG = True
SECRET_KEY = "development key"
USERNAME = "admin"
PASSWORD = "defaultpass"

#intitialize database
"""
need a schema
that tells them how to store that information. So before starting the server for the first
time it's important to create that schema.
Such a schema can be created by piping the schema.sql file into the sqlite3 command as
follows:
sqlite3 /tmp/flaskr.db < schema.sql
"""
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource("schema.sql", mode = "r") as f:
            db.cursor().executescript(f.read())
        db.commit()

#main application
app = Flask(__name__)
app.config.from_object(__name__)
##from_object() will look at the given object (if it's a string it will import it) and then
##look for all uppercase variables defined there

def connect_db():
    return sqlite3.connect(app.config["DATABASE"])

@app.before_request
def before_request():
    #We store our current database connection on the special g object that Flask provides
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    """
    after_request() are called after a request and passed the response that will be sent to the client. They have to
    return that response object or a different one. They are however not guaranteed to be executed if an exception is
    raised, this is where functions marked with teardown_request() come in. They     get called after the response has
    been constructed. They are not allowed to modify the request, and their return values are ignored. If an exception
    occurred while the request was being processed, it is passed to each function; otherwise, None is passed in.
    """
    db = getattr(object = g, name = "db", default = None)
    if db is not None:
        db.close()

@app.route("/")
def show_entries():
    cursor = g.db.execute("select title, text from entries order by id desc")
    entries = [dict(title = row[0], text = row[1]) for row in cursor.fetchall()]
    return render_template(template_name_or_list = "show_entries.html", entries = entries)

if __name__ == "__main__":
    init_db()
    app.run()