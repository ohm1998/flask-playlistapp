from functools import wraps
from flask import jsonify,session

def check_extension(filename):
	return filename.split(".")[-1].lower()=='mp3'

def login_required(func):
	@wraps(func)
	def inner(*args, **kwargs):
		try:
			if "username" in session.keys():
				return func(*args, **kwargs)
			else:
				print("Not Authorized")
				return "Not authorized to access this page"
		except Exception as e:
			return jsonify({
				"status" : "fail",
				"error" : str(e)
				})
	return inner