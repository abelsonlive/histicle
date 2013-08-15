import requests
import re
import json
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("progress")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

def is_post_link(tag):
    return tag.name == "a" and tag.has_attr("rel:gt_act") and tag["rel:gt_act"] == "post/title"

def number_in_list(title):
	match = re.search(' [0-9]+ ',title)
	if match:
		return int(match.group(0).strip())

	match = re.match('^[0-9]+ ',title)
	if match:
		return int(match.group(0).strip())
	
	return False

found = []
results = []

ajax_categories = ["lol","win","omg","cute","trashy","fail","wtf","hot"]

for category in ["lol","win","omg","cute","trashy","fail","wtf","hot","business","politics","tech","sports","ideas","entertainment","celebrity","music","fashion","rewind","books","animals","food","diy","lgbt","geeky"]:
	
	page = 1

	for page in range(1,200):

		if category in ajax_categories:
			paging = "/paging"
			query_str = ""
		else:
			paging = ""
			query_str = "&z=3JJD78&r=1"

		to_scrape = "http://www.buzzfeed.com/" + category + paging + "?p=" + str(page) + query_str
		r = requests.get(to_scrape)
		logger.info("requesting "+to_scrape)

		if r.status_code != 200:
			break

		contents = BeautifulSoup(r.text,"html.parser")

		links = contents.find_all(is_post_link)

		for link in links:
			url = link["href"]
			title = re.sub('\s+',' ',link.text.strip())
			num = number_in_list(title)
			if num and num < 100 and url not in found:
				found.append(url)
				results.append({"url": url, "title": title, "expectedListLength": num})		

		page = page + 1

print json.dumps(results, sort_keys=True, indent=4, separators=(',', ': '))