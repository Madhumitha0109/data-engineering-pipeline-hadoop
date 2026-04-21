import requests
from bs4 import BeautifulSoup
import pandas as pd

# Example: Global daily chart
url = "https://spotifycharts.com/regional/global/daily/latest"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Find rows of the chart table
rows = soup.select("table.chart-table tbody tr")

data = []

for row in rows:
    rank = row.select_one(".chart-table-position").text.strip()
    title = row.select_one(".chart-table-track strong").text.strip()
    artist = row.select_one(".chart-table-track span").text.strip("by ").strip()
    link = row.select_one("a")["href"]
    
    data.append({
        "Rank": int(rank),
        "Title": title,
        "Artist": artist,
        "TrackURL": link
    })

df = pd.DataFrame(data)
print(df.head())