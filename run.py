from flask import Flask, request, jsonify,render_template,redirect,url_for,send_from_directory,session
from werkzeug.utils import secure_filename
import os



app = Flask(__name__)


UPLOAD_FOLDER = './uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from helpers import *


@app.route('/')
def index():
	session['count']  = session['count'] + 1
	return 'hello app is running count : ' + session['count']


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
