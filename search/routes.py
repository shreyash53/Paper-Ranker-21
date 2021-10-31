from flask import Flask, render_template, jsonify, request
from flask import Blueprint

blueprint = Blueprint('Search', __name__)

@blueprint.route("/")
def home():
	return render_template("search.html")

@blueprint.route("/search", methods=['POST'])
def search():
	print(request.form.get('search_key'))
	return jsonify({"data" : "success"}), 200
