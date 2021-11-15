import requests
import json

class PaperCollector:
    def __init__(self):
        self.url = "https://dblp.org/search/publ/api"

    def fetch_papers(self, keyword, hits=1000):
        query = dict()
        query["q"] = keyword
        query["h"] = hits
        query["format"] = "json"
        query_result = requests.get(self.url, params=query).json()
        result = dict()
        result["code"] = query_result["result"]["status"]["@code"]
        result["papers"] = []
        count = 0
        for paper in query_result["result"]["hits"]["hit"]:
            if(paper["info"]["type"] == "Conference and Workshop Papers"):
                result["papers"].append(paper)
                count = count+1
        result["hits"] = count
        return result 

