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

def twitter_shares(url):
	r = requests.get("http://urls.api.twitter.com/1/urls/count.json?url=http://www.buzzfeed.com"+url)
	twitter_shares = json.loads(r.text)
	if "count" in twitter_shares:
		return twitter_shares["count"]	

	logger.warn("No count available for http://www.buzzfeed.com"+url)	
	logger.warn("Received: "+str(r.text))
	return 0

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
			l["twitterShares"] = twitter_shares(l["url"])
			results.append(l)						
			continue

		spans = contents.find_all("span",class_="buzz_superlist_number")

		if len(spans) >= l["expectedListLength"]-5 and len(spans) <= l["expectedListLength"]+5:
			l["twitterShares"] = twitter_shares(l["url"])
			results.append(l)
			continue		
		
		spans = contents.find_all("span",class_="buzz_superlist_number_inline")

		if len(spans) >= l["expectedListLength"]-5 and len(spans) <= l["expectedListLength"]+5:
			l["twitterShares"] = twitter_shares(l["url"])
			results.append(l)
			continue
					
print json.dumps(results, sort_keys=True, indent=4, separators=(',', ': '))