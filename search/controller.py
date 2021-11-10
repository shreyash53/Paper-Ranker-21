from flask.json import jsonify

from constants import HTTP_STATUS_BAD_REQUEST, HTTP_STATUS_OK
from .models import Paper


def paper_add_helper(request_data):
    paper_structure = {
        "title": None,
        "author": None,
        "description": None,
        "conference": None,
        "year": None,
    }
    for key in paper_structure.keys():
        if key in request_data:
            paper_structure[key] = request_data[key]

    paper = Paper(**paper_structure)
    try:
        paper = paper.save()
    except Exception as e:
        print(e)
        paper = None
    return paper


def paper_add(request_data):
    paper = paper_add_helper(request_data)
    if not paper:
        return "Some Error Occured", HTTP_STATUS_BAD_REQUEST
    return paper.getObject(), HTTP_STATUS_OK


def paper_search():
    return jsonify([paper.getObject() for paper in Paper.objects]), 200
