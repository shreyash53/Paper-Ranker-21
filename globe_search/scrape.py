from bs4 import BeautifulSoup
import requests

url="http://cic.tju.edu.cn/faculty/zhileiliu/doc/COREComputerScienceConferenceRankings.html"

req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")

rank = dict()

for row in soup.find_all('tr'):
	data = row.find_all('td')
	if (len(data) == 3):
		acronym = data[0].text.strip('\n').strip('\r')
		name = data[1].text.strip('\n').strip('\r')
		ranking = data[2].text.strip('\n').strip('\r')
		rank[acronym] = {"rank":ranking, "name":name}

def get_conference_rank_from_web(acronym):
	if(acronym in rank.keys()):
		return rank[acronym]["rank"]
	else:
		return "Not found"