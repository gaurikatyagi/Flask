from flask import Flask, render_template, request, url_for, flash, session, redirect, g
import os
from process_data import find_csv_filenames

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(["xlxs", "xls", "csv"])
UPLOAD_FOLDER = os.path.dirname(os.path.abspath( __file__ ))
USERNAME = "admin"
PASSWORD = "gt"
SECRET_KEY = "development key"

app.config.from_object(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def upload_file():
    return render_template("home_screen.html")


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        # check if the post request has the file part
        session["success"] = False
        if 'file' not in request.files:
            flash('No file part')
            return render_template("file_upload.html")
        # if user does not select file, browser also
        # submit a empty part without filename
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return render_template("file_upload.html")
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # flash("File Uploaded")
            session["success"] = True
            return redirect(url_for("csvfiles"))
            # return render_template("show_entries.html")
        else:
            flash("Wrong filetype")
            return render_template("file_upload.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            error = "Invalid Username"
        elif request.form["password"] != app.config["PASSWORD"]:
            error = "Invalid Password"
        else:
            session["logged_in"] = True
            flash(message = "You are now logged in")
            return render_template("file_upload.html")
    return render_template("login.html", error = error)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash(message = "You're now logged out")
    return redirect(url_for("upload_file"))

@app.route("/csvfiles")
def csvfiles():
    file_names = find_csv_filenames()
    entries = [dict(file = index, text = row) for index, row in enumerate(file_names)]
    flash("File Uploaded")
    return render_template("show_entries.html", entries = entries)

@app.route("/analyze", methods = "POST")
def analyze():
    return "Hey"

if __name__ == '__main__':
    app.run(debug=True)