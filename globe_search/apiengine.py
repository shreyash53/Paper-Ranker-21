import requests
from search.controller import conference_add, getConference

from .scrape import get_conference_rank


class PaperCollector:
    def __init__(self):
        self.url = "https://api.semanticscholar.org/graph/v1/paper/search"

    def fetch_papers(self, keyword, limit=100, offset=0):
        query = dict()
        query["query"] = keyword
        query["offset"] = offset
        query["limit"] = limit
        query["fields"] = "url,venue,title,abstract,year,authors"
        result = requests.get(self.url, params=query).json()
        # return json.dumps(result)
        return result

    def fetch_papers_with_ranks(self, keyword, limit=100, offset=0):
        paper_dict = self.fetch_papers(keyword, limit=limit, offset=offset)
        result = dict()
        result["papers"] = []
        count = 0
        if "data" not in paper_dict:
            return None
        for paper in paper_dict["data"]:
            conference_ = getConference(paper["venue"])
            if conference_:
                result["papers"].append(conference_)
                result["conference"] = conference_  # storing the fetched conference obj
                count = count + 1
            else:
                rank = get_conference_rank(paper["venue"])
                if rank != "Not found":
                    paper["rank"] = rank
                    result["papers"].append(paper)
                    count = count + 1
                else:
                    pass
                    # add the conference using
                    # conference_add(conference_name, conference_rank, conference_abbr)

                    # then bind object
                    # result['conference'] = conference_

        result["total"] = count
        # return json.dumps(result)
        return result
