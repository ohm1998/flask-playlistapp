from flask import Flask, request,jsonify,render_template,redirect,url_for,send_from_directory,session
from werkzeug.utils import secure_filename
import os
from helpers import *
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'nptel'

mysql = MySQL(app)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def index():
	if 'count' in session.keys():
		session['count'] = session['count'] + 1
	else:
		session['count'] = 0
	return 'hello app is running count : ' + str(session['count'])


@app.route('/db')
def db():
	#print(help(mysql))
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM event")
	rv = cur.fetchall()
	#print(rv)
	return str(rv)

@app.route('/register',methods=['GET','POST'])
def register():
	try:
		if request.method == 'GET':
			return render_template('register.html')
		elif request.method == 'POST':
			print("post request");
			username = request.form['username']
			password = request.form['password']
			cur = mysql.connection.cursor()
			query = "INSERT INTO `login`(`username`, `password`) VALUES ('{}','{}')".format(username,password)
			print(query)
			cur.execute(query);
			mysql.connection.commit()
			#rv = cur.fetchall()
			return jsonify({
				"status": "success",
				"msg" : "user registered successfully"
				})
	except Exception as e:
		print(e)
		return str(e)
@app.route('/login',methods=['GET','POST'])
def login():
	try:
		if request.method == 'GET':
			return render_template('login.html')
		elif request.method == 'POST':
			username = request.form['username']
			password = request.form['password']
			cur = mysql.connection.cursor()
			query = "select * from login where username = '{}'".format(username)
			print(query)
			cur.execute(query);
			rv = cur.fetchall()
			session['user_id'] = rv[0][0]
			session['username'] = rv[0][1]
			if(rv[0][2]==password):
				return jsonify({
					"status" : "success",
					"msg" : "login Successfull"
					})
			else: 
				return jsonify({
					"status": "fail",
					"msg" : "Credentials Incorrect"
					})
	except Exception as e:
		print(e)
		return str(e)




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
