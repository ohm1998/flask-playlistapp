from flask import Flask, request, jsonify,render_template,redirect,url_for

from helpers import *


app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp3'}


@app.route('/')
def index():
	return 'hello app is running'


@app.route('/upload')
def upload():



# class data():
# 	def __init__(self):
# 		self.curr_matrix = np.zeros((6,7))
# 		self.moves = 1
# 	def reinit(self):
# 		self.curr_matrix = np.zeros((6,7))
# 		self.moves = 1

# user = data()

# @app.route('/')
# def index():
#     return jsonify({'status': 'Online'}), 200


# @app.route('/game/')
# def game():
# 	return render_template('game.html',data = user.curr_matrix)

# @app.route('/start')
# def start():	
# 	user.reinit()
# 	return jsonify({'response' : 'READY' , 'msg' : 'Game Reset'}),200


# @app.route('/get_matrix')
# def get_matrix():
# 	return jsonify({'matrix' : user.curr_matrix.tolist()})


# @app.route('/move',methods=['POST'])
# def move():
# 	move_by = 1
# 	if(user.moves%2==0):
# 		move_by = 2 # Move by red
# 	col =  int(request.form.get('column'))
# 	if(check_valid(user.curr_matrix,col)):
# 		user.curr_matrix = change_matrix(user.curr_matrix,col,move_by)
# 		user.moves = user.moves + 1
# 		winner = check_win_row(user.curr_matrix)
# 		player_win = False
# 		if(winner['winner']):
# 			player_win = winner['player']
# 		winner = check_win_col(user.curr_matrix)
# 		if(winner['winner']):
# 			player_win = winner_player
# 		return jsonify({'response' : 'Valid','matrix' : user.curr_matrix.tolist(),'winner' : player_win})
# 	return jsonify({'response' : 'Invalid','matrix' : user.curr_matrix.tolist()})


if __name__ == "__main__":
	app.run()
