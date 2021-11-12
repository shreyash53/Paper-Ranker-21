import requests

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