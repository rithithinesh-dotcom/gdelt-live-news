import streamlit as st
import pandas as pd
import re
from collections import Counter

st.set_page_config(
    page_title="TrendWatch | Live News Analytics",
    page_icon="📰",
    layout="wide"
)

DATA_URL = "https://raw.githubusercontent.com/rithithinesh-dotcom/gdelt-live-news/main/gdelt_live_news.csv"

@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv(DATA_URL)

    df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")
    df["collected_at"] = pd.to_datetime(df["collected_at"], errors="coerce")
    df["tone"] = pd.to_numeric(df["tone"], errors="coerce")

    df["sentiment"] = "Neutral"
    df.loc[df["tone"] > 1, "sentiment"] = "Positive"
    df.loc[df["tone"] < -1, "sentiment"] = "Negative"

    return df

def get_trending_words(headlines, top_n=8):
    stop_words = {
        "the", "a", "an", "and", "or", "of", "to", "in", "on", "for",
        "with", "from", "at", "by", "is", "are", "as", "this", "that",
        "news", "new", "says", "after", "over", "about", "will", "has",
        "have", "its", "their", "into", "more", "than", "how", "why"
    }

    words = []
    for headline in headlines.dropna():
        found_words = re.findall(r"\b[a-zA-Z]{4,}\b", str(headline).lower())
        words.extend(word for word in found_words if word not in stop_words)

    return Counter(words).most_common(top_n)

df = load_data()

st.title("📰 TrendWatch")
st.caption("Live News Trend & Sentiment Analytics Dashboard | Data source: GDELT")

with st.sidebar:
    st.header("🔎 Filter News")

    search = st.text_input("Search headlines")

    countries = sorted(df["source_country"].dropna().unique())
    selected_countries = st.multiselect(
        "Countries",
        countries,
        default=countries
    )

    languages = sorted(df["language"].dropna().unique())
    selected_languages = st.multiselect(
        "Languages",
        languages,
        default=languages
    )

    sentiment_options = ["Positive", "Neutral", "Negative"]
    selected_sentiments = st.multiselect(
        "Sentiment",
        sentiment_options,
        default=sentiment_options
    )

filtered_df = df[
    (df["source_country"].isin(selected_countries)) &
    (df["language"].isin(selected_languages)) &
    (df["sentiment"].isin(selected_sentiments))
].copy()

if search:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search, case=False, na=False)
    ]

trending_words = get_trending_words(filtered_df["title"])
top_topic = trending_words[0][0].title() if trending_words else "No data"

positive_percent = 0
if len(filtered_df) > 0:
    positive_percent = round(
        (filtered_df["sentiment"].eq("Positive").sum() / len(filtered_df)) * 100
    )

overall_sentiment = "Neutral"
if filtered_df["tone"].mean() > 1:
    overall_sentiment = "Positive"
elif filtered_df["tone"].mean() < -1:
    overall_sentiment = "Negative"

a, b, c, d = st.columns(4)
a.metric("Articles Analyzed", f"{len(filtered_df):,}")
b.metric("Top Trending Topic", top_topic)
c.metric("Overall Sentiment", overall_sentiment, f"{positive_percent}% positive")
d.metric("News Sources", filtered_df["domain"].nunique())

st.divider()

left, right = st.columns([2, 1])

with left:
    st.subheader("📈 Daily News Trend")

    trend_df = filtered_df.dropna(subset=["published_date"]).copy()
    trend_df["date"] = trend_df["published_date"].dt.date
    daily_count = trend_df.groupby("date").size()

    if not daily_count.empty:
        st.line_chart(daily_count)
    else:
        st.info("No date data is available for this filter.")

with right:
    st.subheader("🔥 Trending Topics")

    if trending_words:
        topic_df = pd.DataFrame(trending_words, columns=["Topic", "Articles"])
        topic_df["Topic"] = topic_df["Topic"].str.title()
        st.dataframe(topic_df, hide_index=True, use_container_width=True)
    else:
        st.info("No trending topics found.")

left2, right2 = st.columns(2)

with left2:
    st.subheader("😊 Sentiment Distribution")
    sentiment_counts = filtered_df["sentiment"].value_counts()
    st.bar_chart(sentiment_counts)

with right2:
    st.subheader("🌍 Top News Countries")
    country_counts = filtered_df["source_country"].value_counts().head(10)
    st.bar_chart(country_counts)

st.divider()
st.subheader("🗞️ Latest Headline Insights")

latest_df = filtered_df.sort_values(
    "collected_at",
    ascending=False
)[[
    "title", "source_country", "language",
    "published_date", "sentiment", "tone", "url"
]]

st.dataframe(latest_df, use_container_width=True, hide_index=True)

st.download_button(
    "Download Filtered News CSV",
    filtered_df.to_csv(index=False).encode("utf-8"),
    "trendscope_filtered_news.csv",
    "text/csv"
)
