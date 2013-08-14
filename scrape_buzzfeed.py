import dataset
import requests
import re
from thready import threaded
from BeautifulSoup import BeautifulSoup

# intitialize database
db = dataset.connect("sqlite:///listicles.db")
table = db['listicles']

# buzzfeed url
buzzfeed = "http://www.buzzfeed.com%s"

# category patterns - some of these are broken bc they scroll rather than page
categories = [
  "/animals/?p=%d&z=3JHTNE&r=1",
  "/celebrity/?p=%d&z=3JHTNE&r=1",
  "/entertainment/?p=%d&z=3JHTNE&r=1",
  "/food/?p=%d&z=3JHTNE&r=1",
  "/LGBT/?p=%d&z=3JHTNE&r=1",
  "/Music/?p=%d&z=3JI0KS&r=1",
  "/Politics/?p=%d&z=3JHTNE&r=1",
  "/Rewind/?p=%d&z=3JI0KS&r=1",
  "/Sports/?p=%d&z=3JI0KS&r=1",
  "/Viral/?p=%d&z=3JI0KS&r=1",
  "/LOL/?p=%d&z=3JHTNE&r=1",
  "/Win/?p=%d&z=3JI0KS&r=1",
  "/OMG/?p=%d&z=3JI0KS&r=1",
  "/Cute/?p=%d&z=3JI0KS&r=1",
  "/Geeky/?p=%d&z=3JI0KS&r=1",
  "/Trashy/?p=%d&z=3JI0KS&r=1",
  "/Fail/?p=%d&z=3JI0KS&r=1",
  "/WTF/?p=%d&z=3JI0KS&r=1"
]

# categories and pages
def gen_urls(categories):
  pages = range(1, 200)
  return [buzzfeed  % (c % p) for c in categories for p in pages]

# extract links and headlines
def dump_urls_and_headlines(content, category):
  soup = BeautifulSoup(content)
  for article in soup.findAll("article"):
    for link in article.findAll("a"):
      if link.text != "":
        datum = {
          "url": buzzfeed % link['href'],
          "headline": link.text,
          "category": category
        }
        table.upsert(datum, ["url"])

# generate urls by hitting page up until we get a 404
def fetch_data(url):
    category = url.split("/")[3].lower()
    print "scraping %s" % url
    r = requests.get(url)
    status_code = r.status_code
    if status_code == 200:
      dump_urls_and_headlines(r.content, category)

if __name__ == '__main__':
  urls = gen_urls(categories)
  threaded(urls, fetch_data, num_threads=10, max_queue=200)
