from flask import Blueprint, render_template, request
from search.controller import paper_add, paper_search
from flask_cors import cross_origin
from globe_search.apiengine import PaperCollector
from flask_login import current_user
from math import ceil
from flask_paginate import Pagination, get_page_parameter

blueprint = Blueprint("Search", __name__, url_prefix="/paper")

@blueprint.route("/search", methods=["GET"])
@cross_origin()
def search():
    loggedIn = False
    if current_user and current_user.is_authenticated:
        loggedIn = True
    if len(request.args) == 0 or request.args["q"] == "":
        return render_template("search/search.html", papers=[], loggedIn=loggedIn, value="", size=0, pagination=None)
    else:
        page = request.args.get(get_page_parameter(), type=int, default=1)
        papers=paper_search(request.args)
        size = len(papers)
        pagination = Pagination(page=page, total=size, per_page=10, search=False, record_name='paper_list')
        papers = papers[(page-1)*10:(page-1)*10+10:] 
        return render_template("search/search.html", paper_list=papers, pagination=pagination,loggedIn=loggedIn, value=request.args["q"], size=ceil(size/10))

@blueprint.route("/add", methods=["POST"])
def add():
    return paper_add(request.json)