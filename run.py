from flask import Flask, request, jsonify,render_template,redirect,url_for,send_from_directory,session
from werkzeug.utils import secure_filename
import os
from helpers import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'


UPLOAD_FOLDER = './uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
	if 'count' in session.keys():
		session['count'] = session['count'] + 1
	else:
		session['count'] = 0
	return 'hello app is running count : ' + str(session['count'])


@app.route('/upload',methods=['GET','POST'])
def upload():
	try:
		if request.method == 'GET':
			return render_template('upload.html')
		elif request.method == 'POST':
			if 'file' not in request.files:
				return 'No file Uploaded'
			file = request.files['file']
			if check_extension(file.filename):	
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				return 'file Uploaded'
			else:
				return 'Only Mp3 files Supported (Uploaded file type is: '  + file.filename.split(".")[-1] + ' )'
	except Exception as e:
		print(e)
		return str(e)



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


if __name__ == "__main__":
	app.run(debug=True)
