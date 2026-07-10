import requests
import pandas as pd
from datetime import datetime
import os

query = "artificial intelligence"
file_name = "gdelt_live_news.csv"

url = "https://api.gdeltproject.org/api/v2/doc/doc"

params = {
    "query": query,
    "mode": "artlist",
    "format": "json",
    "maxrecords": 250,
    "sort": "DateDesc"
}

response = requests.get(url, params=params, timeout=30)

if response.status_code == 200:
    data = response.json()
    articles = data.get("articles", [])

    news_data = []

    for article in articles:
        news_data.append({
            "title": article.get("title"),
            "url": article.get("url"),
            "source_country": article.get("sourcecountry"),
            "language": article.get("language"),
            "published_date": article.get("seendate"),
            "tone": article.get("tone"),
            "domain": article.get("domain"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    new_df = pd.DataFrame(news_data)

    if os.path.exists(file_name):
        old_df = pd.read_csv(file_name)
        final_df = pd.concat([old_df, new_df], ignore_index=True)
        final_df = final_df.drop_duplicates(subset=["url"])
    else:
        final_df = new_df

    final_df.to_csv(file_name, index=False)

    print("Live news updated successfully!")
    print("New articles collected:", len(new_df))
    print("Total articles in dataset:", len(final_df))

else:
    print("Error:", response.status_code)
    print(response.text[:300])
