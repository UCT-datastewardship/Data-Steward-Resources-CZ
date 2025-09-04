# Data-Steward-Resources-CZ
Available materials for Data Stewards in CZ and internationally

import pandas as pd
import requests

# Google Sheet published as CSV
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQDeitSl4vNEHlpzWkFBI_NEdskybm7UVtNpK9NVYNzB66V6XuH435QLcu0mAX2fwzLP3OKQCgjux6h/pubhtml?gid=621672034&single=true"

# Download into pandas
df = pd.read_csv(url)

# Save as CSV inside repo
df.to_csv("data.csv", index=False)

# (Optional) also save as Markdown table
with open("TABLE.md", "w") as f:
    f.write(df.to_markdown(index=False))
