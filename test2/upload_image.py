from flask import Flask

UPLOAD_FOLDER = './static'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import os
#import magic
import urllib.request
# from app import app
from flask import Flask, flash, request, redirect, render_template,url_for,jsonify,json
from werkzeug.utils import secure_filename
from flask_cors import CORS


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
CORS(app)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	# return render_template('upload.html')
	return render_template("online-editor.html")

@app.route('/', methods=['POST'])
def upload_file():
	# print("here")
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
			print(file_path)
			file.save(file_path)
			flash('File successfully uploaded')
			message=[file_path]
			resp=jsonify(message)
			resp.status_code=200
			return resp
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True)