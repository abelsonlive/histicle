import matplotlib.pyplot as plot
import json

lengths = []
lists = json.loads(open("results-confirmed.json","r").read())
for l in lists:
	lengths.append(l["listLength"])

#print lengths
num_bins = max(lengths)-min(lengths)+1

plot.hist(lengths,bins=num_bins)
plot.title("BuzzFeed List Lengths")
plot.xlabel("List Length")
plot.ylabel("Frequency")
plot.show()