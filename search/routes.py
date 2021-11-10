from flask import Flask, render_template, jsonify, request
from flask import Blueprint
from search.controller import paper_add, paper_search


blueprint = Blueprint('Search', __name__, url_prefix='/paper')

@blueprint.route("/")
def home():
	return render_template("search.html")

@blueprint.route("/search", methods=['POST'])
def search():
	return paper_search()

@blueprint.route("/add", methods=['POST'])
def add():
	return paper_add(request.json)
