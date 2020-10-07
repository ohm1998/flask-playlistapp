from flask import Flask, request,render_template,redirect,url_for,send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_mysqldb import MySQL
from helpers import *

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
			#print(query)
			cur.execute(query)
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
			session.clear()
			username = request.form['username']
			password = request.form['password']
			cur = mysql.connection.cursor()
			query = "select * from login where username = '{}'".format(username)
			cur.execute(query);
			rv = cur.fetchall()
			if(rv[0][2]==password):
				session['user_id'] = rv[0][0]
				session['username'] = rv[0][1]
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

@app.route('/logout')
def logout():
	session.clear()
	print(url_for("login"))
	return redirect(url_for("login"))


@app.route('/upload',methods=['GET','POST'])
@login_required
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
				cur = mysql.connection.cursor()
				query = ''' 
				SELECT `AUTO_INCREMENT`
				FROM  INFORMATION_SCHEMA.TABLES
				WHERE TABLE_SCHEMA = 'nptel'
				AND   TABLE_NAME   = 'songs';
				'''
				cur.execute(query)
				rv = cur.fetchall()
				print(rv)
				new_song_id = rv[0][0]
				print(new_song_id)
				title = request.form['title']
				artist = request.form['artist']
				album = request.form['album']
				print("here")
				query = "INSERT INTO `songs`(`title`, `artist`, `album`) VALUES ('{}','{}','{}')".format(title,artist,album)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(new_song_id)+'.mp3'))
				cur.execute(query)
				mysql.connection.commit()
				return 'file Uploaded'
			else:
				return 'Only Mp3 files Supported (Uploaded file type is: '  + file.filename.split(".")[-1] + ' )'
	except Exception as e:
		return str(e)


@app.route('/song/<songid>')
def song(songid):
	print(songid)
	cur = mysql.connection.cursor()
	query = "select * from songs where id =" + str(songid)
	cur.execute(query)
	#print(help(cur))
	rv = cur.fetchone()
	if(rv==None):
		return {
		"status" : "fail",
		"msg" : "no song found"
		}
	else:
		d = {}
		d['song_id'] = songid
		d['title'] = rv[1]
		d['artist'] = rv[2]
		d['album'] = rv[3]
		return render_template('song.html',data=d)

@app.route('/get_song/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


if __name__ == "__main__":
	app.run(debug=True)
