import requests
import re
import json
from bs4 import BeautifulSoup

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

	while True:

		if category in ajax_categories:
			paging = "/paging"
		else:
			paging = ""

		r = requests.get("http://www.buzzfeed.com/" + category + paging + "?p=" + str(page))

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