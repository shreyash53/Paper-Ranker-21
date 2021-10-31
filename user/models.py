from flask import Flask, jsonify, request
from extensions import db
import uuid

class User:
	def signup(self):
		user = {
			"_id" : uuid.uuid4().hex,
			"name": request.form.get('name'),
			"password": request.form.get('password'),
			"email": request.form.get('email')
		}
		db.users.insert_one(user)
		return jsonify(user), 200