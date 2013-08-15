# from Marky import marky
from pymarkovchain import MarkovChain
import json
import re

data = json.load(open("results-initial.json"))
text = "\n".join([d['title'] for d in data if d is not ""]).lower()

mc = MarkovChain("./markov")
mc.generateDatabase(text)
print mc.generateString()