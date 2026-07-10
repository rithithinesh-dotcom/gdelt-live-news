import streamlit as st
import pandas as pd

st.set_page_config(page_title="Live News Dashboard", page_icon="📰", layout="wide")

DATA_URL = "https://raw.githubusercontent.com/rithithinesh-dotcom/gdelt-live-news/main/gdelt_live_news.csv"

@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv(DATA_URL)
    df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")
    df["tone"] = pd.to_numeric(df["tone"], errors="coerce")
    return df

df = load_data()

st.title("📰 Live News Trend and Sentiment Dashboard")
st.write("Live news collected using GDELT API")

search = st.text_input("Search news headline")

if search:
    df = df[df["title"].str.contains(search, case=False, na=False)]

col1, col2, col3 = st.columns(3)
col1.metric("Total Articles", len(df))
col2.metric("Countries", df["source_country"].nunique())
col3.metric("Average Tone", round(df["tone"].mean(), 2))

st.subheader("Top Countries")
st.bar_chart(df["source_country"].value_counts().head(10))

st.subheader("Latest News")
st.dataframe(
    df[["title", "source_country", "published_date", "tone", "url"]],
    use_container_width=True
)
