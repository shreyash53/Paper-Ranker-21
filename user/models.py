from flask import Flask, jsonify, request
from mongoengine import *
import uuid
import json

connect('paper_ranker_new',host='localhost',port=27017)

class User(Document):
	username = StringField(required=True)
	email = EmailField(unique=True)
	password = StringField(required=True)

	meta = {
		"indexes" : ["email"]
	}

	def json(self):
		user = {
			"name" : self.username,
			"email": self.email
		}
		return json.dumps(user)


