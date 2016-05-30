#This program is used to generate the urls and help the user understand how the urls will look to the user when
# accessing this application on a website

from flask import Flask, url_for, redirect, session
from flask import request
app = Flask(__name__)

@app.route("/")
#By default route only answers to get requests
def index():
    return "I am the home page"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        session["username"] = request.form["username"]
    return redirect(url_for('index'))
    return """
    <form action="" method="post">
    <p><input type=text name=username>
    <p><input type=submit value=Login>
    </form>
    """

@app.route("/logout")
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for("index"))

@app.route("/profile/<username>")
def profile(username):
    return "Welcome %s"%username

#changing the way route functions by adding post method of hhtp as well to the acceptable form of input
@app.route("/login_new", methods = ["GET", "POST"])
def login_new():
    if request.metod == "POST":
        #do_the_login
        if valid_login(request.form['username'],
                       request.form['password']):
            return redirect(url_for("profile", username = "Gaurika"))
        else:
            error = 'Invalid username/password'
        # the code below is executed if the request method
        # was GET or the credentials were invalid
        return render_template('login.html', error=error)

# with app.test_request_context():
#     """
#     test_request_context method tells flask to behave as though it is handling a request even though we are interacting
#     with the python terminal by calling the program without activating the server.
#     We see the urls like this and use them like this when we want to use them in aprogram and do not want to hardcode
#     them, allowing us to change the URLs in one go, rather than having to change them evrywhere in the code.
#
#     """
#     print url_for("index")
#     print url_for("login")
#     print url_for("login", next = "/")
#     print url_for("profile", username = "Gaurika")
#     print url_for("login_new", _method="POST")
#     print url_for("login_new", _method="GET")

with app.test_request_context("login_new", method = "POST"):
    assert request.path == "/login_new"
    assert request.method == "POST"