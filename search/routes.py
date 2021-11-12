from flask import Blueprint, render_template, request

from search.controller import paper_add, paper_search

blueprint = Blueprint("Search", __name__, url_prefix="/paper")

@blueprint.route("/")
def home():
	return render_template("index.html")
    #return render_template("search.html")

@blueprint.route("/search", methods=["GET"])
def search():
    return paper_search(request.args)


@blueprint.route("/add", methods=["POST"])
def add():
    return paper_add(request.json)
