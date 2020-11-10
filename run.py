from flask import Flask, request,render_template,redirect,url_for,send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_mysqldb import MySQL
from helpers import *
from config import *

app = Flask(__name__)
app.config.from_object(config)

mysql = MySQL(app)

@app.route('/')
def index():
	return redirect(url_for('login'))

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
			cur.execute(query)
			mysql.connection.commit()
			
			return redirect(url_for('home'))
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
				return redirect(url_for("home"))
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
				new_song_id = rv[0][0]
				title = request.form['title']
				artist = request.form['artist']
				album = request.form['album']
				user_id = session['user_id']
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(new_song_id)+'.mp3'))
				query = "INSERT INTO `songs`(`title`, `artist`, `album`,`user_id`) VALUES ('{}','{}','{}','{}')".format(title,artist,album,user_id )
				cur.execute(query)
				mysql.connection.commit()
				return redirect(url_for('home'))
			else:
				return 'Only Mp3 files Supported (Uploaded file type is: '  + file.filename.split(".")[-1] + ' )'
	except Exception as e:
		return str(e)


@app.route('/home')
@login_required
def home():
	d = {}
	d['username'] = session['username']
	print(d)
	return render_template('home.html',data=d)

@app.route('/song/<songid>')
def song(songid):
	cur = mysql.connection.cursor()
	query = "select * from songs where id =" + str(songid)
	cur.execute(query)
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

@app.route('/get_song_by_user',methods=['GET','POST'])
@login_required
def get_song_by_user():
	query = ""
	cur = mysql.connection.cursor()
	try:
		print("here")
		substr = request.form["substr"]
		query = "select * from songs where user_id="+str(session['user_id'])+" and ( title like '%"+substr+"%' or artist like '%"+substr+"%' or album like '%"+substr+"%')"
	except Exception as e: #can be replaced with name error
		query = "select * from songs where user_id="+str(session['user_id'])
	finally:
		cur.execute(query)
		res = cur.fetchall()
		return jsonify(res)

@app.route('/delete_song/<song_id>',methods=['GET','POST'])
@login_required
#While deleting the song check if the song is uploaded by the same user or not
def delete_song(song_id):
	file_path = "./"+app.config['UPLOAD_FOLDER']+"/"+str(song_id)+".mp3"
	if(os.path.exists(file_path)):
		print("exists")
		cur = mysql.connection.cursor()
		query = "delete from songs where id="+str(song_id)
		cur.execute(query)
		mysql.connection.commit()
		os.remove(file_path)
		return redirect(url_for("home"))

if __name__ == "__main__":
	app.run(debug=True)
