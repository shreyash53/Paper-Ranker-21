from constants import HTTP_STATUS_BAD_REQUEST, HTTP_STATUS_OK
from flask.json import jsonify
from globe_search.apiengine import PaperCollector
from mongoengine.queryset.visitor import Q

from .models import Conference, Paper

paper_structure = {
    "title": None,
    "author": None,
    "description": None,
    "conference": None,
    "year": None,
    "url": None,
}


def paper_add_helper(request_data):
    if Paper.objects(title=request_data["title"]):
        return False
    paper_obj = dict(paper_structure)
    for key in paper_structure.keys():
        if key in request_data:
            paper_obj[key] = request_data[key]

    paper = Paper(**paper_obj)
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


def paper_search_helper(params, paper_result_set):
    fetched_papers = PaperCollector.fetch_papers_with_ranks(params)
    for paper_ in fetched_papers["papers"]:
        # paper_obj = dict(paper_structure)
        paper_obj = Paper(
            title=paper_["title"],
            desciption=paper_["abstract"],
            year=paper_["year"],
            url=paper_["url"],
            author=",".join([author["name"] for author in paper_["authors"]]),
            conference=paper_["conference"],
        )

        paper_result_set.insert(paper_obj)

    # return paper_result_set


def paper_search(params):
    paper_result_set = Paper.objects.filter(
        Q(title__icontains=params["query"]) | Q(description__icontains=params["query"])
    )
    if paper_result_set.count() < 5:
        # do global search
        paper_search_helper(params, paper_result_set)

    return jsonify([paper_.getObject() for paper_ in paper_result_set]), HTTP_STATUS_OK
    # return paper_result_set.to_json(), HTTP_STATUS_OK


def getConference(conference_name):
    conference_rs = Conference.objects.filter(
        Q(name=conference_name) | Q(abbr=conference_name)
    )
    if conference_rs:
        return conference_rs.first()
    return None


def conference_add(conference_name, conference_rank, conference_abbr):
    conference_ = Conference(
        name=conference_name, abbr=conference_abbr, rank=conference_rank
    )
    conference_.save()
    return conference_
