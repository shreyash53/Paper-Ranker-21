from flask import Blueprint, render_template, request
from search.controller import paper_add, paper_search
from flask_cors import cross_origin
from globe_search.apiengine import PaperCollector

blueprint = Blueprint("Search", __name__, url_prefix="/paper")

@blueprint.route("/search", methods=["GET"])
@cross_origin()
def search():
    if len(request.args) == 0:
        return render_template("search/search.html", papers=[])
    else:
        papers=paper_search(request.args)
        print(papers)
        return render_template("search/search.html", paper_list=papers)

@blueprint.route("/add", methods=["POST"])
def add():
    return paper_add(request.json)