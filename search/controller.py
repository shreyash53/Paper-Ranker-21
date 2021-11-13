from constants import HTTP_STATUS_BAD_REQUEST, HTTP_STATUS_OK
from flask.json import jsonify
from globe_search.apiengine import PaperCollector
from mongoengine.queryset.visitor import Q 
from search.models import Conference, Paper, RankMeta
from globe_search.scrape import get_conference_rank_from_web

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

def map_ranks(paper_dict):
    result = dict()
    result["papers"] = []
    count = 0
    if "data" not in paper_dict:
        return None
    for paper in paper_dict["data"]:
        conference_ = getConference(paper["venue"])
        if conference_:
            paper["conference"] = conference_
            result["papers"].append(paper) 
            count = count + 1
        else:
            rank = get_conference_rank_from_web(paper["venue"])
            if rank != "Not found":
                conference_ = conference_add(rank["name"],rank["rank"],paper["venue"])
                paper["conference"] = conference_
                result["papers"].append(paper)
                count = count + 1
    result["total"] = count
    return result

def paper_add(request_data):
    paper = paper_add_helper(request_data)
    if not paper:
        return "Some Error Occured", HTTP_STATUS_BAD_REQUEST
    return paper.getObject(), HTTP_STATUS_OK

def paper_search_helper(params, paper_result_set):
    collector = PaperCollector()
    temp = collector.fetch_papers(params["query"])
    fetched_papers = map_ranks(temp)
    for paper_ in fetched_papers["papers"]:
        paper_obj = dict(paper_structure)
        paper_obj = Paper(
            title=paper_["title"],
            description=paper_["abstract"],
            year=paper_["year"],
            url=paper_["url"],
            author=",".join([author["name"] for author in paper_["authors"]]),
            conference=paper_["conference"],
            rank=map_paper_rank(paper_['conference'].rank)
        )
        if not Paper.objects.filter(Q(title=paper_["title"])):
            paper_result_set.insert(paper_obj)

def paper_search(params):
    paper_result_set = Paper.objects.filter(
        Q(title__icontains=params["query"]) | Q(description__icontains=params["query"])
    )
    if paper_result_set.count() < 5:
        # do global search
        paper_search_helper(params, paper_result_set)

    paper_result_set = paper_result_set.order_by('rank')
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
    return conference_.save()

def map_paper_rank(rank_):
    rank_meta = RankMeta.objects(conference_rank=rank_).get()
    if rank_meta:
        return rank_meta.get_rank_value()
    return rank_