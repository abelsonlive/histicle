# from Marky import marky
# import json
# import re

# data = json.load(open("results-initial.json"))
# text = "\n".join([d['title'] for d in data if d is not ""]).lower()
# text = re.sub("[0-9]+", "[num]", text)

from pymarkovchain import MarkovChain
mc = MarkovChain("./markov")
mc.generateDatabase("This is another string of Text. It's automatically separated at question marks, periods, newlines and exclamation marks. This can be changed by giving generateDatabase an optional sentenceSep parameter")
mc.generateString()