import requests
from scrape import get_conference_rank
import json

class PaperCollector:
	def __init__(self):
		self.url = "https://api.semanticscholar.org/graph/v1/paper/search"

	def fetch_papers(self, keyword, limit=100, offset=0):
		query = dict()
		query["query"] = keyword
		query["offset"]= offset
		query["limit"]= limit
		query["fields"]= "url,venue,title"
		result = requests.get(self.url, params=query).json()
		return json.dumps(result)


	def fetch_papers_with_ranks(self, keyword, limit=100, offset=0):
		query = dict()
		query["query"] = keyword
		query["offset"]= offset
		query["limit"]= limit
		query["fields"]= "url,venue,title"
		papers = requests.get(self.url, params=query)
		paper_dict = papers.json()
		result = dict()
		result["data"] = []
		count = 0
		for paper in paper_dict['data']:
			rank = get_conference_rank(paper['venue'])
			if(rank != "Not found"):
				paper["rank"] = rank
				count = count+1
				result["papers"].append(paper)
		result["total"] = count
		return json.dumps(result)
