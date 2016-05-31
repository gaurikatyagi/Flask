from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route('/')
def upload_file():
    return render_template("file_upload.html")


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return 'file uploaded successfully'
    else:
        return 'Try again'


if __name__ == '__main__':
    app.run(debug=True)