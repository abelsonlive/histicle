import requests
import re
import json
from bs4 import BeautifulSoup

# 811 in original list
lists = json.loads(open("results-initial.json","r").read())
results = []

for l in lists:	

	r = requests.get("http://www.buzzfeed.com"+l["url"])
	if r.status_code == 200:		
		contents = BeautifulSoup(r.text,"html.parser")

		l["postDate"] = None

		time_span = contents.find("span",class_="buzz_datetime")
		
		if time_span and re.search('posted on',str(time_span.text)):
			time = time_span.find("time")
			if time and time.has_attr("datetime"):
				l["postDate"] = time["datetime"]		

		divs = contents.find_all("div",class_="buzz_superlist_item")

		if len(divs) >= l["expectedListLength"]-5 and len(divs) <= l["expectedListLength"]+5:
			results.append(l)
			continue

		spans = contents.find_all("span",class_="buzz_superlist_number")

		if len(spans) >= l["expectedListLength"]-5 and len(spans) <= l["expectedListLength"]+5:
			results.append(l)
			continue		
		
		spans = contents.find_all("span",class_="buzz_superlist_number_inline")

		if len(spans) >= l["expectedListLength"]-5 and len(spans) <= l["expectedListLength"]+5:
			results.append(l)
			continue
					
print json.dumps(results, sort_keys=True, indent=4, separators=(',', ': '))