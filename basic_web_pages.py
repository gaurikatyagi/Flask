"""
gaurika@gaurika-Aspire-E1-472G:~$ ps -fA | grep python
gaurika   3532  1186  0 07:31 ?        00:00:00 /home/gaurika/Enthought/Canopy_64bit/User/bin/python2.7 /home/gaurika/PycharmProjects/First/flask_1.py
gaurika   4225  4072  1 07:38 ?        00:00:01 /home/gaurika/Enthought/Canopy_64bit/User/bin/python2.7 /home/gaurika/.local/share/umake/ide/pycharm/helpers/pydev/pydevconsole.py 36470 43958
gaurika   4358  4340  0 07:40 pts/1    00:00:00 grep --color=auto python
gaurika@gaurika-Aspire-E1-472G:~$ sudo kill -9 PID
[sudo] password for gaurika:
kill: failed to parse argument: 'PID'
gaurika@gaurika-Aspire-E1-472G:~$ sudo kill -9 3532
gaurika@gaurika-Aspire-E1-472G:~$ ^C
gaurika@gaurika-Aspire-E1-472G:~$

"""

from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Index!"

@app.route("/hello")
def hello():
    return "Hello world"

@app.route("/members/") #call this with or without the trailing slash at the end
def members():
    return "members"

@app.route("/user/<username>") #if you call it with a trailing slash at the end, it will throw an error
def show_user_profile(username):
    return "User is %s"%username

if __name__ == '__main__':
    # name = "Gaurika"
    app.debug = True #changing the app will reload the server automatically
    app.run()