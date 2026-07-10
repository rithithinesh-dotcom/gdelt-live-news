import requests
import pandas as pd
from datetime import datetime
import os

query = "technology"
file_name = "gdelt_live_news.csv"

url = "https://api.gdeltproject.org/api/v2/doc/doc"

params = {
    "query": query,
    "mode": "artlist",
    "format": "json",
    "maxrecords": 250,
    "sort": "DateDesc"
}

try:
    response = requests.get(url, params=params, timeout=60)
    print("Status code:", response.status_code)
    print("Request URL:", response.url)

    news_data = []

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        print("Articles found:", len(articles))

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
    else:
        print("GDELT error response:", response.text[:500])

    new_df = pd.DataFrame(
        news_data,
        columns=[
            "title", "url", "source_country", "language",
            "published_date", "tone", "domain", "collected_at"
        ]
    )

    if os.path.exists(file_name):
        old_df = pd.read_csv(file_name)
        final_df = pd.concat([old_df, new_df], ignore_index=True)
        final_df = final_df.drop_duplicates(subset=["url"])
    else:
        final_df = new_df

    final_df.to_csv(file_name, index=False)

    print("CSV created:", file_name)
    print("Total articles in dataset:", len(final_df))

except Exception as e:
    print("Python error:", str(e))

    # Create an empty CSV even if GDELT has a temporary error
    empty_df = pd.DataFrame(columns=[
        "title", "url", "source_country", "language",
        "published_date", "tone", "domain", "collected_at"
    ])
    empty_df.to_csv(file_name, index=False)
    print("Empty CSV created because of the error.")
