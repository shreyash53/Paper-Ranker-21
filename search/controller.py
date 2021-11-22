from constants import HTTP_STATUS_BAD_REQUEST, HTTP_STATUS_OK
from flask.json import jsonify
from globe_search.apiengine import PaperCollector
from mongoengine.queryset.visitor import Q 
from search.models import Conference, Paper, RankMeta
from globe_search.scrape import get_conference_rank_dict

rank_dict = get_conference_rank_dict()

paper_structure = {
    "paper_id":None,
    "title": None,
    "author": None,
    "conference": None,
    "year": None,
    "url": None,
}

def map_ranks(paper_dict):
    result = dict()
    result["papers"] = []
    count = 0
    if "papers" not in paper_dict:
        return result
    for paper in paper_dict["papers"]:
        venue = paper["info"]["venue"]
        acronym = venue.split()[0]
        conference_ = getConference(acronym)
        if conference_:
            paper["conference"] = conference_
            result["papers"].append(paper) 
            count = count + 1
        else:
            if acronym in rank_dict.keys():
                conf = rank_dict[acronym]
                conference_ = conference_add(conf["name"],conf["rank"],conf["acronym"])
                paper["conference"] = conference_
                result["papers"].append(paper)
                count = count + 1
    result["total"] = count
    return result

def paper_add_helper(request_data):
    if Paper.objects(title=request_data["title"]):
        return False
    paper_obj = dict(paper_structure)
    conference_ = getConference(request_data["conference"])
    if not conference_:
        conf = rank_dict[request_data["conference"]]
        conference_ = conference_add(conf["name"],conf["rank"],conf["acronym"])
    for key in paper_structure.keys():
        if key in request_data:
            paper_obj[key] = request_data[key]
    paper_obj["conference"] = conference_
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
    collector = PaperCollector()
    temp = collector.fetch_papers(params["q"])
    fetched_papers = map_ranks(temp)
    for paper_ in fetched_papers["papers"]:
        paper_obj = dict(paper_structure)
        authors_list = paper_["info"]["authors"]["author"]
        if not authors_list and type(authors_list) != dict:
            authors_list = []

        paper_obj = Paper(
            paper_id = paper_["@id"],
            title=paper_["info"]["title"],
            year=paper_["info"]["year"],
            url=paper_["info"]["url"],
            author=authors_list,
            conference=paper_["conference"],
            rank=map_paper_rank(paper_['conference'].rank)
        )
        if not Paper.objects.filter(Q(paper_id=paper_["@id"])):
            paper_result_set.insert(paper_obj)

def paper_search(params):
    paper_result_set = Paper.objects.filter(Q(title__icontains=params["q"]))
    if paper_result_set.count() < 5:
        # do global search
        paper_search_helper(params, paper_result_set)

    paper_result_set = paper_result_set.order_by('rank')
    return [paper_.getObject() for paper_ in paper_result_set]

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