import dataset
import re
import pandas as pd

db = dataset.connect("sqlite:///listicles.db")
table = db['listicles']

re_listicle = re.compile("^([0-9]+).*", flags=re.IGNORECASE)

listicles = []
for row in table.all():
  m = re_listicle.search(row['headline'])
  if m is not None:
    row['list_length'] = int(m.group(1))
    listicles.append(row)

df = pd.DataFrame(listicles)
df = df.sort('list_length', ascending=1)
df.to_csv("data/listicles.csv")

